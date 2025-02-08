import socket
import concurrent.futures
from ipaddress import IPv4Network
import struct
import time

def create_icmp_packet():
    """Create an ICMP echo request packet."""
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    header = struct.pack('bbHHh', 8, 0, 0, 0, 1)
    data = struct.pack('d', time.time())
    # Calculate checksum
    checksum = 0
    for i in range(0, len(header + data), 2):
        if i + 1 < len(header + data):
            checksum += (header + data)[i] + ((header + data)[i+1] << 8)
        else:
            checksum += (header + data)[i]
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff
    # Reconstruct header with checksum
    header = struct.pack('bbHHh', 8, 0, checksum, 0, 1)
    return header + data

def tcp_ping_host(ip):
    """
    Alternative host discovery using TCP connection attempt.
    """
    # Handle localhost specially
    if str(ip) == "127.0.0.1":
        return True

    common_ports = [80, 443, 22, 445]
    for port in common_ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)
                result = sock.connect_ex((str(ip), port))
                if result == 0:
                    return True
        except socket.error:
            continue
    return False

def ping_host(ip):
    """
    Try to ping a host. Falls back to TCP ping if ICMP is not available.
    """
    # Special handling for localhost
    if str(ip) == "127.0.0.1":
        return True

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
            sock.settimeout(1)
            packet = create_icmp_packet()
            sock.sendto(packet, (str(ip), 0))
            sock.recvfrom(1024)
            return True
    except (socket.timeout, socket.error, PermissionError):
        # Fallback to TCP ping
        return tcp_ping_host(ip)

def discover_hosts(network: IPv4Network):
    """
    Discover active hosts in the given network using parallel scanning.
    """
    active_hosts = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {executor.submit(ping_host, ip): ip for ip in network.hosts()}
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    active_hosts.append(ip)
            except Exception:
                continue

    return sorted(active_hosts)