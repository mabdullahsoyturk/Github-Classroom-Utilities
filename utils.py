import argparse
import os
import glob
from student import Student

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pledge', action='store_true', default=True, help='Check pledge of honor')
    parser.add_argument('--submission_time', action='store_true', default=True, help='Check last submission time')
    parser.add_argument('--similarity', action='store_true', default=True, help='Check similarity')
    parser.add_argument('--lab_file', default='lab7.csv', help='Path to lab file retrieved from Github Classroom')
    parser.add_argument('--pledge_file', default='pledge.csv', help='Path to output pledge file')
    parser.add_argument('--submission_file', default='submission_time.csv', help='Path to output submission time file')
    parser.add_argument('--year', default=2022, type=int, help='Deadline year')
    parser.add_argument('--month', default=5, type=int, help='Deadline month')
    parser.add_argument('--day', default=13, type=int, help='Deadline day')
    parser.add_argument('--hour', default=11, type=int, help='Deadline hour')
    parser.add_argument('--minute', default=30, type=int, help='Deadline minute')
    return parser.parse_args()

def remove_existing_outs(args):
    if os.path.exists(args.pledge_file):
        os.remove(args.pledge_file)

    if os.path.exists(args.submission_file):
        os.remove(args.submission_file)

def get_students(args):
    students = []

    with open(args.lab_file) as lab7:
        lines = lab7.readlines()

        for line in lines:
            _, _, _, username, identifier, repo_name, repo_link, _, _, _ = line.split(",")
            
            student = Student(args, username, identifier, repo_name, repo_link)

            students.append(student)
    
    return students

def download_repositories(students):
    for student in students:
        student.download_repo()

def download_moss_results(link):
    if not os.path.isdir('students'):
        os.mkdir("students")

    os.system(f'wget {link}')

    main_html_file = glob.glob("*.html")[0]

    out = subprocess.check_output(["grep", "<TD>", main_html_file]).decode("utf-8").split("\n")

    links = []

    for index, line in enumerate(out):
        if index % 2 == 0:
            splitted = line.strip().split('"')

            if len(splitted) > 1:
                links.append(splitted[1])

    os.chdir("students/")

    for link in links:
        folder_name = link.split("/")[-1][:-5]
        os.mkdir(folder_name)
        os.chdir(folder_name)
        
        os.system(f'wget {link}')
        zeroth = "{}-0.html".format(link[:-5])
        first = "{}-1.html".format(link[:-5])
        
        os.system(f'wget {zeroth}')
        os.system(f'wget {first}')

        os.chdir("../")
    