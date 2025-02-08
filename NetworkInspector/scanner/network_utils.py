import socket
import netifaces

def get_network_interfaces():
    """
    Get all network interfaces and their IP addresses.
    Returns a dictionary of interface names and their details.
    """
    interfaces = {}
    
    for interface in netifaces.interfaces():
        try:
            # Get IP addresses for this interface
            addrs = netifaces.ifaddresses(interface)
            
            # Only include interfaces with IPv4 addresses
            if netifaces.AF_INET in addrs:
                ip = addrs[netifaces.AF_INET][0]['addr']
                netmask = addrs[netifaces.AF_INET][0]['netmask']
                
                interfaces[interface] = {
                    'ip': ip,
                    'netmask': netmask
                }
        except Exception:
            continue
    
    return interfaces

def get_hostname(ip):
    """
    Attempt to resolve hostname for an IP address.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None
