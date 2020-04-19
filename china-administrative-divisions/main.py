from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
from Node import Node
import time
import json
import random


provinceUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"

# 获取省份
def getProvince():
    
    soup = BeautifulSoup(getHtml(provinceUrl))

    provincetr = soup.find_all("tr", class_="provincetr")
    # print(provincetr)

    plist = []
    for province in provincetr:
        pa = province.find_all("a")
        for a in pa:
            p = Node(a.contents[0],"%s%s" %(provinceUrl,a['href']))
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

def getHtml(url):
    html =""
    ua = random.choice(uas)
    # 写法1：
    # html = urlopen("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/").read().decode('gbk')
    req = urllib.request.Request(url, headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': ua
    })

    # 写法2:
    with urlopen(req) as response:
        data = response.read()
        html = data.decode('gbk')
 
    
    # print(html)
    return html


def getAllByNode(node:Node,_class="citytr",list = ["citytr","countytr","towntr","villagetr"]):
    if(node.url):
        i = list.index(_class)
        # TODO 改成字符串格式化的形式
        nodeSoup = BeautifulSoup(getHtml(node.url))
        soups = nodeSoup.find_all("tr",class_=_class)
        subs = []
        for soup in soups:
            if(_class != "villagetr"):
                tdSoup = soup.find_all("td")[1]
                name = tdSoup.find("a").contents[0]
                url = node.url[:node.url.rindex('/')+1] + tdSoup.find("a")['href']
                sub = Node(name,url)
                time.sleep(1)
                # print(sub)
                sub.setSubs(getAllByNode(sub,list[i+1]))
                subs.append(sub)
            else:
                tdSoups = soup.find_all("td")
                name = tdSoups[2].contents[0]
                code = tdSoups[0].contents[0]
                sub = Node(name,"")
                sub.setCode(code)
                subs.append(sub)
                # print(sub)
        node.setSubs(subs)
        
def obj_to_dict(obj):
    return obj.__dict__

if __name__ == "__main__":
    nodes = getProvince()
    for node in nodes:
        print(node)
        getAllByNode(node)
    print(nodes.toJSON())
    s =json.dumps(nodes, default=obj_to_dict)
    print(s)
