#!/bin/bash
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'
mv quench.py quench
chmod a+x quench
cp quench /usr/bin/
mv quench quench.py
apt install python3 -y
sleep 5
printf "${YELLOW}Quench has been installed. Use '${GREEN}quench -h${YELLOW}' command for all information.\n"
printf "${NC}"
