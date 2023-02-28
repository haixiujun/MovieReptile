import random
from urllib import request
import ua_info
import re
import pymysql

url_4k = 'https://wsygq.com/show/movie-4K--------'
url_1080p = 'https://wsygq.com/show/movie-1080P--------'
url_720p = 'https://wsygq.com/show/movie-720P--------'
url_all='https://wsygq.com/show/movie---------'
end_str = '---.html'
base_url = "https://wsygq.com"
db = pymysql.connect(
    host='192.168.0.109',
    port=3306,
    user='root',
    passwd='945231',
    db='IBLUE',
    charset='utf8'
)


def create_Href_Table():
    cursor = db.cursor()
    sql = "CREATE TABLE Href(id int PRIMARY KEY,name varchar(50),href varchar(50),score float);"
    try:
        cursor.execute(sql)
        sql1 = "alter table Href change id id int auto_increment;"
        cursor.execute(sql1)
        db.commit()
        print("Create Href Table Success")
    except Exception:
        print("Create Href Table Failed")
    finally:
        cursor.close()


def add_Href(title, score, url):
    cursor = db.cursor()
    sql = "INSERT INTO Href (name,score,href) VALUES (\"" + title + "\"," + score + ",\"" + url + "\");"
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        print("Insert Href Data Success")
    except:
        print("Insert Href Data Failed")
    finally:
        cursor.close()


def access_Page(pageNum, url):
    headers = {'User-Agent': ua_info.ua_list[random.randint(0, 9)]}
    urlAccess = url + str(pageNum) + end_str
    req = request.Request(url=urlAccess, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    movieAll = re.findall("id=\"content\">(.*)</li></ul></div></div><div class=\"box-page clearfix", html)[0]
    movieList = re.split("</li>", movieAll)
    i = 1
    for temp in movieList:
        print("Movie" + str(i) + ":")
        score = re.findall("<span class=\"score\">(.*)</span><span class", temp)
        href = re.findall("<a href=\"(.*)\" title=", temp)
        title = re.findall("\" title=\"(.*)\" style=", temp)
        add_Href(str(title[0]), str(score[0]), str(href[0]))
        # print("Score:" + str(score) + " title:" + str(title) + " href=" + str(href))
        i += 1


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    for i in range(1,505):
        #print(i)
        access_Page(i, url_all)

    # createHrefTable() # 第一次使用创建数据库

    db.close()
# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
