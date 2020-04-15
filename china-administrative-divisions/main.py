from bs4 import BeautifulSoup
from urllib.request import urlopen
from Province import Province

html = ""

# 写法1：
# html = urlopen("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/").read().decode('gbk')

# 写法2:
with urlopen("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/") as response:
    data = response.read()
    html = data.decode('gbk')

# print(html)

soup = BeautifulSoup(html)

provincetr = soup.find_all("tr", class_="provincetr")
print(provincetr)

plist = []
for province in provincetr:
    pa = province.find_all("a")
    for a in pa:
        p = Province(a.contents[0],a['href'])
        print(p)
        plist.append(p)
