class Province:
    name = ''
    url = ''
    def __init__(self,name,url):
        self.name = name
        self.url = url

    def __str__(self):
        return 'name = %s, url= %s' %(self.name,self.url)