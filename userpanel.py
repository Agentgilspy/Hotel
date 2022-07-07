import os
from database import *
from tabulate import tabulate
from datetime import datetime
from random import randint

def userpanel():
    
    while True:
        print('\n')
        print('Welcome to the Paradise               \n')
        print("""
1)Make a Reservation
2)CheckIn
3)Checkout
4)Back
""")
        ch=int(input('Enter choice:'))
        os.system('cls')

        if ch==1:
            cs.execute('select* from packages')
            r=cs.fetchall()
            print('Hotel name Packages \n\n')
            print(tabulate(r , headers=['PkCode' , "People" , 'Room Type' , 'Package Details', 'Cost Per Night' , 'Tourism']))
            print('\n\n')
            
            pkchoice=int(input("Select the package:"))
            os.system('cls')         

            cs.execute("select* from packages where pk_code=%s"%(pkchoice))
            r=cs.fetchall()
            package=r[0]
            pkcode,_,_,_,cost,tourism=package 
            print(f'Package {pkchoice} selected')
            checkIn=input('Enter Check in Date(yyyy/mm/dd):')
            checkOut=input('Enter Check Out Date(yyyy/mm/dd):')
            checkin_d = datetime.strptime(checkIn, '%Y/%m/%d') 
            checkout_d = datetime.strptime(checkOut, '%Y/%m/%d')
            days = (checkout_d - checkin_d).days
            if days<0:
                print('Invalid Dates Provided')
                continue
        
            fname=input('Enter first name:')
            lname=input('Enter last name:')
            ph=input("Enter phone number:")
            cost*=days
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


        elif ch==2:
            phonenum=input('Enter Phone Number:')
            cs.execute('select * from reservations where Phone_Number="%s"'%(phonenum))
            result=cs.fetchall()

            reservation=result[0]
            rid,gid,Pkcode,_,CheckIn,Checkout,_,RoomNo,Expenses = reservation
            if RoomNo!=None:
                print('You have already CheckedIn')
                continue
            cs.execute('select * from packages where Pk_code=%s'%(Pkcode))
            package=cs.fetchall()[0]
            RoomType=package[2]
            cs.execute('select RoomNo,Floor,Status,Type from Rooms where Type="%s" and Status="Vacant"'%(RoomType))
            rooms=cs.fetchall()
            print('\n')            
            print('\t Available Rooms \t')
            print('\n')
            print(tabulate(rooms,headers=['RoomNo','Floor','Status','Type']))
            print('\n')
            roomchoice=int(input('Enter room number:'))
            cs.execute('select * from Rooms where RoomNo=%s and Status="Vacant" and Type="%s"'
            %(roomchoice,RoomType))
            selected=cs.fetchall()
            if len(selected)==0:
                print('Room not Availaible')
                break;

            cs.execute('update Rooms set Status="Occupied",ReservationID=%s where RoomNo=%s'%(rid,roomchoice))
            cs.execute('update guests set RoomNo=%s where Guest_ID=%s' %(roomchoice,gid))
            cs.execute('update reservations set RoomNo=%s where Reservation_ID=%s'%(roomchoice,rid))
            db.commit()
            print()
            print('Successfully CheckedIn Enjoy your stay')

        elif ch==3:
            phonenum=input('Enter Phone Number:')
            cs.execute('select * from reservations where Phone_Number="%s"'%(phonenum))
            result=cs.fetchall()
            if(len(result)==0):
                print('Invalid Phone Number')
                continue
            reservation=result[0]
            rid,gid,Pkcode,_,CheckIn,Checkout,_,RoomNo,Expenses = reservation
            if RoomNo=='Not CheckedIn':
                print('You cannot CheckOut')
                continue

            cs.execute('select First_Name,Last_Name from Guests where Phone_Number="%s"'%(phonenum))
            fname,lname=cs.fetchall()[0]

            score=int(input('On a scale of 1-10 how would you rate your stay %s:'%(fname)))
            comments=input('Anything You want to say about your stay?\n')
            cs.execute('update Rooms set Status="Cleaning",ReservationID=NULL where RoomNo=%s'%(RoomNo))
            cs.execute('update Guests set RoomNo=Null where Guest_ID=%s'%(gid))
            cs.execute('delete from reservations where Reservation_ID=%s'%(rid))
            cs.execute(f'insert into history values({gid},"{fname}","{lname}","{phonenum}",{Expenses},"{CheckIn}","{Checkout}",{score},"{comments}")')
            db.commit()

            print()
            print('Checkout Successful')
        elif ch==4:
            break

