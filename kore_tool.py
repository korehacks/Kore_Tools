#!/usr/bin/env python3
"""
KORE TOOL - A Kali Linux Tool Collection
Created by KORE COMMUNITY
"""

import os
import subprocess
import sys

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    """Print the KORE TOOL banner"""
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   {Colors.RED}██╗  ██╗{Colors.CYAN}███████╗{Colors.CYAN}███████╗{Colors.CYAN}███████╗{Colors.CYAN}  ║
║   {Colors.RED}██║ ██╔╝{Colors.CYAN}██║  ██║{Colors.CYAN}██║  ██║{Colors.CYAN}██╔════╝{Colors.CYAN}  ║
║   {Colors.RED}████║╔╝ {Colors.CYAN}██║  ██║{Colors.CYAN}██████║{Colors.CYAN} ███████╗{Colors.CYAN}  ║
║   {Colors.RED}██╔═██╗ {Colors.CYAN}██║  ██║{Colors.CYAN}██╔══██║{Colors.CYAN}██╔════╝{Colors.CYAN}  ║
║   {Colors.RED}██║  ██╗{Colors.CYAN}███████║{Colors.CYAN}██║  ██║{Colors.CYAN}███████╗{Colors.CYAN}  ║
║   {Colors.RED}╚═╝  ╚═╝{Colors.CYAN}╚══════╝{Colors.CYAN}╚═╝  ╚═╝{Colors.CYAN}╚══════╝{Colors.CYAN}  ║
║                                                               ║
║                    {Colors.YELLOW}K O R E{Colors.CYAN}        ║
║                                                               ║
║               {Colors.GREEN}Created by KORE COMMUNITY{Colors.CYAN}                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
""")

def home_menu():
    """Display the home menu"""
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}[1] KORE TOOLS{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}[2] OTHER TOOLS{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}[3] SUBSCRIBE OUR YOUTUBE{Colors.END}")
        print(f"{Colors.GREEN}{Colors.BOLD}[4] OUR WEBSITE{Colors.END}")
        print(f"{Colors.RED}{Colors.BOLD}[5] EXIT{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        
        choice = input(f"\n{Colors.YELLOW}Enter your choice (1-5): {Colors.END}")
        
        if choice == '1':
            kore_tools_menu()
        elif choice == '2':
            other_tools_menu()
        elif choice == '3':
            youtube_option()
        elif choice == '4':
            website_option()
        elif choice == '5':
            print(f"\n{Colors.GREEN}Thank you for using KORE TOOL! Goodbye!{Colors.END}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid choice! Please try again.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def kore_tools_menu():
    """Display Kore Tools menu - tools from kore community"""
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}KORE COMMUNITY TOOLS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        print(f"\n{Colors.YELLOW}Note: Tools will be added by KORE COMMUNITY. Contact us to add your tool!{Colors.END}\n")
        
        # Placeholder for Kore Community tools - user will provide these
        print(f"{Colors.GREEN}[1] KORE TERMINAL - Make command easy{Colors.END}")
        print(f"{Colors.GREEN}[2] KORE CHAT - Encrypted Chat{Colors.END}")
        print(f"{Colors.GREEN}[3] Tool 3 (Coming Soon){Colors.END}")
        print(f"{Colors.GREEN}[4] Tool 4 (Coming Soon){Colors.END}")
        print(f"{Colors.GREEN}[5] Tool 5 (Coming Soon){Colors.END}")
        print(f"{Colors.RED}[6] BACK TO MAIN MENU{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        
        choice = input(f"\n{Colors.YELLOW}Enter your choice (1-6): {Colors.END}")
        
        
        if choice == '1':
            kore_terminal()
        elif choice == '2':
            kore_chat()
        elif choice in [ '3', '4', '5']:
            print(f"\n{Colors.YELLOW}This tool is coming soon! Contact KORE COMMUNITY to add tools.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")
        elif choice == '6':
            break
        else:
            print(f"{Colors.RED}Invalid choice! Please try again.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def kore_terminal():
   
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}KORE TERMINAL - MAKE YOUR COMMANDS EASY AS SHIT{Colors.END}\n")
    
    start = input(f"{Colors.YELLOW}Start kore terminal: {Colors.END}")
   
    command = f"python3 koreterminal.py"
   
    
    print(f"\n{Colors.CYAN}Executing command: {Colors.END}{Colors.GREEN}{command}{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to execute this command? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system(command)
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")


def kore_chat():
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}KORE CHAT - ENCRYPTED CHAT{Colors.END}\n")
    print(f"{Colors.YELLOW}[1] Host a chat{Colors.END}\n")
    print(f"{Colors.YELLOW}[2] Join a chat{Colors.END}\n")
    
    choice = input(f"{Colors.YELLOW}Choose an option: {Colors.END}")
    if choice == '1':
            port = input(f"{Colors.YELLOW}Enter port: {Colors.END}")
            username = input(f"{Colors.YELLOW}Enter username: {Colors.END}")
            start = input(f"{Colors.YELLOW}Start kore chat: {Colors.END}")
            command = f"python3 korechat.py -l -p {port} -u {username}"
    elif choice == '2':
            ip = input(f"{Colors.YELLOW}Enter host IP: {Colors.END}")
            port = input(f"{Colors.YELLOW}Enter host port: {Colors.END}")
            username = input(f"{Colors.YELLOW}Enter username: {Colors.END}")
            command = f"python3 korechat.py -c {ip} -p {port} -u {username}"
    else:
            print(f"{Colors.RED}Invalid choice.{Colors.END}")
            return
    
    print(f"\n{Colors.CYAN}Executing command: {Colors.END}{Colors.GREEN}{command}{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to execute this command? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system(command)
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")


def other_tools_menu():
    """Display Other Tools menu - tools like hydra, etc."""
    while True:
        clear_screen()
        print_banner()
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}OTHER TOOLS{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.GREEN}[1] HYDRA - Password Cracker{Colors.END}")
        print(f"{Colors.GREEN}[2] NMAP - Network Scanner{Colors.END}")
        print(f"{Colors.GREEN}[3] SQLMAP - SQL Injection Tool{Colors.END}")
        print(f"{Colors.GREEN}[4] METASPLOIT - Penetration Testing Framework{Colors.END}")
        print(f"{Colors.GREEN}[5] WIRESHARK - Network Protocol Analyzer{Colors.END}")
        print(f"{Colors.GREEN}[6] JOHN THE RIPPER - Password Cracker{Colors.END}")
        print(f"{Colors.RED}[7] BACK TO MAIN MENU{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
        
        choice = input(f"\n{Colors.YELLOW}Enter your choice (1-7): {Colors.END}")
        
        if choice == '1':
            hydra_tool()
        elif choice == '2':
            nmap_tool()
        elif choice == '3':
            sqlmap_tool()
        elif choice == '4':
            metasploit_tool()
        elif choice == '5':
            wireshark_tool()
        elif choice == '6':
            john_tool()
        elif choice == '7':
            break
        else:
            print(f"{Colors.RED}Invalid choice! Please try again.{Colors.END}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def hydra_tool():
    """Hydra - Password Cracker with user-friendly prompts"""
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}HYDRA - PASSWORD CRACKER{Colors.END}\n")
    
    target = input(f"{Colors.YELLOW}Enter target IP or hostname: {Colors.END}")
    service = input(f"{Colors.YELLOW}Enter service (ssh, ftp, http-post-form, etc.): {Colors.END}")
    username = input(f"{Colors.YELLOW}Enter username (or leave blank for username list): {Colors.END}")
    
    if not username:
        username_file = input(f"{Colors.YELLOW}Enter username file path: {Colors.END}")
        username_option = f"-L {username_file}"
    else:
        username_option = f"-l {username}"
    
    password_file = input(f"{Colors.YELLOW}Enter password file path (e.g., /usr/share/wordlists/rockyou.txt): {Colors.END}")
    port = input(f"{Colors.YELLOW}Enter port (or leave blank for default): {Colors.END}")
    
    command = f"hydra {username_option} -P {password_file} {target} {service}"
    if port:
        command += f" -s {port}"
    
    print(f"\n{Colors.CYAN}Executing command: {Colors.END}{Colors.GREEN}{command}{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to execute this command? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system(command)
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def nmap_tool():
    """NMAP - Network Scanner with user-friendly prompts"""
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}NMAP - NETWORK SCANNER{Colors.END}\n")
    
    target = input(f"{Colors.YELLOW}Enter target IP or hostname: {Colors.END}")
    print(f"{Colors.CYAN}Scan Types:{Colors.END}")
    print(f"{Colors.GREEN}[1] Basic Scan{Colors.END}")
    print(f"{Colors.GREEN}[2] Port Scan{Colors.END}")
    print(f"{Colors.GREEN}[3] Service Version Detection{Colors.END}")
    print(f"{Colors.GREEN}[4] OS Detection{Colors.END}")
    print(f"{Colors.GREEN}[5] Aggressive Scan{Colors.END}")
    
    scan_type = input(f"\n{Colors.YELLOW}Select scan type (1-5): {Colors.END}")
    
    scan_commands = {
        '1': f"nmap {target}",
        '2': f"nmap -p- {target}",
        '3': f"nmap -sV {target}",
        '4': f"nmap -O {target}",
        '5': f"nmap -A {target}"
    }
    
    command = scan_commands.get(scan_type, f"nmap {target}")
    
    print(f"\n{Colors.CYAN}Executing command: {Colors.END}{Colors.GREEN}{command}{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to execute this command? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system(command)
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def sqlmap_tool():
    """SQLMAP - SQL Injection Tool with user-friendly prompts"""
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}SQLMAP - SQL INJECTION TOOL{Colors.END}\n")
    
    url = input(f"{Colors.YELLOW}Enter target URL: {Colors.END}")
    print(f"{Colors.CYAN}Options:{Colors.END}")
    print(f"{Colors.GREEN}[1] Basic Scan{Colors.END}")
    print(f"{Colors.GREEN}[2] Get Databases{Colors.END}")
    print(f"{Colors.GREEN}[3] Get Tables{Colors.END}")
    print(f"{Colors.GREEN}[4] Dump Data{Colors.END}")
    
    option = input(f"\n{Colors.YELLOW}Select option (1-4): {Colors.END}")
    
    commands = {
        '1': f"sqlmap -u {url}",
        '2': f"sqlmap -u {url} --dbs",
        '3': f"sqlmap -u {url} -D <database> --tables",
        '4': f"sqlmap -u {url} -D <database> -T <table> --dump"
    }
    
    command = commands.get(option, f"sqlmap -u {url}")
    
    if option in ['3', '4']:
        print(f"{Colors.YELLOW}Note: Replace <database> and <table> with actual values{Colors.END}")
    
    print(f"\n{Colors.CYAN}Executing command: {Colors.END}{Colors.GREEN}{command}{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to execute this command? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system(command)
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def metasploit_tool():
    """METASPLOIT - Penetration Testing Framework"""
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}METASPLOIT FRAMEWORK{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Metasploit Console will be opened.{Colors.END}")
    print(f"{Colors.CYAN}Common commands:{Colors.END}")
    print(f"{Colors.GREEN}- search <name> : Search for exploits{Colors.END}")
    print(f"{Colors.GREEN}- use <exploit> : Use an exploit{Colors.END}")
    print(f"{Colors.GREEN}- show options : Show exploit options{Colors.END}")
    print(f"{Colors.GREEN}- set <option> <value> : Set option value{Colors.END}")
    print(f"{Colors.GREEN}- exploit : Run the exploit{Colors.END}")
    print(f"{Colors.GREEN}- exit : Exit Metasploit{Colors.END}")
    
    confirm = input(f"\n{Colors.YELLOW}Do you want to open Metasploit Console? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system("msfconsole")
        except Exception as e:
            print(f"{Colors.RED}Error opening Metasploit: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def wireshark_tool():
    """WIRESHARK - Network Protocol Analyzer"""
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}WIRESHARK - NETWORK PROTOCOL ANALYZER{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Wireshark will be opened with GUI.{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to open Wireshark? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system("wireshark")
        except Exception as e:
            print(f"{Colors.RED}Error opening Wireshark: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def john_tool():
    """JOHN THE RIPPER - Password Cracker"""
    clear_screen()
    print_banner()
    print(f"{Colors.MAGENTA}{Colors.BOLD}JOHN THE RIPPER - PASSWORD CRACKER{Colors.END}\n")
    
    password_file = input(f"{Colors.YELLOW}Enter password file path: {Colors.END}")
    wordlist = input(f"{Colors.YELLOW}Enter wordlist path (or leave blank for default): {Colors.END}")
    
    if wordlist:
        command = f"john --wordlist={wordlist} {password_file}"
    else:
        command = f"john {password_file}"
    
    print(f"\n{Colors.CYAN}Executing command: {Colors.END}{Colors.GREEN}{command}{Colors.END}")
    confirm = input(f"\n{Colors.YELLOW}Do you want to execute this command? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            os.system(command)
        except Exception as e:
            print(f"{Colors.RED}Error executing command: {e}{Colors.END}")
    else:
        print(f"{Colors.YELLOW}Command cancelled.{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def youtube_option():
    """Display YouTube subscription information"""
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}SUBSCRIBE TO OUR YOUTUBE CHANNEL{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Channel: @KORECOMMUNITY{Colors.END}")
    print(f"\n{Colors.GREEN}Please subscribe to our YouTube channel for more tools and tutorials!{Colors.END}")
    print(f"{Colors.CYAN}https://youtube.com/@KORECOMMUNITY{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def website_option():
    """Display website information"""
    clear_screen()
    print_banner()
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}OUR WEBSITE{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Website: https://kore.unaux.com{Colors.END}")
    print(f"\n{Colors.GREEN}Visit our website for more tools, resources, and updates!{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}═══════════════════════════════════════════════════════════════{Colors.END}")
    
    confirm = input(f"\n{Colors.YELLOW}Do you want to open the website in browser? (y/n): {Colors.END}")
    
    if confirm.lower() == 'y':
        try:
            import webbrowser
            webbrowser.open("https://kore.unaux.com")
        except Exception as e:
            print(f"{Colors.RED}Error opening website: {e}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")

def main():
    """Main function to run the tool"""
    try:
        home_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN}Thank you for using KORE TOOL! Goodbye!{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}An error occurred: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
