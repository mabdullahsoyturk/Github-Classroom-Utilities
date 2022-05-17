import os
import subprocess
import datetime

class Student:
    def __init__(self, args, username, identifier, repo_name, repo_link):
        self.args = args
        self.username = username
        self.identifier = identifier
        self.repo_name = repo_name
        self.repo_link = repo_link

    def download_repo(self):
        if os.path.exists(self.repo_name):
            print(f'{self.repo_name} already exists.')
            return

        result = subprocess.run(f'git clone {self.repo_link}', shell=True, check=True, stderr=subprocess.PIPE)
        if result.stderr != None:
            print(result.stderr.decode('utf-8').strip())

    def check_pledge_of_honor(self):
        with open(self.args.pledge_file, "a") as pledge_file:
            result = subprocess.run(f'grep "READ AND SIGN" {self.repo_name}/src/main/Main.java | wc -l', shell=True, check=True, stdout=subprocess.PIPE)
            exists = result.stdout.decode('utf-8').strip()
            
            pledge_file.write(f'{self.identifier},{exists}\n')
            
    def check_submission_date(self, deadline):
        if os.path.exists(self.repo_name):
            os.chdir(self.repo_name)

            date_and_time = subprocess.run('git log --pretty=format:"%ci" --date=iso8601-strict', shell=True, check=True, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")[0].strip()
            date, time, _ = date_and_time.split(" ")

            year, month, day = date.split("-")
            hour, minute, second = time.split(":")

            last_submission_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))

            os.chdir("../")

            with open(self.args.submission_file, "a") as submisson_file:
                if last_submission_time > deadline:
                    print(f'Late Submission: {self.identifier}, {last_submission_time}')
                    submisson_file.write(f'{self.identifier},{last_submission_time},0\n')
                else:
                    submisson_file.write(f'{self.identifier},{last_submission_time},1\n')