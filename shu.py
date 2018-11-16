import datetime
import html
import re

import lxml.html
import requests


class LoginError(Exception):

    def __init__(self, arg):
        self.args = arg


class SHU:

    __pattern = re.compile('(?P<weekday>[一二三四五])(?P<start_course>\d{1,2})-(?P<end_course>\d{1,2})'
                           '(?P<single>[单双\s])?(\s?\((?P<week_start>\d{1,2})(?P<type>[,-])'
                           '(?P<week_end>\d{1,2})周\)|\(第(?P<week>\d)周\))?')
    __a_week = datetime.timedelta(7)
    __start_time_map = {
        1: datetime.time(hour=8, minute=0),
        2: datetime.time(hour=8, minute=55),
        3: datetime.time(hour=10, minute=0),
        4: datetime.time(hour=10, minute=55),
        5: datetime.time(hour=12, minute=10),
        6: datetime.time(hour=13, minute=5),
        7: datetime.time(hour=14, minute=10),
        8: datetime.time(hour=15, minute=5),
        9: datetime.time(hour=16, minute=0),
        10: datetime.time(hour=16, minute=55),
        11: datetime.time(hour=18, minute=0),
        12: datetime.time(hour=18, minute=55),
        13: datetime.time(hour=19, minute=50),
    }
    __end_time_map = {
        1: datetime.time(hour=8, minute=45),
        2: datetime.time(hour=9, minute=40),
        3: datetime.time(hour=10, minute=45),
        4: datetime.time(hour=11, minute=40),
        5: datetime.time(hour=12, minute=55),
        6: datetime.time(hour=13, minute=50),
        7: datetime.time(hour=14, minute=55),
        8: datetime.time(hour=15, minute=50),
        9: datetime.time(hour=16, minute=45),
        10: datetime.time(hour=17, minute=40),
        11: datetime.time(hour=18, minute=45),
        12: datetime.time(hour=19, minute=40),
        13: datetime.time(hour=20, minute=35),
    }
    __weekday_map = {
        '一': datetime.timedelta(0),
        '二': datetime.timedelta(1),
        '三': datetime.timedelta(2),
        '四': datetime.timedelta(3),
        '五': datetime.timedelta(4),
    }

    def __init__(self, username, password, port=80, weeks=10, first_day=None):
        self.username = username
        self.password = password
        self.__weeks = weeks
        if first_day:
            self.__first_day = first_day - datetime.timedelta(first_day.weekday())
        else:
            today = datetime.date.today()
            self.__first_day = today - datetime.timedelta(today.weekday())
        self.__login_url = 'http://xk.autoisp.shu.edu.cn:{0}'.format(port)
        self.__course_list_url = 'http://xk.autoisp.shu.edu.cn:{0}/StudentQuery/CtrlViewQueryCourseTable'.format(port)
        self.__session = requests.session()
        self.__session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
        }
        self.__logged = False

    @staticmethod
    def get_saml_info(html_str):
        html_tree = lxml.html.fromstring(html_str)
        RelayState = html_tree.cssselect('input[name=RelayState]')[0].get('value')
        SAMLRequest = html_tree.cssselect('input[name=SAMLRequest]')
        SAMLResponse = html_tree.cssselect('input[name=SAMLResponse]')
        url = html.unescape(html_tree.cssselect('form')[0].get('action'))
        data = {
            'url': url,
            'data': {
                'RelayState': RelayState
            }
        }
        if SAMLRequest:
            data['data']['SAMLRequest'] = SAMLRequest[0].get('value')
        if SAMLResponse:
            data['data']['SAMLResponse'] = SAMLResponse[0].get('value')
        return data

    def login(self):
        xk_r = self.__session.get('http://xk.shu.edu.cn')
        info = SHU.get_saml_info(xk_r.text)
        self.__session.post(info['url'], data=info['data'])
        login_r = self.__session.post('https://sso.shu.edu.cn/idp/Authn/UserPassword', data={
            'j_password': self.password,
            'j_username': self.username
        })
        info = SHU.get_saml_info(login_r.text)
        r = self.__session.post(info['url'], data=info['data'])
        if self.username not in r.text:
            raise LoginError('login failed')
        self.__logged = True

    def get_course(self):
        if not self.__logged:
            self.login()
        course_web = self.__session.get(self.__course_list_url)
        html_tree = lxml.html.fromstring(course_web.text)
        courses_num = len(html_tree.xpath('/html/div/div/table[1]/tr')) - 4
        courses = []
        for i in range(4, 4 + courses_num):
            results = html_tree.xpath('/html/div/div/table[1]/tr[{0}]/td'.format(i))
            courses.append({
                'name': results[2].text.strip(),
                'teacher': results[4].text.strip(),
                'time': results[6].text.strip(),
                'location': results[7].text.strip()
            })
        return courses

    def detect(self, time_str):
        time_list = []
        for i in SHU.__pattern.finditer(time_str):
            day = self.__first_day + SHU.__weekday_map[i.group('weekday')]
            start_time = SHU.__start_time_map[int(i.group('start_course'))]
            end_time = SHU.__end_time_map[int(i.group('end_course'))]
            if i.group('week'):
                day += SHU.__a_week * (int(i.group('week')) - 1)
                time_list.append({
                    'start_time': datetime.datetime.combine(day, start_time),
                    'end_time': datetime.datetime.combine(day, end_time),
                })
                continue
            if i.group('type') == ',':
                day_ = day + SHU.__a_week * (int(i.group('week_start')) - 1)
                time_list.append({
                    'start_time': datetime.datetime.combine(day_, start_time),
                    'end_time': datetime.datetime.combine(day_, end_time),
                })
                day_ = day + SHU.__a_week * (int(i.group('week_end')) - 1)
                time_list.append({
                    'start_time': datetime.datetime.combine(day_, start_time),
                    'end_time': datetime.datetime.combine(day_, end_time),
                })
                continue
            if i.group('type') == '-':
                for j in range(int(i.group('week_start')), int(i.group('week_end')) + 1):
                    day_ = day + SHU.__a_week * (j - 1)
                    time_list.append({
                        'start_time': datetime.datetime.combine(day_, start_time),
                        'end_time': datetime.datetime.combine(day_, end_time),
                    })
                continue
            if i.group('single') == '单' or i.group('single') == '双':
                for j in range(1 if i.group('single') == '单' else 2, self.__weeks + 1, 2):
                    day_ = day + SHU.__a_week * (j - 1)
                    time_list.append({
                        'start_time': datetime.datetime.combine(day_, start_time),
                        'end_time': datetime.datetime.combine(day_, end_time),
                    })
                continue
            for j in range(1, self.__weeks + 1):
                day_ = day + SHU.__a_week * (j - 1)
                time_list.append({
                    'start_time': datetime.datetime.combine(day_, start_time),
                    'end_time': datetime.datetime.combine(day_, end_time),
                })
        return time_list
