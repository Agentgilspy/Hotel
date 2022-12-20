#Importing modules

import os
from database import *
from userpanel import *
from staffpanel import *
import maskpass
import time

startup()
while True:
    os.system('cls')
    print('The Paradise')
    print("\n1)Admin")
    print("2)User\n")
    ch=int(input('Enter choice:'))
    os.system('cls')
    if ch==1:
        pwd=maskpass.askpass('Enter Password:')
        if pwd=='123':
            staffpanel()
        else:
            print('Wrong Password')
            time.sleep(2)
    elif ch==2:
        userpanel()