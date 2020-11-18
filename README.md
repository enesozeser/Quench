## Quench - The Reverse Shell Payload Generator
- Quench is a reverse shell payload generator for penetration testers. It developed to automate the process of generating various reverse shell payloads.
<p align="center">
  <a href="https://enesozeser.com/quench.mp4"><img src="https://i.imgur.com/g4K9kGZ.png" width="700" height="375"></a>
</p>

## Supported Payload Types
- Bash
- Perl
- Python
- Socat
- PHP
- Ruby
- Netcat
- Golang
- AWK
- Lua
- PowerShell

## Installation
```
$ git clone https://github.com/enesozeser/Quench.git
$ cd Quench
$ chmod +x quench.py
$ ./quench.py
```

## Arguments & Usage
```
Arguments:
  -i, --ip ==> IP Address
  -p, --port ==> Port Number
  -t, --type ==> Payload Type
  --update ==> Update To The Latest Version
  --install ==> Install To '/usr/local/bin/' Directory
Usage:
  quench -i <IP Address> -p <Port Number> -t <Payload Type>
  quench -i 127.0.0.1 -p 4444 -t php
  quench --ip 192.168.1.1 --port 1337 --type awk
  quench --update
  quench --install
```
