from dataExtractor import extract_data
from cgpaCalculator import calc_cgpa

rollNumber = input("Enter your roll Number: ")

name = extract_data(rollNumber)
table, cgpa, totalCredits, gradedCredits = calc_cgpa()

print(table)
print(f"\n\nName: {name}\nCGPA: {cgpa}\nTotal Credits: {totalCredits}\nGraded Credits: {gradedCredits}")

