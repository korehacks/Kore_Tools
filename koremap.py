import socket
import sys
import threading
import ssl
from queue import Queue
from urllib.parse import urlparse

# ANSI Colors for a professional KØRE look
G, R, W, C, Y = "\033[92m", "\033[91m", "\033[97m", "\033[96m", "\033[93m"
END = "\033[0m"

def print_banner():
    print(f"{R}  _  __  ____  _____  ______ ")
    print(f" | |/ / / __ \|  __ \|  ____|")
    print(f" | ' / | |  | | |__) | |__   ")
    print(f" |  <  | |  | |  _  /|  __|  ")
    print(f" | . \ | |__| | | \ \| |____ ")
    print(f" |_|\_\ \____/|_|  \_\______|{END}")
    print(f"{W}      [ GATEWAY ENGINE v5.2 ]{END}\n")

def clean_url(target):
    if "://" in target:
        return urlparse(target).hostname
    return target

def identify_gateway(target_ip, port):
    """Probes the port to identify if it's HTTP, HTTPS, or other."""
    try:
        # Check for HTTPS (SSL/TLS)
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        with socket.create_connection((target_ip, port), timeout=1) as sock:
            with context.wrap_socket(sock, server_hostname=target_ip) as ssock:
                return "HTTPS (Encrypted Gateway)"
    except:
        try:
            # Check for HTTP
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((target_ip, port))
                s.sendall(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
                response = s.recv(10)
                if b"HTTP" in response:
                    return "HTTP (Standard Gateway)"
        except:
            pass
    
    # Default service lookup
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown Service"

# Global data
open_gateways = [] # Stores (port, service_name)
queue = Queue()

def audit_worker(target_ip):
    while not queue.empty():
        port = queue.get()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((target_ip, port)) == 0:
                    service = identify_gateway(target_ip, port)
                    open_gateways.append((port, service))
        except:
            pass
        queue.task_done()

def run_kore():
    if len(sys.argv) < 2:
        print_banner()
        print(f"{Y}Usage: python3 koremap.py <target_url_or_ip>{END}")
        return

    target = clean_url(sys.argv[1])
    print_banner()
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"{C}[*] Target: {W}{target} ({target_ip}){END}")
    except:
        print(f"{R}[!] Failed to resolve target.{END}")
        return

    # Scan Range: Focus on Gateway and Web ports
    ports = [21, 22, 25, 53, 80, 110, 443, 3306, 5432, 8080, 8443, 9000]
    total = len(ports)
    for p in ports: queue.put(p)

    print(f"{Y}[*] Probing {total} Gateways...{END}")

    for _ in range(10): # Efficient threading for mobile
        t = threading.Thread(target=audit_worker, args=(target_ip,))
        t.daemon = True
        t.start()

    while not queue.empty():
        done = total - queue.qsize()
        sys.stdout.write(f"\r{W}[+] Progress: {(done/total)*100:.1f}% ({done}/{total}){END}")
        sys.stdout.flush()

    queue.join()
    print(f"\n{C}-----------------------------------------{END}")
    
    if open_gateways:
        for port, service in sorted(open_gateways):
            print(f"{G}[OPEN]{END} Port {port:<5} | {W}{service}{END}")
    else:
        print(f"{R}[-] No active gateways found.{END}")

if __name__ == "__main__":
    run_kore()
