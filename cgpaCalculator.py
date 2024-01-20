import json, os
from prettytable import PrettyTable

def match(a, b):
    a = ''.join(x for x in a if x.isalnum())
    b = ''.join(x for x in b if x.isalnum())
    return a == b

def check(branch, courseno, courses_data):
    for course in courses_data["Courses"]:
        if match(course["Code"], courseno)  and branch in course["Branches"]:
            return True
    return False


def gradeConverter(grade):
    if not grade:
        return -1
    
    gpa = -1
    if grade[0] == 'O':
        gpa = 10
    elif grade[0] == 'A':
        gpa = 9
    elif grade[0] == 'B':
        gpa = 8
    elif grade[0] == 'C':
        gpa = 7
    elif grade[0] == 'D':
        gpa = 6
    elif grade[0] == 'E':
        gpa = 4
    elif grade[0] == 'F':
        gpa = 0
    elif grade[0] == 'P':
        gpa = 1
    return gpa

def calc_cgpa(branch='CSE'):

    dir = os.path.dirname(__file__)
    file_path = dir + '/response.json'
    elective_file_path = dir + '/courses_data.json'

    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        course_data = json_data['newdataset'][0]["table3"]
        
    with open(elective_file_path, 'r') as json_file:
        elective_data = json.load(json_file)

    cgpa, gradedCredits, pfCredits, totalCredits, clearedCredits, clearedDECredits, totalDECredits, gradedDECredits = 0, 0, 0, 0, 0, 0, 0, 0
    table = PrettyTable()
    table.field_names = ["Course Name", "Credit", "Grade"]
    
    
    for course in course_data:
        is_DE = False
        course_no = course['courseno'][0]["_value"]
        course_name = course["coursename"][0]["_value"]
        credit = float(course["credit"][0]["_value"]) if course["credit"][0]["_value"] else 0.0
        is_pass_fail = course["ispassfailcourse"][0]["_value"]
        grade = course.get("gradecode",[{}])[0].get("_value","")
        
        table.add_row([course_name, credit, grade])
        
        gpa = gradeConverter(grade)
        if is_pass_fail == 'No':
            if check(branch, course_no, elective_data):
                is_DE = True
            if gpa >= 0: # Graded
                gradedCredits += credit
                if is_DE:
                    gradedDECredits += credit     
            
            if gpa >= 4: # Passed
                clearedCredits += credit
                cgpa += credit * gpa
                if is_DE:
                    clearedDECredits += credit
                
            totalCredits += credit
            if is_DE:
                totalDECredits += credit
        else: 
            if gpa >= 0:
                pfCredits += credit
            if gpa == 1: # Cleared
                clearedCredits += credit
            totalCredits += credit
        
    if gradedCredits:
        cgpa = round(cgpa/gradedCredits, 3)
        
    return table, cgpa, totalCredits, gradedCredits, clearedCredits, totalDECredits, gradedDECredits, clearedDECredits, pfCredits