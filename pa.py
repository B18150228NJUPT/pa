import requests
from lxml import etree
from pyecharts.charts import Bar
a = []
import csv
# 0
url0 = "https://m.umu.cn/uapi/v2/element/chapter-session?t=1624945903712&parent_id=5509811&chapter_id=242354&page=1&size=50&get_draft=0"
# 5
url  = "https://m.umu.cn/uapi/v2/element/chapter-session?t=1624945905137&parent_id=5509811&chapter_id=264100&page=1&size=50&get_draft=0"
# 1
url1 = "https://m.umu.cn/uapi/v2/element/chapter-session?t=1624945904018&parent_id=5509811&chapter_id=242389&page=1&size=50&get_draft=0"
# 2
url2 = "https://m.umu.cn/uapi/v2/element/chapter-session?t=1624945904395&parent_id=5509811&chapter_id=247670&page=1&size=50&get_draft=0"
# 3
url3 = "https://m.umu.cn/uapi/v2/element/chapter-session?t=1624945904764&parent_id=5509811&chapter_id=251012&page=1&size=50&get_draft=0"
# 4
url4 = "https://m.umu.cn/uapi/v2/element/chapter-session?t=1624945905137&parent_id=5509811&chapter_id=264100&page=1&size=50&get_draft=0"

url_ids= "https://m.umu.cn/uapi/v1/chapter/completion-status?t=1624945903711&group_id=5509811&chapter_ids=242354%2C242389%2C247670%2C251012%2C264100%2C259924%2C280359"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'}
# 5
cookie_str ="_lang=zh-cn; umuU=dc2c58c744a8ade2795d3a649e957a79; JSESSID=n8ia72ldbprp6uq0l8b7u6j966; estuid=u129489231976; estuidtoken=9cbac1318497a52773675d34afcce1f61624942192; Hm_lvt_0dda0edb8e4fbece1e49e12fc49614dc=1624943244; DeviceId=DID_3ca16d4d723d44cb1ea18773cd1b7f1d; Hm_lpvt_0dda0edb8e4fbece1e49e12fc49614dc=1624945904"

type={}
type[14] = "文档"
type[11] = "视频"
type[13] = "文章"
type[2] = "提问"
type[10] = "考试"
type[1] = "问卷"
type[3] = "讨论"
type[16] = "作业"


def get_cookie(cookie_str):
    cookies = {}
    lines = cookie_str.split(';')
    for line in lines:
        key, value = line.strip().split('=', 1)
        cookies[key] = value
    return cookies

cookie = get_cookie(cookie_str)
def get_jsonitem(url):
    page=requests.Session().get(url=url,cookies=cookie,headers=headers)
    page.content.decode("utf-8")
    course_items = page.json()["data"]["list"]
    return course_items

def get_items(course_items,course_list):
    for course_item in course_items:
        course = {
            'name':course_item['title'],
            'participate':course_item['stat']['participate_num'],
            'type':type.get(course_item['type'])
        }
        course_list.append(course)

course_list = []
get_items(get_jsonitem(url0),course_list)
get_items(get_jsonitem(url1),course_list)
get_items(get_jsonitem(url2),course_list)
get_items(get_jsonitem(url3),course_list)
get_items(get_jsonitem(url4),course_list)
get_items(get_jsonitem(url),course_list)
print(course_list[0:])



bar = Bar()
# bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
x_list = []
y_list = []
z_list = []
for course in course_list:
    x_list.append(course["name"])
    y_list.append(course["participate"])
    z_list.append(course["type"])
bar.add_xaxis(x_list)
bar.add_yaxis("教育管理信息系统", y_list)

# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
bar.render()
#注意newline
with open("XXX.csv","w",newline="") as datacsv:
     #dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
     csvwriter = csv.writer(datacsv,dialect = ("excel"))
     #csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
     for course in course_list:
        csvwriter.writerow([course["name"],course["participate"],course["type"]])

