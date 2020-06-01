from urllib import request
import uuid  
import pyamf 
import json,datetime  
from pyamf import remoting  
from pyamf.flex import messaging  
import time
import jsonlines

class HqPara:    
    def __init__(self):  
        self.marketInfo = None  
        self.breedInfoDl = None  
        self.breedInfo = None  
        self.provice = None  
# https://en.wikipedia.org/wiki/Action_Message_Format  
# registerClassAlias("personTypeAlias", Person);  
# 注册自定义的Body参数类型，这样数据类型com.itown.kas.pfsc.report.po.HqPara就会在后面被一并发给服务端（否则服务端就可能返回参数不是预期的异常Client.Message.Deserialize.InvalidType）  
pyamf.register_class(HqPara, alias='com.itown.kas.pfsc.report.po.HqPara')  
  
# 构造flex.messaging.messages.RemotingMessage消息

msg = messaging.RemotingMessage(messageId=str(uuid.uuid1()).upper(),  
                                    clientId=str(uuid.uuid1()).upper(),  
                                    operation='getHqSearchData',  
                                    destination='reportStatService',  
                                    timeToLive=0,  
                                    timestamp=0)  
# 第一个是查询参数，第二个是页数，第三个是控制每页显示的数量（默认每页只显示15条）

# 构造请求数据
def getRequestData(page_num,total_num):
    msg.body = [HqPara(),str(page_num), str(total_num)]  
    msg.headers['DSEndpoint'] = None  
    msg.headers['DSId'] = str(uuid.uuid1()).upper()  
    # 按AMF协议编码数据  
    req = remoting.Request('null', body=(msg,))  
    env = remoting.Envelope(amfVersion=pyamf.AMF3)  
    env.bodies = [('/1', req)]  
    data = bytes(remoting.encode(env).read())
    return data
# 获取响应源数据
def getResponse(data):
    url = 'http://jgsb.agri.cn/messagebroker/amf'
    req = request.Request(url, data, headers={'Content-Type': 'application/x-amf'})
    # 解析返回数据  
    opener = request.build_opener()          
    return opener.open(req).read()
# 解析d
def getContent(response):
    amf_parse_info = remoting.decode(response)
    # 数据总条数
    total_num = amf_parse_info.bodies[0][1].body.body[3]
    info = amf_parse_info.bodies[0][1].body.body[0]
    print("总条数：{}".format(total_num))
    return total_num, info

def store2json(info,filename):
    res = []
    for record in info:
        if(record['reportDate']):
            record['reportDate'] = record['reportDate'].strftime('%Y-%m-%d %H:%M:%S')
        if(record['auditDate']):
            record['auditDate'] = record['auditDate'].strftime('%Y-%m-%d %H:%M:%S')
        if(record['snatchDate']):
            record['snatchDate'] = record['snatchDate'].strftime('%Y-%m-%d %H:%M:%S')
        
        res.append(record)
    # with open('prices/{}.json'.format(filename),'w') as fp:
        # json.dump(res,fp,indent=4,ensure_ascii=False)
    with jsonlines.open('prices/{}.jsonl'.format(filename), mode='w') as writer:
        writer.write_all(res)

def getDateString():
    return time.strftime("%Y-%m-%d",time.localtime())

def getTodayDataToJson():
    reqData = getRequestData(1,15)
    rep = getResponse(reqData)
    total_num,info = getContent(rep)

    reqData = getRequestData(1,total_num)
    rep = getResponse(reqData)
    total_num,info = getContent(rep)
    store2json(info,getDateString())

getTodayDataToJson()