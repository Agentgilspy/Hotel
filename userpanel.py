import os
from database import *
from tabulate import tabulate
from datetime import datetime
from random import randint


def createReservation():
    cs.execute('select * from packages')
    r=cs.fetchall()
    print('\n\t\t\t\t\tPackages \n\n')
    print(tabulate(r , headers=['PkCode' , "People" , 'Room Type' , 'Package Details', 'Cost Per Night' , 'Tourism'],tablefmt='fancy_grid'))
    print('\n\n')
    
    pkchoice=int(input("Select the package:"))
    os.system('cls')         

    cs.execute(f"select* from packages where pk_code={pkchoice}")
    r=cs.fetchall()
    package=r[0]
    pkcode,_,room_type,pk_type,rate,tourism=package 
    print(f'Package {pkchoice} selected')
    checkIn=input('Enter Check in Date(yyyy/mm/dd):')
    checkOut=input('Enter Check Out Date(yyyy/mm/dd):')
    checkin_d = datetime.strptime(checkIn, '%Y/%m/%d').date()
    checkout_d = datetime.strptime(checkOut, '%Y/%m/%d').date()
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
    cs.execute(f"insert into reservations values({rid},{guestid},{pkchoice},'{ph}','{checkin_d}','{checkout_d}',{days},Null,{cost})")
    cs.execute(f"insert into Guests values({guestid},{rid},'{fname}','{lname}','{ph}',Null)")
    db.commit()
    print('Reservation Made')
    print('\n=======================================')
    print('\t\t Receipt\n\n')
    print(f' Name:{fname} {lname}')
    print(f' Phone Number: {ph}')
    print(f' Reservation ID: {rid}')
    print(f' CheckInDate: {checkin_d}')
    print(f' Checkout Date: {checkout_d}')
    print(f' Days: {days}')
    print(f' Package Type : {pk_type}')
    print(f' Room Type : {room_type}')     
    print(f' Expenses: {cost} AED')
    print('\n======================================')


def checkIn():
    phonenum=input('Enter Phone Number:')
    cs.execute(f'select * from reservations where Phone_Number="{phonenum}"')
    result=cs.fetchall()

    reservation=result[0]
    rid,gid,Pkcode,_,CheckIn,Checkout,_,RoomNo,Expenses = reservation
    if RoomNo!=None:
        print('You have already checked in')
        return
    cs.execute(f'select * from packages where Pk_code={Pkcode}')
    package=cs.fetchall()[0]
    RoomType=package[2]
    cs.execute(f'select RoomNo,Floor,Status,Type from Rooms where Type="{RoomType}" and Status="Vacant"')
    rooms=cs.fetchall()
    print('\n')            
    print('\t Available Rooms \t')
    print('\n')
    print(tabulate(rooms,headers=['RoomNo','Floor','Status','Type'],tablefmt='fancy_grid'))
    print('\n')
    roomchoice=int(input('Enter room number:'))
    cs.execute(f'select * from Rooms where RoomNo={roomchoice} and Status="Vacant" and Type="{RoomType}"')
    selected=cs.fetchall()
    if len(selected)==0:
        print('Room not Availaible')
        return;

    cs.execute(f'update Rooms set Status="Occupied",ReservationID={rid} where RoomNo={roomchoice}')
    cs.execute(f'update guests set RoomNo={roomchoice} where Guest_ID={gid}')
    cs.execute(f'update reservations set RoomNo={roomchoice} where Reservation_ID={rid}')
    db.commit()
    print()
    print('Successfully checked in Enjoy your stay\n')
    #Receipt
    cs.execute(f'select * from Guests where Guest_ID={gid}')
    guest=cs.fetchall()[0]
    _,_,fname,lname,_,_=guest
    print('Receipt\n')
    print(f'Name:{fname} {lname}')
    print(f'Phone Number:{phonenum}')
    print(f'ReservationID:{rid}')
    print(f'RoomNo:{roomchoice}')    
def checkOut():
    phonenum=input('Enter Phone Number:')
    cs.execute(f'select * from reservations where Phone_Number="{phonenum}"')
    result=cs.fetchall()
    if(len(result)==0):
        print('Invalid Phone Number')
        return
    reservation=result[0]
    rid,gid,Pkcode,_,CheckIn,Checkout,_,RoomNo,Expenses = reservation
    if RoomNo=='Not CheckedIn':
        print('You cannot CheckOut')
        return

    cs.execute(f'select First_Name,Last_Name from Guests where Phone_Number="{phonenum}"')
    fname,lname=cs.fetchall()[0]

    score=int(input(f'On a scale of 1-10 how would you rate your stay {fname}:'))
    if score<1 or score>10:
        print('Invalid Score')
        return
    comments=input('Anything You want to say about your stay?\n')
    cs.execute(f'update Rooms set Status="Cleaning",ReservationID=NULL where RoomNo={RoomNo}')
    cs.execute(f'delete from Guests where Guest_ID={gid}')
    cs.execute(f'delete from reservations where Reservation_ID={rid}')
    cs.execute(f'insert into history values("{fname}","{lname}","{phonenum}",{Pkcode},{Expenses},"{CheckIn}","{Checkout}",{score},"{comments}")')
    db.commit()

    print()
    print('Checkout Successful')
def userpanel():
    
    while True:
        print('')
        print('Welcome to The Paradise\n')
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

