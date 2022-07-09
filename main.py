#Importing modules

import os
from database import *
from userpanel import *
from staffpanel import *

startup()
while True:
    os.system('cls')
    print("\n1)Staff")
    print("2)User\n")
    ch=int(input('Enter choice:'))
    os.system('cls')
    if ch==1:
        staffpanel()
    elif ch==2:
        userpanel()