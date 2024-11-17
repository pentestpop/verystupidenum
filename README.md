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

1. (user/password)
   1. `nxc smb $IP -u $user -p $password`
   2. -
2. (user/passwordlist)
   1. `nxc smb $IP -u $user -p $passwordlist`
   2. -
3. (userlist/password)
   1. `kerbrute passwordspray -d $domain $userlist $password`
   2. - 
4. (userlist/passwordlist)
   1. `smbclient -L \\$domain -I $IP -N`
  
It could not be easier, and frankly it shouldn't be this easy. 
