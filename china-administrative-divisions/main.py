from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
from Node import Node
import time
import json
import random
import requests
import multiprocessing as mp
import pymysql.cursors
import redis

provinceUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"

# 获取省份
def getProvince():
    
    soup = BeautifulSoup(getHtmlByRequests(provinceUrl))

    provincetr = soup.find_all("tr", class_="provincetr")
    # print(provincetr)

    plist = []
    for province in provincetr:
        pa = province.find_all("a")
        for a in pa:
            name = a.contents[0]
            url = "{}{}".format(provinceUrl,a['href'])
            i = url.strip().rindex('/')
            code = url[i+1:i+3]
            p = Node(name,url)
            p.setCode(code)
            plist.append(p)

    return plist

def loadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas

uas = loadUserAgents("user_agents.txt")
r = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)

def getHtml(url):
    html =""
    ua = random.choice(uas)
    print(ua)
    # 写法1：
    # html = urlopen("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/").read().decode('gbk')
    req = urllib.request.Request(url, headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': ua
    })
    time.sleep(3)
    # 写法2:
    with urlopen(req) as response:
        data = response.read()
        html = data.decode('gbk')
        print("code:{}".format(response.getcode()))
    
    # print(html)
    return html

session = requests.Session()
hkey = "docs"
failURLs = 'fails'

def getHtmlByRequests(url):
    html = ''
    if r.hexists(hkey,url):
        html = r.hget(hkey,url) 
        if '502 Bad Gateway' not in html and 'sojson.v5' not in html:
            # print("{} cache success value:{}".format(url,html))
            return html
    print("{} doc not in redis".format(url))
    response = session.get(url)
    response.encoding="gbk"
    html = response.text
    if '502 Bad Gateway' in html or 'sojson.v5' in html:
        print("html {} put {} to fail queue".format(html,url))
        r.lpush(failURLs,url)
    else:
         print("put {} doc {} into docs hash".format(url,html))
    r.hset(hkey,url,html)
    return html    

def getAllByNode(node:Node,_class="citytr",list = ["citytr","countytr","towntr","villagetr"]):
    if(node.url):
        i = list.index(_class)
        doc1 = getHtmlByRequests(node.url)
        if '502 Bad Gateway' not in doc1:
            nodeSoup = BeautifulSoup(doc1)
            soups = nodeSoup.find_all("tr",class_=_class)
            subs = []
            for soup in soups:
                if(_class != "villagetr"):
                    tdSoup = soup.find_all("td")[1]
                    if(tdSoup.find("a")):
                        name = tdSoup.find("a").contents[0]
                        url = "{}{}".format(node.url[:node.url.rindex('/')+1], tdSoup.find("a")['href'])
                        code = soup.find_all("td")[0].find("a").contents[0]
                        sub = Node(name,url)
                        sub.setCode(code)
                        print(sub)
                        getAllByNode(sub,list[i+1])
                        subs.append(sub)
                else:
                    # print(soup)
                    tdSoups = soup.find_all("td")
                    name = tdSoups[2].contents[0]
                    code = tdSoups[0].contents[0]
                    sub = Node(name,"")
                    sub.setCode(code)
                    subs.append(sub)
                    print(sub)
            node.setSubs(subs)
    if(_class=="citytr"):
        writeNodeToJSONFile(node,"{}".format(node.name))

def getAllByNodeAndInsertIntoDB(node:Node,_class="citytr",list = ["citytr","countytr","towntr","villagetr"]):
    # pid = insertIntoDB(node)
    if(node.url):
        i = list.index(_class)
        level = i+1
        doc1 = getHtmlByRequests(node.url)
        if '502 Bad Gateway' not in doc1:
            nodeSoup = BeautifulSoup(doc1)
            soups = nodeSoup.find_all("tr",class_=_class)
            for soup in soups:
                if(_class != "villagetr"):
                    tdSoup = soup.find_all("td")[1]
                    if(tdSoup.find("a")):
                        name = tdSoup.find("a").contents[0]
                        url = "{}{}".format(node.url[:node.url.rindex('/')+1], tdSoup.find("a")['href'])
                        code = soup.find_all("td")[0].find("a").contents[0]
                        sub = Node(name,url)
                        sub.setCode(code)
                        # print(sub)
                        # insertIntoDB(sub,pid,level)
                        getAllByNodeAndInsertIntoDB(sub,list[i+1])
                else:
                    # print(soup)
                    tdSoups = soup.find_all("td")
                    name = tdSoups[2].contents[0]
                    code = tdSoups[0].contents[0]
                    sub = Node(name,"")
                    sub.setCode(code)
                    # print(sub)
                    # insertIntoDB(sub,pid,level)

def insertIntoDB(node:Node,parentId=0,level=0):
    print('insertIntoDB')
    print(node)
    id = 0
    connection = pymysql.connect(host='localhost',port=3307,user='root'
    ,password='123456',db='spiders',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        exist = False
        with connection.cursor() as cursor:
            sql = "select id from node where code=%s"
            cursor.execute(sql,(node.code))
            result = cursor.fetchone()
            print(result)
            if result:
                id = result['id']
                if id>0:
                    exist = True
        print(exist)
        if exist==False:
            print("不存在，插入数据库")
            with connection.cursor() as cursor:
                sql = "insert into node (`parent_id`,`name`,`code`,`url`,`level`) values (%s,%s,%s,%s,%s)"
                cursor.execute(sql,(parentId,node.name,node.code,node.url,level))
            connection.commit()

            with connection.cursor() as cursor:
                sql = "select id from node where code=%s"
                cursor.execute(sql,(node.code))
                result = cursor.fetchone()
                print(result)
                id = result['id']
    finally:
        connection.close()
    return id

def obj_to_dict(obj):
    return obj.__dict__


# 多进程处理
def multicore():
    nodes = getProvince()
    pool = mp.Pool()
    try:
        pool.map(getAllByNodeAndInsertIntoDB,nodes)
    except Exception as e:
        print(e)
    pool.close()
    pool.join()

# 单进程处理
def signleCore(nodes):
    for node in nodes:
        getAllByNodeAndInsertIntoDB(node)

def writeNodeToJSONFile(object,filename):
    s =json.dumps(object, default=obj_to_dict,ensure_ascii=False).encode('utf8')
    s = s.decode('utf8')
    # print(s)
    with open("{}.json".format(filename),"w") as file:
        file.write(s)

def insertANode():
    node = Node("重庆市","http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/50.html")
    node.setCode(50)
    id = insertIntoDB(node)
    print(id)

def stringContain(s1,s2):
    return s2 not in s1

def scanFailUrl():
    url = []
    keys = r.hkeys(hkey)
    for key in keys:
        val = r.hget(hkey,key)
        if '502 Bad Gateway' in val or 'sojson.v5' in val:
            # if 'sojson.v5' in val:
            #     print(val)
            url.append(key)
            r.lpush(failURLs,key)
    return url

def processFail():
    print(r.llen(failURLs))
    while(r.llen(failURLs)>0):
        url = r.rpop(failURLs)
        print(url)
        getHtmlByRequests(url)

if __name__ == "__main__":
    time1 = time.time()
    # signleCore(nodes)
    multicore()
    # print(scanFailUrl())
    # processFail()
    # print(r.lrange(failURLs,0,-1))
    # print(r.hlen(hkey))#28906 33368 35736 36183 44253 45872 46348 46392 46392
    # getHtmlByRequests('http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/65/90/659006.html')
    # print(len(scanFailUrl()))#199 197 370 183 164 69 277 96 10 2
    # print(r.llen(failURLs))
    time2 = time.time()
    print(str(time2-time1))


