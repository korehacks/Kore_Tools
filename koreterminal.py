#!/usr/bin/env python3

import sys
import json
import subprocess
import readline
import os
from pathlib import Path
import shlex

# Config
CONFIG_DIR = Path.home() / ".koreterminal"
CONFIG_FILE = CONFIG_DIR / "commands.json"
HISTORY_FILE = CONFIG_DIR / "history.txt"

# Clean KORE Branding
KORE_ASCII = r"""
  ██╗  ██╗ ██████╗ ██████╗ ███████╗
  ██║ ██╔╝██╔═══██╗██╔══██╗██╔════╝
  █████╔╝ ██║   ██║██████╔╝█████╗  
  ██╔═██╗ ██║   ██║██╔══██╗██╔══╝  
  ██║  ██╗╚██████╔╝██║  ██║███████╗
  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
  
           K O R E   T E R M I N A L
           Kali Linux Hacker Edition
"""

# Colors
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Package Mapping
CMD_TO_PACKAGE = {
    "nmap": "nmap", "msfconsole": "metasploit-framework", "sqlmap": "sqlmap",
    "hydra": "hydra", "john": "john", "hashcat": "hashcat", "wpscan": "wpscan",
    "nikto": "nikto", "gobuster": "gobuster", "ffuf": "ffuf", "aircrack-ng": "aircrack-ng",
    "bettercap": "bettercap", "responder": "responder", "crackmapexec": "crackmapexec",
}

def ensure_config():
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump({}, f, indent=4)

def load_commands():
    ensure_config()
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except:
        return {}

def save_commands(commands):
    data = {str(k): v for k, v in commands.items()}
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_next_id(commands):
    return max(commands.keys(), default=0) + 1

def is_command_installed(cmd_name):
    try:
        result = subprocess.run(f"command -v {cmd_name}", shell=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except:
        return False

def install_package(package):
    print(f"{RED}[!] {package} is not installed.{RESET}")
    confirm = input(f"{YELLOW}Install {package}? (y/n): {RESET}").strip().lower()
    if confirm != 'y':
        return False
    print(f"{GREEN}[+] Installing {package}...{RESET}")
    try:
        subprocess.run(f"sudo apt update && sudo apt install -y {package}", 
                      shell=True, check=True)
        print(f"{GREEN}[+] {package} installed successfully!{RESET}")
        return True
    except:
        print(f"{RED}[-] Installation failed.{RESET}")
        return False

def add_command(cmd_id, real_cmd, custom_cmd):
    commands = load_commands()
    if cmd_id is None:
        cmd_id = get_next_id(commands)
    else:
        cmd_id = int(cmd_id)
    commands[cmd_id] = {"real": real_cmd, "custom": custom_cmd}
    save_commands(commands)
    print(f"{GREEN}[+] Added ID {cmd_id}: '{custom_cmd}' → '{real_cmd}'{RESET}")

def edit_command(cmd_id, real_cmd, custom_cmd):
    commands = load_commands()
    cmd_id = int(cmd_id)
    if cmd_id in commands:
        commands[cmd_id] = {"real": real_cmd, "custom": custom_cmd}
        save_commands(commands)
        print(f"{GREEN}[+] Updated ID {cmd_id}{RESET}")
    else:
        print(f"{RED}[-] ID {cmd_id} not found.{RESET}")

def delete_command(cmd_id):
    commands = load_commands()
    cmd_id = int(cmd_id)
    if cmd_id in commands:
        del commands[cmd_id]
        save_commands(commands)
        print(f"{GREEN}[+] Deleted ID {cmd_id}{RESET}")
    else:
        print(f"{RED}[-] ID {cmd_id} not found.{RESET}")

def list_commands():
    commands = load_commands()
    if not commands:
        print(f"{YELLOW}No custom commands saved yet.{RESET}")
        return
    print(f"\n{GREEN}{'ID':<4} {'Custom Command':<25} → Real Command{RESET}")
    print("-" * 75)
    for cid, data in sorted(commands.items()):
        print(f"{cid:<4} {data['custom']:<25} → {data['real']}")
    print("")

def print_help():
    print(KORE_ASCII)
    print(f"{CYAN}KORE Terminal Commands:{RESET}")
    print(f"  {GREEN}add id=<number> \"real command\" \"custom command\"{RESET}")
    print(f"  {GREEN}edit id=<number> \"real command\" \"custom command\"{RESET}")
    print(f"  {GREEN}delete id=<number>{RESET}")
    print(f"  {GREEN}list{RESET}")
    print(f"  {GREEN}help{RESET}")
    print(f"  {GREEN}exit / quit{RESET}")
    print(f'\n{YELLOW}Example:{RESET}')
    print('  add id=1 "nmap -sV -sC -O -T4" "fullscan"')

def setup_history():
    try:
        readline.read_history_file(str(HISTORY_FILE))
    except FileNotFoundError:
        pass
    readline.set_history_length(1000)
    import atexit
    atexit.register(lambda: readline.write_history_file(str(HISTORY_FILE)))

def handle_cd(args):
    try:
        if not args or args[0] == "\~":
            os.chdir(Path.home())
        else:
            os.chdir(os.path.expanduser(args[0]))
        print(f"{GREEN}Changed directory to: {os.getcwd()}{RESET}")
    except FileNotFoundError:
        print(f"{RED}cd: No such directory: {args[0] if args else '\~'}{RESET}")
    except Exception as e:
        print(f"{RED}cd error: {e}{RESET}")

def handle_pwd():
    print(os.getcwd())

def run_kore_terminal():
    setup_history()
    os.chdir(Path.home())
    
    print(KORE_ASCII)
    print(f"{GREEN}KORE Terminal Started in \~{RESET}")
    print(f"{CYAN}Up/Down arrows = History | cd, ls, pwd work properly{RESET}\n")
    
    while True:
        try:
            user_input = input(f"{BOLD}{GREEN}kore@kalilinux{RESET}{RED} \~# {RESET}").strip()
            
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print(f"{RED}[-] Exiting KORE Terminal...{RESET}")
                break

            if user_input.lower() == 'help':
                print_help()
                continue

            if user_input.lower() == 'list':
                list_commands()
                continue

            try:
                parts = shlex.split(user_input)
            except:
                print(f"{RED}[-] Invalid syntax{RESET}")
                continue

            cmd_type = parts[0].lower()
            args = parts[1:]

            # Built-in Commands
            if cmd_type == 'cd':
                handle_cd(args)
                continue
            if cmd_type == 'pwd':
                handle_pwd()
                continue

            # Custom Command Management
            if cmd_type == 'add' and len(parts) >= 4:
                id_str = parts[1]
                if id_str.startswith("id="):
                    try:
                        cid = id_str.split('=', 1)[1]
                        real_cmd = parts[2]
                        custom_cmd = parts[3]
                        add_command(cid, real_cmd, custom_cmd)
                    except:
                        print(f"{RED}[-] Invalid add format.{RESET}")
                continue

            elif cmd_type == 'edit' and len(parts) >= 4:
                id_str = parts[1]
                if id_str.startswith("id="):
                    try:
                        cid = id_str.split('=', 1)[1]
                        real_cmd = parts[2]
                        custom_cmd = parts[3]
                        edit_command(cid, real_cmd, custom_cmd)
                    except:
                        print(f"{RED}[-] Invalid edit format.{RESET}")
                continue

            elif cmd_type == 'delete' and len(parts) == 2:
                id_str = parts[1]
                if id_str.startswith("id="):
                    try:
                        cid = id_str.split('=', 1)[1]
                        delete_command(cid)
                    except:
                        print(f"{RED}[-] Invalid delete format.{RESET}")
                continue

            # Normal Command Execution
            commands = load_commands()
            first_word = parts[0]
            full_cmd = None

            for data in commands.values():
                if data['custom'] == first_word:
                    real_base = data['real']
                    extra = " " + " ".join(parts[1:]) if len(parts) > 1 else ""
                    full_cmd = real_base + extra
                    break

            if full_cmd is None:
                full_cmd = user_input

            main_tool = full_cmd.split()[0]
            if not is_command_installed(main_tool) and main_tool not in ['ls', 'cat', 'echo', 'whoami', 'pwd', 'mkdir', 'touch']:
                package = CMD_TO_PACKAGE.get(main_tool, main_tool)
                if package and not install_package(package):
                    continue

            try:
                subprocess.run(full_cmd, shell=True, check=True)
            except subprocess.CalledProcessError:
                pass
            except FileNotFoundError:
                print(f"{RED}[-] Command '{main_tool}' not found.{RESET}")
            except Exception as e:
                print(f"{RED}[-] Error: {e}{RESET}")

        except KeyboardInterrupt:
            print(f"\n{RED}[-] Use 'exit' to quit.{RESET}")
        except Exception as e:
            print(f"{RED}[-] Unexpected error: {e}{RESET}")

def main():
    if len(sys.argv) == 1:
        run_kore_terminal()
    else:
        print("Run without arguments: python3 koreterminal.py")

if __name__ == "__main__":
    main()
