
# Reading an excel file using Python
import xlrd
 
# Give the location of the file
loc = ("Hotel.xls")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(1)
 
rows=range(1,25)

for i in rows:
   print(f"""cs.execute('insert into Rooms values({int(sheet.cell_value(i,0))},{int(sheet.cell_value(i,1))},"{sheet.cell_value(i,2)}" ,"{sheet.cell_value(i,3)}",Null)')"""
   )
   
  

