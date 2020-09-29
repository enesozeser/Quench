#!/bin/bash
wget https://raw.githubusercontent.com/enesozeser/Quench/master/quench.py
mv quench.py quench
chmod a+x quench
cp quench /usr/local/bin/
mv quench quench.py
apt update && apt install python3 -y
sleep 2
echo "Quench has been installed. Use 'quench' command for all information."
