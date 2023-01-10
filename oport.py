import sys
import socket
import argparse
import textwrap

def parse_ports(ports_str):
  try:
    parts = ports_str.split('-')
    if len(parts) == 1:
      # Single port or list of ports
      return [int(p) for p in parts[0].split(',')]
    elif len(parts) == 2:
      # Port range
      return range(int(parts[0]), int(parts[1])+1)
  except:
    return []

parser = argparse.ArgumentParser(
        description='An easy tool for finding open ports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
        ./oport.py <IP_Address> --port <Port_Num>
        '''))
parser.add_argument('ip', help='Add IP_Address or host')
parser.add_argument('--port', default='1-65535', help='Add Ports (e.g. 1-65535 or 80,443,22)')
args = parser.parse_args()
ip = args.ip
ports_str = args.port
ports = parse_ports(ports_str)

def probe_port(ip, port): 
  try: 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.settimeout(0.5) 
    r = sock.connect_ex((ip, port))   
    sock.close()
    return r == 0
  except:
    return False

def scan_ports(ip, ports):
  open_ports = []
  for port in ports: 
    if probe_port(ip, port):
      open_ports.append(port) 
  return open_ports

def main():
  open_ports = scan_ports(ip, ports)

  if open_ports: 
    print("Open Ports are: ") 
    print(sorted(open_ports)) 
  else: 
    print("Looks like no ports are open :(")

if __name__ == '__main__':
  main()
