#!/usr/bin/python3
import argparse
import subprocess
import sys
from datetime import datetime
import os
import time
import threading

def rgb_to_ansi(hex_color):
    # Convert hex color to RGB
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"\033[38;2;{r};{g};{b}m"

def print_title():
    # Pink color (F686BD)
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    
    title = f"""{pink}
 _,   _            __,                             
( |  /            (    _/_          o    /         
  | /_  _   __  ,  `.  /  , ,  ,_  ,  __/          
  |/(/_/ (_/ (_/_(___)(__(_/__/|_)_(_(_/_          
              /               /|                   
             '               (/                    
 ______                                            
(  /                                  _/_o         
  /--   _ _   , , _ _ _   _  _   __,  / ,  __ _ _  
(/____// / /_(_/_/ / / /_(/_/ (_(_/(_(__(_(_)/ / /_
{reset}"""
    print(title)
    print("\n" + "="*60)
    print(" "*20 + "Starting Enumeration...")
    print("="*60 + "\n")

def loading_animation():
    frames = [
        """
        ⠋
        """,
        """
        ⠙
        """,
        """
        ⠹
        """,
        """
        ⠸
        """,
        """
        ⠼
        """,
        """
        ⠴
        """,
        """
        ⠦
        """,
        """
        ⠧
        """,
        """
        ⠇
        """,
        """
        ⠏
        """
    ]
    return frames

def animate(stop):
    frames = loading_animation()
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    while not stop.is_set():
        for frame in frames:
            if stop.is_set():
                break
            sys.stdout.write(f'\r{pink}{frame}{reset}')
            sys.stdout.flush()
            time.sleep(0.1)

def setup_logging(domain, ip):
    """Setup logging directory and file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "enum_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = f"{log_dir}/enum_{domain}_{ip}_{timestamp}.log"
    return log_file

def log_command(log_file, command, output):
    """Log command and its output to file"""
    with open(log_file, 'a') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Command: {command}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n")
        f.write(output)
        f.write("\n")

def run_command(command, log_file, stop_animation):
    """Execute command and log output"""
    try:
        pink = rgb_to_ansi("F686BD")
        reset = "\033[0m"
        print(f"\n{pink}[*] Running: {reset}{command}")
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()
        
        # Combine stdout and stderr for logging
        full_output = output + error
        log_command(log_file, command, full_output)
        
        print(f"{pink}[+] Command completed. Output saved to {reset}{log_file}")
        return True
    except Exception as e:
        print(f"{pink}[-] Error executing command: {reset}{e}")
        log_command(log_file, command, f"Error: {str(e)}")
        return False
    finally:
        stop_animation.set()

def prompt_for_input():
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    print(f"\n{pink}[*] Please provide the following information, assuming you can even read:{reset}")
    
    # Required inputs
    domain = input(f"{pink}Domain (required): {reset}").strip()
    while not domain:
        print(f"{pink}Domain is required dumbass!{reset}")
        domain = input(f"{pink}Domain (required): {reset}").strip()
    
    ip = input(f"{pink}IP Address (required): {reset}").strip()
    while not ip:
        print(f"{pink}IP Address is required dumbass!{reset}")
        ip = input(f"{pink}IP Address (required): {reset}").strip()
    
    # Optional DC-IP
    dc_ip = input(f"{pink}DC-IP (optional, press Enter to skip): {reset}").strip()
    
    # User authentication
    print(f"\n{pink}User Authentication (choose one idiot):{reset}")
    print(f"{pink}1. Single valid username{reset}")
    print(f"{pink}2. User list file{reset}")
    user_choice = input(f"{pink}Enter choice (1/2): {reset}").strip()
    
    username = None
    userlist = None
    while user_choice not in ['1', '2']:
        user_choice = input(f"{pink}Please enter 1 or 2: {reset}").strip()
    
    if user_choice == '1':
        username = input(f"{pink}Username: {reset}").strip()
        while not username:
            username = input(f"{pink}Username cannot be empty: {reset}").strip()
    else:
        userlist = input(f"{pink}Path to user list file: {reset}").strip()
        while not userlist or not os.path.exists(userlist):
            userlist = input(f"{pink}Please enter a valid file path: {reset}").strip()
    
    # Password authentication
    print(f"\n{pink}Password Authentication (pick one doofus):{reset}")
    print(f"{pink}1. Single valid password{reset}")
    print(f"{pink}2. Password list file{reset}")
    pass_choice = input(f"{pink}Enter choice (1/2): {reset}").strip()
    
    password = None
    passwordlist = None
    while pass_choice not in ['1', '2']:
        pass_choice = input(f"{pink}Please enter 1 or 2: {reset}").strip()
    
    if pass_choice == '1':
        password = input(f"{pink}Password: {reset}").strip()
        while not password:
            password = input(f"{pink}Password cannot be empty: {reset}").strip()
    else:
        passwordlist = input(f"{pink}Path to password list file: {reset}").strip()
        while not passwordlist or not os.path.exists(passwordlist):
            passwordlist = input(f"{pink}Please enter a valid file path: {reset}").strip()
    
    return {
        'domain': domain,
        'ip': ip,
        'dc_ip': dc_ip,
        'username': username,
        'userlist': userlist,
        'password': password,
        'passwordlist': passwordlist
    }

def main():
    print_title()
    inputs = prompt_for_input()
    
    # Setup logging
    log_file = setup_logging(inputs['domain'], inputs['ip'])
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    print(f"\n{pink}[*] Starting enumeration. Log file: {reset}{log_file}")
    
    # Setup animation stop event
    stop_animation = threading.Event()
    
    # Determine scenario and run appropriate commands
    if inputs['username'] and inputs['password']:
        # Scenario 1: Single username and password
        animation_thread = threading.Thread(target=animate, args=(stop_animation,))
        animation_thread.start()
        
        command = f"nxc smb {inputs['ip']} -u {inputs['username']} -p {inputs['password']}"
        run_command(command, log_file, stop_animation)
        
    elif inputs['username'] and inputs['passwordlist']:
        # Scenario 2: Single username with password list
        animation_thread = threading.Thread(target=animate, args=(stop_animation,))
        animation_thread.start()
        
        command = f"nxc smb {inputs['ip']} -u {inputs['username']} -p {inputs['passwordlist']}"
        run_command(command, log_file, stop_animation)
        
    elif inputs['userlist'] and inputs['password']:
        # Scenario 3: User list with single password
        animation_thread = threading.Thread(target=animate, args=(stop_animation,))
        animation_thread.start()
        
        command = f"kerbrute passwordspray -d {inputs['domain']} {inputs['userlist']} {inputs['password']}"
        run_command(command, log_file, stop_animation)
        
    elif inputs['userlist'] and inputs['passwordlist']:
        # Scenario 4: User list with password list
        animation_thread = threading.Thread(target=animate, args=(stop_animation,))
        animation_thread.start()
        
        command = f"kerbrute userenum -d {inputs['domain']} {inputs['userlist']}"
        run_command(command, log_file, stop_animation)
    
    print(f"\n{pink}[*] Enumeration completed!{reset}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Script terminated by user")
        sys.exit(0)
