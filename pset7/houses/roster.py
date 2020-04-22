# TODO
import cs50
import sys
import csv

lst = sys.argv
if(len(lst) != 2):
    print("Error")
else:
    db = cs50.SQL("sqlite:///students.db")
    house = lst[1]
    rows = db.execute('select first, middle, last, birth from students where house= ? order by last,first', house)
    for each in rows:
        if(each['middle'] == None):
            print(each['first']+' '+each['last']+', born'+' '+str(each['birth']))
        else:
            print(each['first']+' '+each['middle']+' '+each['last']+', born'+' '+str(each['birth']))