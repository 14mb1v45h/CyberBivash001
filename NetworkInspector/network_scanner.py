#!/usr/bin/env python3
import argparse
import ipaddress
from rich.console import Console
from rich.table import Table
from scanner.host_discovery import discover_hosts
from scanner.port_scanner import scan_ports
from scanner.network_utils import get_network_interfaces

console = Console()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Network Scanner Tool')
    parser.add_argument('-n', '--network', type=str, help='Network to scan (CIDR notation)')
    parser.add_argument('-p', '--ports', type=str, help='Ports to scan (e.g., 80,443 or 1-1000)')
    parser.add_argument('-i', '--interface', action='store_true', help='List network interfaces')
    return parser.parse_args()

def parse_ports(ports_str):
    ports = []
    if not ports_str:
        return list(range(1, 1001))  # Default port range
    
    for part in ports_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return sorted(list(set(ports)))

def display_interfaces():
    interfaces = get_network_interfaces()
    table = Table(title="Network Interfaces")
    table.add_column("Interface", style="cyan")
    table.add_column("IP Address", style="green")
    table.add_column("Netmask", style="yellow")

    for interface, details in interfaces.items():
        table.add_row(interface, details['ip'], details['netmask'])
    
    console.print(table)

def main():
    args = parse_arguments()

    if args.interface:
        display_interfaces()
        return

    if not args.network:
        console.print("[red]Error: Please provide a network to scan using -n option[/red]")
        return

    try:
        network = ipaddress.ip_network(args.network)
        ports = parse_ports(args.ports)

        with console.status("[bold green]Scanning network...") as status:
            # Discover hosts
            console.print("\n[bold]Starting host discovery...[/bold]")
            active_hosts = discover_hosts(network)
            
            if not active_hosts:
                console.print("[yellow]No active hosts found.[/yellow]")
                return

            # Display active hosts
            hosts_table = Table(title=f"Active Hosts in {network}")
            hosts_table.add_column("IP Address", style="cyan")
            hosts_table.add_column("Status", style="green")
            
            for host in active_hosts:
                hosts_table.add_row(str(host), "Active")
            
            console.print(hosts_table)

            # Scan ports for each active host
            for host in active_hosts:
                console.print(f"\n[bold]Scanning ports for {host}...[/bold]")
                open_ports = scan_ports(str(host), ports)
                
                if open_ports:
                    ports_table = Table(title=f"Open Ports for {host}")
                    ports_table.add_column("Port", style="cyan")
                    ports_table.add_column("Status", style="green")
                    
                    for port in open_ports:
                        ports_table.add_row(str(port), "Open")
                    
                    console.print(ports_table)
                else:
                    console.print("[yellow]No open ports found.[/yellow]")

    except ValueError as e:
        console.print(f"[red]Error: Invalid network format - {str(e)}[/red]")
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main()
