import json, os
from prettytable import PrettyTable


def gradeConverter(grade):
    if not grade:
        return 0, False
    
    gpa, count = 0, True
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
    else: 
        count = False
    
    return gpa, count


def calc_cgpa():

    dir = os.path.dirname(__file__)
    file_path = dir + '/response.json'

    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        course_data = json_data['newdataset'][0]["table3"]

    cgpa, gradedCredits, totalCredits = 0, 0, 0
    table = PrettyTable()
    table.field_names = ["Course Name", "Credit", "Grade"]

    for course in course_data:
        course_name = course["coursename"][0]["_value"]
        credit = float(course["credit"][0]["_value"]) if course["credit"][0]["_value"] else 0.0
        is_pass_fail = course["ispassfailcourse"][0]["_value"]
        grade = course.get("gradecode",[{}])[0].get("_value","")
        
        table.add_row([course_name, credit, grade])
        
        if is_pass_fail == 'No':
            gpa, valid = gradeConverter(grade)
            if valid:
                cgpa += gpa*credit
                gradedCredits += credit
        totalCredits += credit
    if gradedCredits:
        cgpa = round(cgpa/gradedCredits, 3)
        
    return table, cgpa, totalCredits, gradedCredits