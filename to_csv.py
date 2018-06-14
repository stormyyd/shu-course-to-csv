from get_course import get_course
from course_time import detect
import os
import csv
import datetime

def to_csv(username: str, password: str, csv_filename: str, port: int =80, weeks: int =10, first_day: datetime.date =None) -> None:
    if(os.path.isfile(csv_filename)):
        print('File {0} already exists. Overwrite it? <y/N> '.format(csv_filename), end = '')
        if(input().lower() != 'y'):
            return
    courses_list = get_course(username, password, port)
    with open(csv_filename, 'w', newline='') as f:
        fieldnames = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Description', 'Location']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in courses_list:
            time_list = detect(i['time'], first_day=first_day, weeks=2)
            row = {
                'Subject': i['name'],
                'Description': '教师：{0}'.format(i['teacher']),
                'Location': i['location']
            }
            for j in time_list:
                row['Start Date'] = j['start_time'].date().isoformat()
                row['End Date'] = j['end_time'].date().isoformat()
                row["Start Time"] = j['start_time'].time().strftime("%H:%M")
                row["End Time"] = j['end_time'].time().strftime("%H:%M")
                writer.writerow(row)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='Your student ID.', required=True)
    parser.add_argument('-p', '--password', help='Your password.', required=True)
    parser.add_argument('-P', '--port', type=int, help='The port of xk.shu.edu.cn, 80 or 8080. The default is 80.')
    parser.add_argument('-w', '--weeks', type=int, help='The weeks of this semester, 10 for the general semester or 2 for the short semester. The default is 10.')
    parser.add_argument('-f', '--first-day', help='The first day of this semester. Like 2018-06-18. The default is this Monday.')
    parser.add_argument('csv_filename', help='csv filename')
    args = parser.parse_args()
    to_csv(
        username=args.username,
        password=args.password,
        csv_filename=args.csv_filename,
        port=args.port if args.port else 80,
        weeks=args.weeks if args.weeks else 10,
        first_day=datetime.datetime.strptime(args.first_day, '%Y-%m-%d') if args.first_day else None
    )
