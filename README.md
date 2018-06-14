# 将上大课表导出为 csv 日历文件

## 介绍

把课表导出为 csv 文件，可将其导入到 Google 日历 中。

## 安装

对于 Linux、OS X、WSL 用户，使用 git 将代码库克隆到任意目录，安装依赖后直接使用 to_csv.py 即可（见 [用法](#用法)）。

```
git clone https://github.com/stormyyd/shu-course-to-csv.git
cd shu-course-to-csv
pip3 install -r requirements.txt
python3 convert.py ...
```

对于 Windows 用户，建议在 [这里](https://github.com/stormyyd/shu-course-to-csv/releases) 下载制作好的二进制文件直接使用。或者使用上述方法。

## 用法

代码采用 Python 3 编写，在运行在 WSL 上的 Python 3.5.2 中工作正常，不保证低版本兼容性。

```
usage: convert.py [-h] -u USERNAME -p PASSWORD [-P PORT] [-w WEEKS]
                  [-f FIRST_DAY] [-t TYPE]
                  filename

positional arguments:
  filename              文件名

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        学生证号码
  -p PASSWORD, --password PASSWORD
                        学生证密码
  -P PORT, --port PORT  该学期选课网站的端口，80或8080，默认为80。
  -w WEEKS, --weeks WEEKS
                        该学期的周数，普通学期为 10，夏季短学期为
                        2，我没有报名国际化小学期并不知道是什么流程，
                        故夏季学期周数取 2 而非 4。默认为10。
  -f FIRST_DAY, --first-day FIRST_DAY
                        该学期的第一天，输入格式类似于 2018-06-18。
                        默认为本周周一。
  -t TYPE, --type TYPE  导出文件的类型，csv或ics。默认为csv。
```

### 几个例子

    python3 convert.py -u 学号 -p 密码 课表.csv

以本周周一为该学期第一天，学校选课网站端口为80，该学期周数为10（即普通学期）来生成课表，生成的文件为该目录下的 课表.csv 文件。

    python3 convert.py -u 学号 -p 密码 -P 8080 课表.csv

以本周周一为该学期第一天，学校选课网站端口为8080，该学期周数为10（即普通学期）来生成课表，生成的文件为该目录下的 课表.csv 文件。

    python3 convert.py -u 学号 -p 密码 -w 2 -f 2016-06-18 -t ics 课表.ics

以2018年6月18日为该学期第一天，学校选课网站端口为8080，该学期周数为2（即夏季短学期）来生成课表，生成的文件为该目录下的 课表.ics 文件。

## 程序结构

get_course.py 用于模拟登录选课网站以获取课表，使用了 requests 及 lxml 库，验证码识别来自 [shuopensourcecommunity/anti-captcha.shuosc.org
](https://github.com/shuopensourcecommunity/anti-captcha.shuosc.org)。

course_time.py 将上课时间字符串如“四11-13”、“二9-10(1-5)周”转换为程序可识别的 datetime 对象，核心为正则表达式。

to_csv.py 用于调用以上两个文件声明的函数并用于生成 csv 文件，并提供了一个简单的命令行交互界面。

## 已知可能存在的问题

不知道选课系统会不会冒出一些对上课时间奇怪的描述，目前已知且该程序可以处理的对上课时间的描述收录在 [known_time_string.csv](https://github.com/stormyyd/shu-course-to-csv/blob/master/known_time_string.csv) 中。如果你遇到了该程序不能处理的或未收录在上述文件中的类型欢迎在 Issue 中提出，提出时请务必附上选课界面的图片。
