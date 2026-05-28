#!/usr/bin/env python3
import socket
import ssl
import threading
import argparse
import subprocess
import os
import sys

# --- UI Styling ---
C, G, Y, R, W, B = "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[0m", "\033[34m"

BANNER = fr"""
{C}  _  __  ____   _____   ______           _____  _    _         _______ 
 | |/ / / __ \ |  __ \ |  ____|         / ____|| |  | |    /\ |__   __|
 | ' / | |  | || |__) || |__    ______ | |     | |__| |   /  \   | |   
 |  <  | |  | ||  _  / |  __|  |______|| |     |  __  |  / /\ \  | |   
 | . \ | |__| || | \ \ | |____         | |____ | |  | | / ____ \ | |   
 |_|\_\ \____/ |_|  \_\|______|         \_____||_|  |_|/_/    \_\|_|{W}
               {Y}[ KØRE-SYSTEMS SECURE P2P HUB ]{W}
"""

def check_certificates():
    cert_file, key_file = "kore.crt", "kore.key"
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        print(f"{Y}[!] Generating native TLS keys...{W}")
        cmd = ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-keyout", key_file, "-out", cert_file, "-days", "365", "-nodes", "-subj", "/CN=KORE-CHAT"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return cert_file, key_file

def send_file(ssock, filepath):
    if not os.path.isfile(filepath):
        print(f"{R}[!] File not found.{W}")
        return
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    # Protocol: FILE:[name]:[size]
    header = f"FILE:{filename}:{filesize}"
    ssock.send(header.encode())
    
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            ssock.send(chunk)
    print(f"{G}[+] File '{filename}' sent.{W}")

def handle_recv(ssock):
    peer_name = "Peer"
    while True:
        try:
            data = ssock.recv(4096)
            if not data: break
            
            decoded = data.decode('utf-8', errors='ignore')
            
            if decoded.startswith("NAME:"):
                peer_name = decoded.split(":", 1)[1]
                print(f"{Y}[*] Peer identified as: {peer_name}{W}")
            
            elif decoded.startswith("FILE:"):
                _, fname, fsize = decoded.split(":")
                print(f"\n{Y}[!] Incoming File: {fname} ({fsize} bytes) from {peer_name}{W}")
                confirm = input(f"{Y}[?] Accept file? (y/n): {W}").lower()
                
                if confirm == 'y':
                    with open(f"received_{fname}", "wb") as f:
                        remaining = int(fsize)
                        while remaining > 0:
                            chunk = ssock.recv(min(remaining, 4096))
                            f.write(chunk)
                            remaining -= len(chunk)
                    print(f"{G}[+] File saved as 'received_{fname}'{W}")
                else:
                    print(f"{R}[X] File transfer rejected.{W}")
                    # Clear the buffer if rejected
                    ssock.recv(int(fsize)) 

            else:
                print(f"\n{G}[{peer_name}]:{W} {decoded}")
            
            print(f"{B}[YOU]:{W} ", end="", flush=True)
        except: break
    os._exit(0)

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--listen", action="store_true")
    group.add_argument("-c", "--connect", metavar="IP")
    parser.add_argument("-u", "--user", default="KoreUser", help="Your display name")
    parser.add_argument("-p", "--port", type=int, default=4433)
    args = parser.parse_args()

    print(BANNER)
    cert, key = check_certificates()

    if args.listen:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    else:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname, context.verify_mode = False, ssl.CERT_NONE

    context.load_cert_chain(certfile=cert, keyfile=key)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        if args.listen:
            sock.bind(('0.0.0.0', args.port)); sock.listen(1)
            print(f"{Y}[*] Listening on port {args.port}...{W}")
            raw_conn, _ = sock.accept()
            ssock = context.wrap_socket(raw_conn, server_side=True)
        else:
            sock.connect((args.connect, args.port))
            ssock = context.wrap_socket(sock, server_hostname=args.connect)

        # Initial Handshake: Send Username
        ssock.send(f"NAME:{args.user}".encode())

        threading.Thread(target=handle_recv, args=(ssock,), daemon=True).start()

        while True:
            msg = input(f"{B}[YOU]:{W} ")
            if msg.lower() in ['exit', 'quit']: break
            if msg.startswith("/send "):
                filepath = msg.split(" ", 1)[1]
                send_file(ssock, filepath)
            elif msg.strip():
                ssock.send(msg.encode())

    except Exception as e: print(f"{R}[ERROR]: {e}{W}")
    finally: sock.close()

if __name__ == "__main__":
    main()