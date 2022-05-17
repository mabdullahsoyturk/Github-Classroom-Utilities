import datetime
from utils import get_args, remove_existing_outs, get_students, download_repositories
from similarity import send_to_moss, download_moss_results

def main(args):
    remove_existing_outs(args)
    
    students = get_students(args)

    download_repositories(students)
            
    # Pledge of honor and submission time check
    for student in students:
        if args.pledge:
            student.check_pledge_of_honor()
        
        if args.submission_time:
            deadline = datetime.datetime(args.year, args.month, args.day, args.hour, args.minute)
            student.check_submission_date(deadline)

        if args.similarity:
            send_to_moss()

if __name__ == '__main__':
    args = get_args()
    main(args)