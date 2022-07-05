#Importing modules

import os
from tabulate import tabulate
from tkinter import *
from startup import *

from datetime import datetime
from random import randint
checkin_d = datetime.strptime("2005/07/23", '%Y/%m/%d') # Get the date from user input
checkout_d= datetime.strptime("2005/07/23", '%Y/%m/%d') 



guestid = 10000 + randint(0, 9999)


def reservation():
    cs.execute('select* from packages')
    r=cs.fetchall()
    print(tabulate(r , headers=['PkCode' , "People" , 'Room Type' , 'Package Details', 'Cost Per Night' , 'Tourism']))

    pkchoice=int(input("Select the package:"))
    cs.execute("select* from packages where pk_code=%s"%(pkchoice))
    r=cs.fetchall()
   


reservation()