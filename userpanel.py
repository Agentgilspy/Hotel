import os
from database import *
from tabulate import tabulate
from datetime import datetime
from random import randint


def createReservation():
    cs.execute('select* from packages')
    r=cs.fetchall()
    print('Hotel name Packages \n\n')
    print(tabulate(r , headers=['PkCode' , "People" , 'Room Type' , 'Package Details', 'Cost Per Night' , 'Tourism'],tablefmt='fancy_grid'))
    print('\n\n')
    
    pkchoice=int(input("Select the package:"))
    os.system('cls')         

    cs.execute("select* from packages where pk_code=%s"%(pkchoice))
    r=cs.fetchall()
    package=r[0]
    pkcode,_,_,_,rate,tourism=package 
    print(f'Package {pkchoice} selected')
    checkIn=input('Enter Check in Date(yyyy/mm/dd):')
    checkOut=input('Enter Check Out Date(yyyy/mm/dd):')
    checkin_d = datetime.strptime(checkIn, '%Y/%m/%d') 
    checkout_d = datetime.strptime(checkOut, '%Y/%m/%d')
    days = (checkout_d - checkin_d).days
    if days<0:
        print('Invalid Dates Provided')
        return

    fname=input('Enter first name:')
    lname=input('Enter last name:')
    ph=input("Enter phone number:")
    cost=rate*days
    torsm=input("Do you want tourism(y/n):")
    if torsm=='y':
        cost+=tourism
    
    guestid=1000000+randint(0,99999)
    rid=10000+randint(0,9999)           
    
    cs.execute("insert into reservations values(%s,%s,%s,'%s','%s','%s',%s,%s,%s)"
    %(rid,guestid,pkchoice,ph,checkin_d,checkout_d,days,"NULL",cost))
    cs.execute("insert into Guests values(%s,%s,'%s','%s','%s',Null)"
    %(guestid,rid,fname,lname,ph))
    db.commit()
    print('Reservation Made')
def checkIn():
    phonenum=input('Enter Phone Number:')
    cs.execute('select * from reservations where Phone_Number="%s"'%(phonenum))
    result=cs.fetchall()

    reservation=result[0]
    rid,gid,Pkcode,_,CheckIn,Checkout,_,RoomNo,Expenses = reservation
    if RoomNo!=None:
        print('You have already CheckedIn')
        return
    cs.execute('select * from packages where Pk_code=%s'%(Pkcode))
    package=cs.fetchall()[0]
    RoomType=package[2]
    cs.execute('select RoomNo,Floor,Status,Type from Rooms where Type="%s" and Status="Vacant"'%(RoomType))
    rooms=cs.fetchall()
    print('\n')            
    print('\t Available Rooms \t')
    print('\n')
    print(tabulate(rooms,headers=['RoomNo','Floor','Status','Type'],tablefmt='fancy_grid'))
    print('\n')
    roomchoice=int(input('Enter room number:'))
    cs.execute('select * from Rooms where RoomNo=%s and Status="Vacant" and Type="%s"'
    %(roomchoice,RoomType))
    selected=cs.fetchall()
    if len(selected)==0:
        print('Room not Availaible')
        return;

    cs.execute('update Rooms set Status="Occupied",ReservationID=%s where RoomNo=%s'%(rid,roomchoice))
    cs.execute('update guests set RoomNo=%s where Guest_ID=%s' %(roomchoice,gid))
    cs.execute('update reservations set RoomNo=%s where Reservation_ID=%s'%(roomchoice,rid))
    db.commit()
    print()
    print('Successfully CheckedIn Enjoy your stay\n')
    #Receipt
    cs.execute('select * from Guests where Guest_ID=%s'%(gid))
    guest=cs.fetchall()[0]
    _,_,fname,lname,_,_=guest
    print('Receipt\n')
    print('Name:%s %s'%(fname,lname))
    print('Phone Number:%s'%(phonenum))
    print('ReservationID:%s'%(rid))
    print('RoomNo:%s'%(roomchoice))    
def checkOut():
    phonenum=input('Enter Phone Number:')
    cs.execute('select * from reservations where Phone_Number="%s"'%(phonenum))
    result=cs.fetchall()
    if(len(result)==0):
        print('Invalid Phone Number')
        return
    reservation=result[0]
    rid,gid,Pkcode,_,CheckIn,Checkout,_,RoomNo,Expenses = reservation
    if RoomNo=='Not CheckedIn':
        print('You cannot CheckOut')
        return

    cs.execute('select First_Name,Last_Name from Guests where Phone_Number="%s"'%(phonenum))
    fname,lname=cs.fetchall()[0]

    score=int(input('On a scale of 1-10 how would you rate your stay %s:'%(fname)))
    if score<1 or score>10:
        print('Invalid Score')
        return
    comments=input('Anything You want to say about your stay?\n')
    cs.execute('update Rooms set Status="Cleaning",ReservationID=NULL where RoomNo=%s'%(RoomNo))
    cs.execute('delete from Guests where Guest_ID=%s'%(gid))
    cs.execute('delete from reservations where Reservation_ID=%s'%(rid))
    cs.execute(f'insert into history values("{fname}","{lname}","{phonenum}",{Pkcode},{Expenses},"{CheckIn}","{Checkout}",{score},"{comments}")')
    db.commit()

    print()
    print('Checkout Successful')
def userpanel():
    
    while True:
        print('\n')
        print('Welcome to the Paradise\n')
        print("""
1)Make a Reservation
2)CheckIn
3)Checkout
4)Back
""")
        ch=int(input('Enter choice:'))
        os.system('cls')

        if ch==1:
            createReservation()
        elif ch==2:
            checkIn()
        elif ch==3:
            checkOut()
        elif ch==4:
            break

