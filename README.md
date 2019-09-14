# insydys
insydys is an easy to use python based exploitation set that extends capabities which are included in frameworks such as Metasploit 

**Features**

Reverse shell

keystrokes extractor

Remote file encryption and decryption(crypto)

Screenshot extractor

Remote webcam access

Remote microphone access

Grab files

upload files

**Getting Started**

On running the server file 3 options are displayed.Option 1 allows you  to setup a listener immediately,
option 2 generates the executable and quits, option 3 generates the payload and starts the listener.
after the connection has been established a list of commands is displayed on default commands not included on the list are executed as shell commands for target machine.

The payloads generated are native to the operating system used to generate it. 

On opening the payload it runs persistently in the background unless the machine is turned off or its processes are terminated from the process list.

The keylogger is persistent too and captured keystrokes are retrieved using the 'keylog' command

The vidcap- enables you record the target machines webcam or connected camera device

The audcap-command records the target machines microphone 

Grab - enables retrieval of files and folders from target machine

upload - enables dropping of a file on target

encrypt - utilizes AES encryption  to encrypt files and folders chosen

decrypt-decryption of the AES encrypted files

keys -displays a list of saved keys for encryption and decryption and the name of files they were used on

sysinfo -displays information about the target machine

help/options-displays a list of commands



