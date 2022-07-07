from database import *
import os
from tabulate import tabulate
from datetime import datetime

def manageEmployees():
    while True:
        print('\nEmployee Management\n')
        print("1)View all Employees")
        print("2)Add an employee")
        print("3)Fire an Employee")
        print("4)Update Employee Details")
        print("5)Back\n")
            
        ch=int(input('Enter choice:'))
        print()
        if ch==1:
            cs.execute('select * from employees')
            result=cs.fetchall()
            print(tabulate(result , headers=['Empcode','Name','Designation','Salary','Date of join']))
        
        elif ch==2:
            empcode=int(input('Enter empcode:'))
            name=input('Enter name:')
            des=input('Enter designation:')
            sal=int(input('Enter salary:'))
            doj=input('Enter date of join(yyyy/mm/dd):')
            doj=datetime.strptime(doj, '%Y/%m/%d')
            cs.execute('insert into employees values(%s,"%s","%s",%s,"%s")'%(empcode,name,des,sal,doj))
            db.commit() 
            print('\nEmployee Added')

        elif ch==3:
            empcode=int(input('Enter empcode:'))
            cs.execute('delete from employees where empcode=%s'%(empcode))
            db.commit()
            print('\nEmployee Fired')

        elif ch==4:
            empcode=int(input('Enter empcode:'))
            des=input('Enter new designation:')
            sal=int(input('Enter new salary:'))
            cs.execute('update employees set salary=%s,designation="%s" where empcode=%s'%(sal,des,empcode))
            db.commit()
            print('\nEmployee Details Updated')
        elif ch==5:
            break

def manageReservations():
    while True:
        print('\nReservation Management\n')
        print('1)View all Reservations')
        print('2)Delete a Reservation')
        print('3)Back\n')

        ch=int(input('Enter choice:'))
        print()

        if ch==1:
            cs.execute("select Reservation_ID,Guest_ID,PkCode,Phone_Number,CheckIn,Checkout,Nights,Case When RoomNo is null then 'Not CheckedIn' else RoomNo end as 'RoomNo' ,Expenses from reservations")
            result=cs.fetchall()
            print(tabulate(result ,
                headers=['Reservation ID','Guest ID','PkCode','Phone Number','CheckIn','CheckOut','Nights','RoomNo','Expenses']))
        elif ch==2:
            rid=int(input('Enter ReservationID:'))
            cs.execute('delete from reservations where Reservation_ID=%s'%(rid))
            db.commit()
            print('\n Reservation Deleted')
        elif ch==3:
            break

def manageGuests():
    while True:
        print('\nGuest Management\n')
        print('1)View All Guests')
        print('2)View all Guests In the Hotel')
        print('3)Delete Guest Details')

        ch=int(input('Enter choice:'))
def staffpanel():
    while True:
        os.system('cls')
        print('\n1)Manage Employees')
        print('2)Manage Reservations')
        print('3)Manage Guests')
        print('4)Manage Rooms')
        print('5)Back\n')

        ch=int(input('Enter choice:'))
        os.system('cls')
        if ch==1:
            manageEmployees()
        elif ch==2:
            manageReservations()
        elif ch==3:
            manageGuests()
        elif ch==5:
            break