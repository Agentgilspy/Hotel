from database import *
import os
from tabulate import tabulate
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd 

def manageReservations():
    while True:
        print('\nReservation Management\n')
        print('1)View all Reservations')
        print('2)Delete a Reservation')
        print('3)Back\n')

        ch=int(input('Enter choice:'))
        print()
        os.system('cls')

        if ch==1:
            cs.execute("select Reservation_ID,Guest_ID,PkCode,Phone_Number,CheckIn,Checkout,Nights,Case When RoomNo is null then 'Not CheckedIn' else RoomNo end as 'RoomNo' ,Expenses from reservations")
            result=cs.fetchall()
            print(tabulate(result ,
                headers=['Reservation ID','Guest ID','PkCode','Phone Number','CheckIn','CheckOut','Nights','RoomNo','Expenses'],tablefmt='fancy_grid'))
        elif ch==2:
            rid=int(input('Enter ReservationID:'))
            cs.execute(f'delete from reservations where Reservation_ID={rid}')
            db.commit()
            print('\n Reservation Deleted')
        elif ch==3:
            break

def manageGuests():
    while True:
        print('\nGuest Management\n')
        print('1)View All Guests')
        print('2)View all Guests In the Hotel')
        print('3)Back')

        ch=int(input('Enter choice:'))
        print()
        os.system('cls')

        if ch==1:
            cs.execute("select Guest_ID,Reservation_ID,First_Name,Last_Name,Phone_Number,Case When RoomNo is null then 'Not CheckedIn' else RoomNo end as 'RoomNo' from Guests")
            result=cs.fetchall()
            print(tabulate(result,
            headers=['GuestID','ReservationID','First Name','Last Name','Phone Number','RoomNo'],tablefmt='fancy_grid'))
        elif ch==2:
            cs.execute('select * from Guests where RoomNo is not null')
            result=cs.fetchall()
            print(tabulate(result,
            headers=['GuestID','ReservationID','First Name','Last Name','Phone Number','RoomNo'],tablefmt='fancy_grid'))

        elif ch==3:
            break

def manageRooms():
    while True:
        print('\nRoom Management\n')
        print('1)View all Rooms')
        print('2)View all Vacant Rooms')
        print('3)View all Occupied Rooms')
        print('4)View all Rooms with Cleaning Status')
        print('5)Change Room Status')
        print('6)Back')

        ch=int(input('Enter choice:'))
        print()
        os.system('cls')

        if ch==1:
            cs.execute("select RoomNo,Floor,Status,Type,Case When ReservationID is null then 'Not Reserved' else ReservationID End as ReservationID from Rooms")
            result=cs.fetchall()
            print(tabulate(result,
            headers=['RoomNo','Floor','Status','Type','ReservationID'],tablefmt='fancy_grid'))
        elif ch==2:
            cs.execute("select RoomNo,Floor,Status,Type from Rooms where Status='Vacant'")
            result=cs.fetchall()
            print(tabulate(result,
            headers=['RoomNo','Floor','Status','Type'],tablefmt='fancy_grid'))
        elif ch==3:
            cs.execute("select * from Rooms where Status='Occupied'")
            result=cs.fetchall()
            print(tabulate(result,
            headers=['RoomNo','Floor','Type','ReservationID'],tablefmt='fancy_grid'))
        elif ch==4:
            cs.execute("select RoomNo,Floor,Type from Rooms where Status='Cleaning'")
            result=cs.fetchall()
            print(tabulate(result,
            headers=['RoomNo','Floor','Type'],tablefmt='fancy_grid'))
        elif ch==5:
            room=int(input('Enter Room Number:'))
            status=input('Enter status(Cleaning/Vacant):')
            cs.execute(f'update rooms set status="{status}" where RoomNo={room}')
            db.commit()
            cs.execute(f'select RoomNo,Floor,Status,Type from rooms where roomno={room}')
            result=cs.fetchall()
            print(tabulate(result,tablefmt='fancy_grid',headers=['RoomNo','Floor','Status','Type']))
        elif ch==6:
            break

def dataAnalysis():
    while True:
        print('\nData Analysis\n')
        print('1)Plot Bar Graph of Feedbacks (Pkcodes/Feedback)')
        print('2)Plot Bar Graph of Visits (Month/Visits)')
        print('3)Create a xlsx file of Visitor History')
        print('4)Back')

        ch=int(input('Enter choice:'))
        os.system('cls')

        if ch==1:
            cs.execute('select Pk_code,avg(feedback) from history group by Pk_code order by Pk_code')
            result=cs.fetchall()
            pkcodes=[str(row[0]) for row in result]
            scores=[row[1] for row in result]
            plt.bar(pkcodes,scores)
            plt.title('Average Feedback Score')
            plt.xlabel('Package Code')
            plt.ylabel('Score')
            plt.show()
        elif ch==2:
            cs.execute('select month(CheckIn),Count(Checkin) from history group by month(CheckIn) order by month(CheckIn);')
            result=cs.fetchall()
            months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
            visits=[0,0,0,0,0,0,0,0,0,0,0,0,]
            for row in result:
                month=row[0]
                count=row[1]
                visits[month-1]=count
            plt.bar(months,visits)
            plt.title('Visits')
            plt.xlabel('Month')
            plt.ylabel('Visits')
            plt.show()
        elif ch==3:
            cs.execute('select * from history')
            result=cs.fetchall()
            data={
                "First Name" :[row[0] for row in result],
                "Last Name" : [row[1] for row in result],
                "Phone Number" : [row[2] for row in result],
                "Pk_Code":[row[3] for row in result],
                "Expenses" :[row[4] for row in result],
                "CheckIn":[row[5] for row in result],
                "Checkout":[row[6] for row in result],
                "Feedback":[row[7] for row in result],
                "Comments" :[row[8] for row in result]
            }
            dt=pd.DataFrame(data)
            dt.to_excel('Visitors.xlsx',index=False)
            os.system('Visitors.xlsx')
        elif ch==4:
            break

def staffpanel():
    while True:
        os.system('cls')
        print('\n1)Manage Reservations')
        print('2)Manage Guests')
        print('3)Manage Rooms')
        print('4)Data Analysis')
        print('5)Back\n')

        ch=int(input('Enter choice:'))
        os.system('cls')
        if ch==1:
            manageReservations()
        elif ch==2:
            manageGuests()
        elif ch==3:
            manageRooms()
        elif ch==4:
            dataAnalysis()
        elif ch==5:
            break