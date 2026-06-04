#!/usr/bin/env python3
import socket
import threading
import argparse
import os
import sys
import time
import signal
from datetime import datetime

# --- UI Styling ---
C, G, Y, R, W, B = "\033[36m", "\033[32m", "\033[33m", "\033[31m", "\033[0m", "\033[34m"

BANNER = fr"""
{C}  _  __  ____   _____   ______           _____  _    _         _______ 
 | |/ / / __ \ |  __ \ |  ____|         / ____|| |  | |    /\ |__   __|
 | ' / | |  | || |__) || |__    ______ | |     | |__| |   /  \   | |   
 |  <  | |  | ||  _  / |  __|  |______|| |     |  __  |  / /\ \  | |   
 | . \ | |__| || | \ \ | |____         | |____ | |  | | / ____ \ | |   
 |_|\_\ \____/ |_|  \_\|______|         \_____||_|  |_|/_/    \_\|_|{W}
               {Y}[ KØRE-SYSTEMS ZERO-DEPENDENCY HUB ]{W}
"""

# Global controls
file_transfer_active = threading.Event()
global_sock = None  
XOR_KEY = b"KoreSecureP2P_DefaultPassphraseToken!" # Fallback dynamic block cipher array key

def write_log(action, peer, filename, size, status):
    """Logs file actions locally to 'kore_downloads.log'."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {action} | Peer: {peer} | File: {filename} | Size: {size} bytes | Status: {status}\n"
    with open("kore_downloads.log", "a") as f:
        f.write(log_entry)

def print_progress(current, total, start_time, prefix=''):
    """Ultra-compact progress bar optimized specifically for Termux layout constraints."""
    elapsed_time = time.time() - start_time
    speed = current / elapsed_time if elapsed_time > 0 else 0
    
    if speed > 1024 * 1024:
        speed_text = f"{speed / 1024 / 1024:.1f}M/s"
    else:
        speed_text = f"{speed / 1024:.1f}K/s"
        
    percent = float(current) * 100 / total if total > 0 else 0.0
    iteration = int(percent // 10)
    bar = '█' * iteration + '-' * (10 - iteration)
    
    output = f'\r{prefix} |{bar}| {percent:.1f}% ({speed_text}) [Ctrl+C to Cancel]'
    sys.stdout.write('\033[K' + output)
    sys.stdout.flush()

def xor_crypt(data, key):
    """Symmetric stream processing engine using pure native runtime loop structures."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def secure_send(sock, raw_bytes):
    """Encrypts payload natively and structures it into a safe length-prefixed packet boundary."""
    encrypted = xor_crypt(raw_bytes, XOR_KEY)
    sock.sendall(len(encrypted).to_bytes(4, byteorder='big') + encrypted)

def secure_recv(sock):
    """Reads stream boundary and decrypts packet payloads cleanly with zero delay loops."""
    size_bytes = sock.recv(4)
    if not size_bytes or len(size_bytes) < 4:
        return b""
    expected_size = int.from_bytes(size_bytes, byteorder='big')
    
    data = b""
    while len(data) < expected_size:
        packet = sock.recv(expected_size - len(data))
        if not packet:
            return b""
        data += packet
    return xor_crypt(data, XOR_KEY)

def send_file(sock, filepath):
    """Transmits target file safely with explicit high-speed network chunk loops."""
    if not os.path.isfile(filepath):
        print(f"\n{R}[!] Error: File not found at '{filepath}'{W}")
        return
    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    
    file_transfer_active.set()
    try:
        secure_send(sock, f"FILE_REQ:{filename}:{filesize}".encode())
        print(f"{Y}[*] Waiting for peer to accept file '{filename}'...{W}", flush=True)
        
        response = secure_recv(sock).decode('utf-8', errors='ignore')
        if response == "FILE_OK":
            print(f"{G}[+] Peer accepted! Initiating data stream...{W}")
            bytes_sent = 0
            last_update_time = 0
            start_time = time.time()
            
            with open(filepath, "rb") as f:
                while chunk := f.read(4096):
                    secure_send(sock, b"DATA:" + chunk)
                    bytes_sent += len(chunk)
                    
                    if time.time() - last_update_time > 0.1:
                        print_progress(bytes_sent, filesize, start_time, prefix=f'{G}Send{W}')
                        last_update_time = time.time()
            
            secure_send(sock, b"EOF")
            print_progress(filesize, filesize, start_time, prefix=f'{G}Send{W}') 
            print(f"\n{G}[+] Transfer Complete.{W}")
            write_log("UPLOAD", "Remote-Peer", filename, filesize, "SUCCESS")
        else:
            print(f"{R}[X] File transfer was rejected by the peer.{W}")
            write_log("UPLOAD", "Remote-Peer", filename, filesize, "REJECTED_BY_PEER")
            
    except (socket.error, ConnectionResetError):
        print(f"\n{R}[X] Transfer cancelled / Connection interrupted.{W}")
        write_log("UPLOAD", "Remote-Peer", filename, filesize, "CANCELLED")
    finally:
        file_transfer_active.clear()

def handle_recv(sock):
    """Background parallel worker managing incoming decrypted protocol traffic chunks."""
    peer_name = "Peer"
    while True:
        try:
            raw_data = secure_recv(sock)
            if not raw_data: break
            
            if raw_data.startswith(b"NAME:"):
                peer_name = raw_data.split(b":", 1)[1].decode('utf-8', errors='ignore')
                print(f"{Y}[*] Peer identified as: {peer_name}{W}")
                print(f"{B}[YOU]:{W} ", end="", flush=True)
            
            elif raw_data.startswith(b"FILE_REQ:"):
                file_transfer_active.set()
                decoded = raw_data.decode('utf-8', errors='ignore')
                _, fname, fsize = decoded.split(":")
                fsize = int(fsize)
                
                print(f"\n{Y}[!] {peer_name} wants to send: {fname} ({fsize} bytes){W}")
                confirm = input(f"{Y}[?] Accept file? (y/n): {W}").lower()
                
                if confirm == 'y':
                    secure_send(sock, "FILE_OK".encode())
                    
                    start_time = time.time()
                    last_update_time = 0
                    received = 0
                    aborted = False
                    
                    with open(f"received_{fname}", "wb") as f:
                        while received < fsize:
                            payload = secure_recv(sock)
                            if not payload or payload == b"EOF":
                                if received < fsize: aborted = True
                                break
                            if payload.startswith(b"DATA:"):
                                chunk = payload[5:]
                                f.write(chunk)
                                received += len(chunk)
                                
                                if time.time() - last_update_time > 0.1:
                                    print_progress(received, fsize, start_time, prefix=f'{G}Recv{W}')
                                    last_update_time = time.time()
                    
                    if aborted:
                        print(f"\n{R}[X] Download cancelled or incomplete.{W}")
                        write_log("DOWNLOAD", peer_name, fname, fsize, "CANCELLED")
                        if os.path.exists(f"received_{fname}"): os.remove(f"received_{fname}")
                    else:
                        print_progress(fsize, fsize, start_time, prefix=f'{G}Recv{W}')
                        print(f"\n{G}[+] Saved as 'received_{fname}'{W}")
                        write_log("DOWNLOAD", peer_name, fname, fsize, "ACCEPTED")
                else:
                    secure_send(sock, "FILE_REJECT".encode())
                    print(f"{R}[X] File rejected.{W}")
                    write_log("DOWNLOAD", peer_name, fname, fsize, "REJECTED")
                
                file_transfer_active.clear()
                print(f"{B}[YOU]:{W} ", end="", flush=True)

            else:
                if not file_transfer_active.is_set():
                    decoded_msg = raw_data.decode('utf-8', errors='ignore')
                    print(f"\n{G}[{peer_name}]:{W} {decoded_msg}")
                    print(f"{B}[YOU]:{W} ", end="", flush=True)
        except: 
            break
    print(f"\n{R}[!] Connection closed.{W}")
    os._exit(0)

def main():
    global global_sock
    parser = argparse.ArgumentParser(description="KØRE-CHAT: Pure zero-dependency script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--listen", action="store_true")
    group.add_argument("-c", "--connect", metavar="IP")
    parser.add_argument("-u", "--user", default="KoreUser")
    parser.add_argument("-p", "--port", type=int, default=4433)
    args = parser.parse_args()

    print(BANNER)
    
    def sigint_handler(signum, frame):
        global global_sock
        if file_transfer_active.is_set() and global_sock:
            try:
                global_sock.shutdown(socket.SHUT_RDWR)
                global_sock.close()
            except:
                pass
            print(f"\n{R}[X] Transfer aborted instantly via Ctrl+C.{W}")
            os._exit(0)
        else:
            print(f"\n{R}[!] Use 'exit' or 'quit' to close chat session safely.{W}")
            print(f"{B}[YOU]:{W} ", end="", flush=True)

    signal.signal(signal.SIGINT, sigint_handler)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        if args.listen:
            sock.bind(('0.0.0.0', args.port))
            sock.listen(1)
            print(f"{Y}[*] Listening on port {args.port}...{W}")
            active_sock, _ = sock.accept()
        else:
            print(f"{Y}[*] Connecting to {args.connect}:{args.port}...{W}")
            sock.connect((args.connect, args.port))
            active_sock = sock

        global_sock = active_sock
        
        secure_send(active_sock, f"NAME:{args.user}".encode())
        threading.Thread(target=handle_recv, args=(active_sock,), daemon=True).start()

        while True:
            if not file_transfer_active.is_set():
                try:
                    msg = input(f"{B}[YOU]:{W} ")
                except (KeyboardInterrupt, EOFError):
                    continue
                    
                if msg.lower() in ['exit', 'quit']: 
                    break
                    
                if msg.startswith("/send "):
                    parts = msg.split(" ", 1)
                    if len(parts) > 1:
                        filepath = parts[1].strip()
                        send_file(active_sock, filepath)
                    else:
                        print(f"{R}[!] Usage: /send [path_to_file]{W}")
                elif msg.strip():
                    secure_send(active_sock, msg.encode())
            else:
                time.sleep(0.2)
                
    except Exception as e: 
        print(f"\n{R}[ERROR]: {e}{W}")
    finally: 
        sock.close()

if __name__ == "__main__":
    main()
