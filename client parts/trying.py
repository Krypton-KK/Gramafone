r'''import csv
fh = open(r'..\Program files\keys.csv','a',newline='\r\n')
x = csv.reader(fh)
for i in x:
    print(i)
'''
x = b'hi_senorita=='[:-2]
print(x+b'==')