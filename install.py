#!/usr/bin/env python
import os
import time

print("Quench is installing...")
os.system('mv quench.py quench')
os.system('chmod a+x quench')
os.system('cp quench /usr/bin/')
os.system('mv quench quench.py')
time.sleep(5)
print("Quench has been installed. Use 'quench -h' command for all information.")
