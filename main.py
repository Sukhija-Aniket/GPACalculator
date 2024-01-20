from dataExtractor import extract_data
from cgpaCalculator import calc_cgpa

from PIL import Image
from io import BytesIO
import base64

branchMap = {
    "ROHITSALUJAB20": "CSE",
    "JINESHMACHAARB20": "DSE",
    "GOPISHRIKANTHREDDY": "EE"
}

def update(*args):
    arr = []
    for name in args:
        updatedName = ''.join(x for x in name if x != ' ')
        updatedName = updatedName.upper()
        arr.append(updatedName)
    return tuple(arr)
            
        

def getBranch(facultyAdvisor, rollNumber):
        facultyAdvisor, rollNumber = update(facultyAdvisor, rollNumber)
        print(facultyAdvisor, rollNumber)
        key = facultyAdvisor + rollNumber[0:3]
        val =  branchMap.get(key, None)
        return val
    
rollNumber = input("Enter your roll Number: ")
name, facultyAdvisor = extract_data(rollNumber)
branch = getBranch(facultyAdvisor, rollNumber)
table, cgpa, totalCredits, gradedCredits, clearedCredits, totalDECredits, gradedDECredits, clearedDECredits, pfCredits = calc_cgpa(branch=branch)

print(table)
print(f"\n\nName: {name}\nCGPA: {cgpa}\nTotal Credits: {totalCredits}\nGraded Credits: {gradedCredits}\nPF Credits: {pfCredits}\nCleared Credits: {clearedCredits}\nTotal DE Credits: {totalDECredits}\nGraded DE Credits: {gradedDECredits}\nCleared DE Credits: {clearedDECredits}")

