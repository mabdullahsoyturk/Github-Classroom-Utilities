import argparse
import os
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