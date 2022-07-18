import mysql.connector as sql
import pandas as pd 
import json

config=(json.load(open('config.json')))

    
db = sql.connect(host=config['host'] ,
                user=config['user'] ,
                password=config['password'])

cs=db.cursor()
cs.execute('create database if not exists hotel')
cs.execute('use hotel')


def startup():

    #Rooms
    cs.execute("""create table if not exists 
                Rooms(RoomNo int primary key,
                Floor int not null,
                Status varchar(20) not null,
                Type varchar(20) not null,
                ReservationID int)""")
    #Guests
    cs.execute("""create table if not exists
                Guests(Guest_ID int primary key,
                Reservation_ID int not null,
                First_Name varchar(20) not null,
                Last_Name varchar(20) not null,
                Phone_Number char(10) not null,
                RoomNo int )""")

    #Reservations
    cs.execute("""create table if not exists
                Reservations(Reservation_ID int primary key,
                Guest_ID int not null,
                PkCode int not null,
                Phone_Number char(10) not null,
                CheckIn date not null,
                CheckOut date not null,
                Nights int,
                RoomNo int , 
                Expenses int not null,
                constraint check_PkCode check (PkCode between 1 and 12) 
                )
                
    """)# Checked in boolean shows as 1 and 0 in the table

    #Employees
    cs.execute("""create table if not exists
                Employees(Empcode int primary key,
                Empname varchar(20) not null,
                Designation varchar(20) not null,
                Salary int not null,
                DateofJoin date not null)
                """)
    #Packages
    cs.execute("""create table if not exists
                Packages(Pk_Code int primary key,
                Max int not null,
                Room_Type varchar(20) not null,
                Package_Type varchar(100) not null,
                Cost_Per_Night int not null,
                Tourism_Fee int not null)

    """)
    #History
    cs.execute("""create table if not exists
                History(First_Name varchar(20) not null,
                Last_Name varchar(20) not null,
                Phone_Number char(10) primary key,
                Pk_code int not null,
                Expenses int not null,
                CheckIn date not null,
                Checkout date not null,
                FeedBack int not null,
                Comments varchar(200),
                constraint check_FeedBack check (Feedback between 1 and 10)
                )

    """)
    print('Startup Done')

def insert_values():
    #Packages
    
    Packages =pd.read_excel('Hotel.xlsx' , 'Packages' ).to_dict(orient='list')

    Pkcode=Packages['Pkcode']
    People=Packages['People']
    Type=Packages['Type']
    Details=Packages['Details']
    Rate=Packages['Rate']
    Tourism=Packages['Tourism']
    for i in range(0,len(Pkcode)):
        cs.execute(f'insert into Packages values({Pkcode[i]},{People[i]},"{Type[i]}","{Details[i]}",{Rate[i]},{Tourism[i]})')

    #Rooms
    Rooms =pd.read_excel('Hotel.xlsx' , 'Rooms' ).to_dict(orient='list')
    RoomNo=Rooms['RoomNo']
    Floor=Rooms['Floor']
    Status=Rooms['Status']
    Type=Rooms['Type']
    rid=Rooms['Reservation id']
    for i in range(0,len(RoomNo)):
        cs.execute(f'insert into Rooms values({RoomNo[i]},{Floor[i]},"{Status[i]}","{Type[i]}",{rid[i]})')


    #History
    History =pd.read_excel('Hotel.xlsx' , 'Feedback' ).to_dict(orient='list')
    fname=History['FirstName']
    lname=History['LastName']
    phone=History['PhoneNumber']
    Pk_Code=History['Pk_Code']
    Exp=History['Expenses']
    checkin=History['CheckIn']
    checkout=History['Checkout']
    feedback=History['Feedback']
    comments=History['Comments']

    for i in range(0,len(fname)):
        cs.execute(f'insert into history values("{fname[i]}","{lname[i]}","0{phone[i]}",{Pk_Code[i]},{Exp[i]},{checkin[i]},{checkout[i]},{feedback[i]},"{comments[i]}")')
   
    #Employees
    cs.execute("insert into employees values(101 ,'Anand' , 'IT',20000,'2005-07-23')")
    cs.execute("insert into employees values(102 ,'Max' , 'LifeGuard',5000,'2004-03-21')")
    cs.execute("insert into employees values(103 ,'Gordan' , 'Chef',20000,'2007-02-23')")

    #Guests
    cs.execute('insert into Guests values(1004648,12944,"Jordan","Cross","0507313342",NULL)')
    cs.execute('insert into Guests values(1017095,10435,"Eric","Soders","0524345211",NULL)')
    cs.execute('insert into Guests values(1083125,10862,"Gilchrist","Tavares","0567681598",302)')
    
    #Reservations
    cs.execute('insert into Reservations values(10435,1017095,7 ,"0524345211","2022-09-02" ,"2022-09-21" ,19,NULL,18050)')
    cs.execute('insert into Reservations values(10862,1083125,3 ,"0567681598","2022-07-23" ,"2022-07-31" ,8,302,9800)')
    cs.execute('insert into Reservations values(12944,1004648,11 ,"0507313342","2022-08-20" ,"2022-08-30" ,10,NULL,16200)')

   
    
    db.commit()


