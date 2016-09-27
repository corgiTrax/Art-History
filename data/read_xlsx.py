import xlrd
import sys
import re
import string
book = xlrd.open_workbook(sys.argv[1])
#print("The number of worksheets is", book.nsheets)
#print("Worksheet name(s):", book.sheet_names())
sh = book.sheet_by_index(0)
#print(sh.name, sh.nrows, sh.ncols)
#print("Cell 00 is ", sh.cell_value(rowx=0, colx=0))
for rx in range(sh.nrows):
    if rx != 0:
        row = sh.row(rx)
        wiki = row[5].value.encode('ascii','ignore')
        wikis = re.split('\n|\.|;|\?|!',wiki) 
        for sent in wikis:
#            print(item)
#            sent = item.encode('ascii', 'ignore')
            print(sent.translate(None, string.punctuation))
