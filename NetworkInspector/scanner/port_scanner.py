import socket
import concurrent.futures
from typing import List

def check_port(ip: str, port: int) -> bool:
    """
    Check if a specific port is open on the target host.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)  # Increased timeout for better reliability
            result = sock.connect_ex((ip, port))
            if result == 0:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except:
                    pass
                return True
            return False
    except (socket.timeout, socket.error):
        return False

def scan_ports(ip: str, ports: List[int]) -> List[int]:
    """
    Scan multiple ports on a target host using parallel scanning.
    """
    open_ports = []
    max_workers = min(50, len(ports))  # Adjust workers based on port count

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {executor.submit(check_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    open_ports.append(port)
            except Exception:
                continue

    return sorted(open_ports)