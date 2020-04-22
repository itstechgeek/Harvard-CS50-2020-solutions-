# TODO
import cs50
import sys
import csv

lst = sys.argv
if(len(lst) != 2):
    print("Error")
else:
    f= sys.argv[1]
    db = cs50.SQL("sqlite:///students.db")
    #db.execute('create table students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)')
    with open(f, "r") as input:

        # Create DictReader
        reader = csv.DictReader(input)
        i = 1
        for row in reader:
            name = row['name']
            house = row['house']
            birth = row['birth']
            name_lst = name.split(' ')
            if (len(name_lst) == 2):
                first = name_lst[0]
                middle = None
                last = name_lst[1]
            elif (len(name_lst) == 3):
                first = name_lst[0]
                middle = name_lst[1]
                last = name_lst[2]
            #print(first,middle,last)
            query = 'insert into students values(?, ?, ?, ?, ?, ?)'
            db.execute(query, i, first,middle, last, house, birth)
            i += 1
