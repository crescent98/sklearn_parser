import xlrd
import sys

# get the xl file
wb=xlrd.open_workbook(sys.argv[1])
print(sys.argv[1])
ws=wb.sheet_by_index(2)
print(wb.sheet_names())
print(ws.cell_value(4,1))
