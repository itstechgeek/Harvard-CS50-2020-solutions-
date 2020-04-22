import sys
import csv
def main():
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    seq_count = {
                "AGATC" : count_seq("AGATC"),
                "TTTTTTCT" : count_seq("TTTTTTCT"),
                "AATG" : count_seq("AATG"),
                "TCTAG" : count_seq("TCTAG"),
                "GATA" : count_seq("GATA"),
                "TATC" : count_seq("TATC"),
                "GAAA" : count_seq("GAAA"),
                "TCTG" : count_seq("TCTG")
                }

    small = ("AGATC", "AATG", "TATC")
    large = ("AGATC", "TTTTTTCT", "AATG", "TCTAG", "GATA", "TATC", "GAAA", "TCTG")

    temp = small
    matched = False

    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        ncol = len(next(reader)) - 1
        csvfile.seek(0)
        next(reader)
        if ncol != 3:
            temp = large
        for row in reader:
            for i in range(ncol):
                if (int(row[temp[i]]) == seq_count[temp[i]]):
                    matched = True
                else:
                    matched = False
            if matched == True:
                print (row["name"])
                break
        if matched == False:
            print("No match")

def count_seq(ctr):
    c = 0
    new_c = 0
    l = len(ctr)
    dna_seq = open(sys.argv[2], "r").read()
    pos = dna_seq.find(ctr)
    if pos == -1:
        return 0
    i = pos
    while i < len(dna_seq):
        if dna_seq[i : i + l] == ctr:
            new_c += 1
            i += l
        else:
            i = i + 1
            if new_c > c:
                c = new_c
            new_c = 0
    return c

main()