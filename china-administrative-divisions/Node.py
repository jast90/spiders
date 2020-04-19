class Node:
    name = ''
    url = ''
    code = ''
    subs = []
    def __init__(self,name,url):
        self.name = name
        self.url = url

    def __str__(self):
        return 'name = %s, url= %s ,code = %s' %(self.name,self.url,self.code)

    def setSubs(self,subs):
        self.subs = subs

    def setCode(self,code):
        self.code = code