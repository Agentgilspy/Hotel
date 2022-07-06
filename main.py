#Importing modules

import os
from database import *
from userpanel import *

startup()
while True:
    os.system('cls')
    print('\n\n')
    print('Welcome to Hotel Name')
    print("""
1)Staff
2)User
""")
    ch=int(input('Enter choice:'))
    os.system('cls')
    if ch==2:

        userpanel()