import random
import time
from urllib import request
import ua_info
import re
import pymysql

url_4k = 'https://wsygq.com/show/movie-4K--------'
url_1080p = 'https://wsygq.com/show/movie-1080P--------'
url_720p = 'https://wsygq.com/show/movie-720P--------'
url_all = 'https://wsygq.com/show/movie---------'
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



def handle_Href_Link(data):
    url_Movie = base_url + data[2]
    headers = {'User-Agent': ua_info.ua_list[random.randint(0, 9)]}
    req = request.Request(url=url_Movie, headers=headers)
    res = request.urlopen(req)
    html = res.read().decode('utf-8')
    try:
        link_All = re.findall(
            "<div class=\"downlist\" id=\"downlist\">(.*)</div></div><div class=\"layout-box clearfix\">",
            html)
        link_Split = re.split("</ul>", link_All[0])
        for block in link_Split:
            if block != '':
                li_List = re.split("</li><li>", re.findall("<li>(.*)</li>", block)[0])
                for a in li_List:
                    print(a)
    except Exception:
        print("Find Link Failed")


def handle_Href_List(id):
    cursor = db.cursor()
    id = id * 100;
    sql = 'SELECT * FROM Href WHERE id <=' + str(id) + ";"
    try:
        cursor.execute(sql)
        retDataList = cursor.fetchall()
        for temp in retDataList:
            print(temp)
        print("Select Data From Href Table Success,Index Max is: " + str(id))
    except Exception:
        print("Select Data From Href Failed")
        db.rollback()
    finally:
        cursor.close()


def create_Link_Table():
    cursor = db.cursor()
    sql = "CREATE TABLE MovieLink(id int PRIMARY KEY,movie_id int,link varchar(50));"
    try:
        cursor.execute(sql)
        sql1 = "alter table MovieLink change id id int auto_increment;"
        cursor.execute(sql1)
        db.commit()
        print("Create MovieLink Table Success")
    except Exception:
        print("Create MovieLink Table Failed")
        db.rollback()
    finally:
        cursor.close()


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
        db.rollback()
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
        db.rollback()
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


if __name__ == '__main__':
    # create_Href_Table()
    # create_Link_Table()
    # handle_Href_List(1)
    # handle_Href_Link((5, '阿甘正传', '/hd/3.html', 9.5))

    print("Reptile Success")

