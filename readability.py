from cs50 import get_string

text = get_string("Text: ")

letter = 0
w = 1
s = 0
for i in text:
    if i.isalpha():
        letter = letter + 1
    elif i == ' ':
        w = w + 1
    elif i == '.' or i == "!" or i == '?':
        s = s + 1

L = (letter * 100)/w
S = (s * 100)/w
grade = 0.0588 * L - 0.296 * S - 15.8
index = round(grade)
if index > 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print("Grade ", index)