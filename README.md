# 将上大课表导出为 csv 或 ics 日历文件

![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/version-0.0.6-519dd9.svg)
![](https://img.shields.io/badge/license-WTFPL-000000.svg)

----------------------------------------------------------------------

把课表导出为 csv 或 ics 文件，可将其导入到 Google 日历 或 Microsoft Outlook 中。

安装
----

```bash
pip3 install pipenv #如果未安装 pipenv
git clone https://github.com/stormyyd/shu-course-to-csv.git
cd shu-course-to-csv
pipenv install
pipenv shell
python convert.py ... #见用法
```

另外，对于 64-bit Windows 用户，强烈建议在 [这里](https://github.com/stormyyd/shu-course-to-csv/releases) 下载制作好的二进制文件直接使用。32-bit 的因为没有环境，懒得弄了，用上面的方法吧。

用法
----

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

几个例子
------

    python convert.py -u 学号 -p 密码 课表.csv

以本周周一为该学期第一天，学校选课网站端口为 80，该学期周数为 10（即普通学期）来生成课表，生成的文件为该目录下的 课表.csv 文件。

    python convert.py -u 学号 -p 密码 -P 8080 课表.csv

以本周周一为该学期第一天，学校选课网站端口为 8080，该学期周数为 10（即普通学期）来生成课表，生成的文件为该目录下的 课表.csv 文件。

    python convert.py -u 学号 -p 密码 -w 2 -f 2018-06-18 -t ics 课表.ics

以 2018年6月18日 为该学期第一天，学校选课网站端口为80，该学期周数为2（即夏季短学期）来生成课表，生成的文件为该目录下的 课表.ics 文件。

已知可能存在的问题
---------------

不知道选课系统会不会冒出一些对上课时间奇怪的描述，目前已知且该程序可以处理的对上课时间的描述收录在 [known_time_string.csv](https://github.com/stormyyd/shu-course-to-csv/blob/master/known_time_string.csv) 中。如果你遇到了该程序不能处理的或未收录在上述文件中的类型欢迎在 Issue 中提出，提出时请务必附上选课界面的图片。

TODO
----
- 移除 ics.py 依赖
