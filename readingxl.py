
# Reading an excel file using Python
import xlrd
 
# Give the location of the file
loc = ("Hotel.xls")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(2)
 
rows=range(6,10+1)

for i in rows:
   checkin=sheet.cell_value(i,4)
   checkin=checkin[1:-1]
   checkout=sheet.cell_value(i,5)
   checkout=checkout[1:-1]


   checkin= checkin[6:10] + checkin[2:-4] + checkin[0:2]
   checkout= checkout[6:10] + checkout[2:-4] + checkout[0:2]

   print(f"""cs.execute('insert into Reservations values({int(sheet.cell_value(i,0))},{int(sheet.cell_value(i,1))},{int(sheet.cell_value(i,2))},"0{int(sheet.cell_value(i,3))}","{checkin}","{checkout}",{int(sheet.cell_value(i,6))},{sheet.cell_value(i,7)},{int(sheet.cell_value(i,8))},{int(sheet.cell_value(i,9))})')"""
   
   )
  

