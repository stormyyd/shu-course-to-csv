import datetime
import re

COURSE_START_TIME_MAP = {
    1: datetime.time(hour = 8, minute = 0),
    2: datetime.time(hour = 8, minute = 55),
    3: datetime.time(hour = 10, minute = 0),
    4: datetime.time(hour = 10, minute = 55),
    5: datetime.time(hour = 12, minute = 10),
    6: datetime.time(hour = 13, minute = 5),
    7: datetime.time(hour = 14, minute = 10),
    8: datetime.time(hour = 15, minute = 5),
    9: datetime.time(hour = 16, minute = 0),
    10: datetime.time(hour = 16, minute = 55),
    11: datetime.time(hour = 18, minute = 0),
    12: datetime.time(hour = 18, minute = 55),
    13: datetime.time(hour = 19, minute = 50),
}

COURSE_END_TIME_MAP = {
    1: datetime.time(hour = 8, minute = 45),
    2: datetime.time(hour = 9, minute = 40),
    3: datetime.time(hour = 10, minute = 45),
    4: datetime.time(hour = 11, minute = 40),
    5: datetime.time(hour = 12, minute = 55),
    6: datetime.time(hour = 13, minute = 50),
    7: datetime.time(hour = 14, minute = 55),
    8: datetime.time(hour = 15, minute = 50),
    9: datetime.time(hour = 16, minute = 45),
    10: datetime.time(hour = 17, minute = 40),
    11: datetime.time(hour = 18, minute = 45),
    12: datetime.time(hour = 19, minute = 40),
    13: datetime.time(hour = 20, minute = 35),
}

WEEKDAY_MAP = {
    '一': datetime.timedelta(0),
    '二': datetime.timedelta(1),
    '三': datetime.timedelta(2),
    '四': datetime.timedelta(3),
    '五': datetime.timedelta(4),
}

A_WEEK = datetime.timedelta(7)

PATTERN = re.compile('(?P<weekday>[一二三四五])(?P<start_course>\d{1,2})-(?P<end_course>\d{1,2})(?P<single>[单双\s])?(\((?P<week_start>\d{1,2})(?P<type>[,-])(?P<week_end>\d{1,2})周\)|\(第(?P<week>\d)周\))?')

def detect(time_str: str, first_day: datetime.date =None, weeks: int =10) -> list:
    if(not first_day):
        today = datetime.date.today()
        first_day = today - datetime.timedelta(today.weekday())
    if(first_day.weekday() != 0):
        first_day = first_day - datetime.timedelta(first_day.weekday())
    time_list = list()
    for i in PATTERN.finditer(time_str):
        day = first_day + WEEKDAY_MAP[i.group('weekday')]
        start_time = COURSE_START_TIME_MAP[int(i.group('start_course'))]
        end_time = COURSE_END_TIME_MAP[int(i.group('end_course'))]
        if(i.group('week')):
            day += A_WEEK * (int(i.group('week')) - 1)
            time_list.append({
                'start_time': datetime.datetime.combine(day, start_time),
                'end_time': datetime.datetime.combine(day, end_time),
            })
            continue
        if(i.group('type') == ','):
            day_ = day + A_WEEK * (int(i.group('week_start')) - 1)
            time_list.append({
                'start_time': datetime.datetime.combine(day_, start_time),
                'end_time': datetime.datetime.combine(day_, end_time),
            })
            day_ = day + A_WEEK * (int(i.group('week_end')) - 1)
            time_list.append({
                'start_time': datetime.datetime.combine(day_, start_time),
                'end_time': datetime.datetime.combine(day_, end_time),
            })
            continue
        if(i.group('type') == '-'):
            for j in range(int(i.group('week_start')), int(i.group('week_end')) + 1):
                day_ = day + A_WEEK * (j - 1)
                time_list.append({
                    'start_time': datetime.datetime.combine(day_, start_time),
                    'end_time': datetime.datetime.combine(day_, end_time),
                })
            continue
        if(i.group('single') == '单' or i.group('single') == '双'):
            for j in range(1 if i.group('single') == '单' else 2, weeks + 1, 2):
                day_ = day + A_WEEK * (j - 1)
                time_list.append({
                    'start_time': datetime.datetime.combine(day_, start_time),
                    'end_time': datetime.datetime.combine(day_, end_time),
                })
            continue
        for j in range(1, weeks + 1):
            day_ = day + A_WEEK * (j - 1)
            time_list.append({
                'start_time': datetime.datetime.combine(day_, start_time),
                'end_time': datetime.datetime.combine(day_, end_time),
            })
    return time_list


if __name__ == '__main__':
    import sys
    from pprint import pprint
    for i in sys.argv[1:]:
        result = detect(i)
        pprint(result)
        print('count={0}'.format(len(result)))
