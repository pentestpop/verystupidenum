import subprocess

# Get user input
domain = input("Enter the domain: ")
user = input("Enter the username: ")
password = input("Enter the password: ")
ip = input("Enter the IP address: ")

# Construct the commands
command1 = f"impacket-GetUserSPNs {domain}/{user}:'{password}' -dc-ip {ip}"
command2 = f"impacket-GetNPUsers {domain}/{user}:'{password}' -dc-ip {ip}"

# Run the commands
subprocess.run(command1, shell=True)
subprocess.run(command2, shell=True)
