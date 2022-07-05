import mysql.connector as sql
import json

config=(json.load(open('config.json')))

    
db = sql.connect(host=config['host'] ,
                user=config['user'] ,
                password=config['password'])

cs=db.cursor()

cs.execute('create database if not exists hotel')
cs.execute('use hotel')

#Rooms
cs.execute("""create table if not exists 
            Rooms(RoomNo int primary key,
            Floor int,
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
            CheckedIn boolean not null,
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
            History(GuestID int primary key,
            PkCode int not null,
            First_Name varchar(20) not null,
            Last_Name varchar(20) not null,
            Phone_Number char(10) not null,
            RoomNo int not null,
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
    cs.execute("insert into employees values(101 ,'Anand' , 'IT',20000,'2005-07-23')")
    cs.execute("insert into employees values(102 ,'Max' , 'LifeGuard',5000,'2004-03-21')")
    cs.execute("insert into employees values(103 ,'Gordan' , 'Chef',20000,'2007-02-23')")

    #Packages
    cs.execute('insert into packages values(1,1,"Standard","Room Only",650,200)')
    cs.execute('insert into packages values(2,1,"Standard","Room and Breakfast",800,200)')
    cs.execute('insert into packages values(3,1,"Standard","Full Board",1200,200)')
    cs.execute('insert into packages values(4,2,"Deluxe","Room Only",800,400)')
    cs.execute('insert into packages values(5,2,"Deluxe","Room and Breakfast",950,400)')
    cs.execute('insert into packages values(6,2,"Deluxe","Full Board",1350,400)')
    cs.execute('insert into packages values(7,4,"Single Suite","Room Only",950,800)')
    cs.execute('insert into packages values(8,4,"Single Suite","Room and Breakfast",1100,800)')
    cs.execute('insert into packages values(9,4,"Single Suite","Full Board",1500,800)')
    cs.execute('insert into packages values(10,6,"Family Suite","Room Only",1350,1200)')
    cs.execute('insert into packages values(11,6,"Family Suite","Room and Breakfast",1500,1200)')
    cs.execute('insert into packages values(12,6,"Family Suite","Full Board",2000,1200)')


    #Reservations
    cs.execute('insert into Reservations values(10001,1123456,1,"0561202794","2022/07/12","2022/07/15",3,0,839,2150)')
    cs.execute('insert into Reservations values(10002,1234567,6,"0569312734","2022/07/02","2022/07/04",2,1,463,3100)')
    cs.execute('insert into Reservations values(10115,1203945,4,"0564628228","2022/10/14","2022/10/19",5,0,794,3600)')
    cs.execute('insert into Reservations values(10313,1987654,12,"0562323432","2022/12/30","2023/01/03",4,0,632,9200)')
    cs.execute('insert into Reservations values(10932,1322492,11,"0561249248","2022/06/29","2022/07/07",8,1,104,13200)')        
    

    
    
    db.commit()







#Occupied Rooms
# cs.execute("""create table if not exists
#             Occupied_Rooms(RoomNo int primary key,
#             Guest_ID int not null,
#             CheckIn datetime not null,
#             Checkout datetime not null,
#             Reservation_ID int not null)""")