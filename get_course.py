import requests
import lxml.html

VALIDATE_CODE_URL = 'http://xk.shu.edu.cn:{0}/Login/GetValidateCode'
LOGIN_URL = 'http://xk.shu.edu.cn:{0}'
ANTI_CAPTCHA_URL = 'http://anti-captcha.iskeng.cn/jwc'
COURSE_LIST_URL = 'http://xk.shu.edu.cn:{0}/StudentQuery/CtrlViewQueryCourseTable'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'

def get_course(username: str, password: str, port: int = 80) -> list:
    s = requests.session()
    s.headers.update({
        'User-Agent': USER_AGENT
    })
    files = {
        'captcha': ('validateCode.jpg', s.get(VALIDATE_CODE_URL.format(port)).content, 'image/jpg')
    }
    anti_captcha = requests.post(ANTI_CAPTCHA_URL, files = files)
    result = anti_captcha.json()
    if not result['succeed']:
        raise Exception(result["reason"])
    validate_code = result["result"]
    login_data = {
        'txtUserName': username,
        'txtPassword': password,
        'txtValiCode': validate_code
    }
    s.post(LOGIN_URL.format(port), data = login_data)
    course_web = s.get(COURSE_LIST_URL.format(port))
    html = lxml.html.fromstring(course_web.text)
    courses_num = len(html.xpath('/html/div/div/table[1]/tr')) - 4
    courses = list()
    for i in range(4, 4 + courses_num):
        results = html.xpath('/html/div/div/table[1]/tr[{0}]/td'.format(i))
        courses.append({
            'name': results[2].text.strip(),
            'teacher': results[4].text.strip(),
            'time': results[6].text.strip(),
            'location': results[7].text.strip()
        })
    return courses

if __name__ == '__main__':
    import sys
    from pprint import pprint
    if(len(sys.argv) < 3):
        print('Usage: get_course.py username password [port]')
        sys.exit(-1)
    elif(len(sys.argv) > 3):
        result = get_course(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        result = get_course(sys.argv[1], sys.argv[2])
    pprint(result)
