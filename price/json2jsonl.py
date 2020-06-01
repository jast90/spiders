
import json
import jsonlines
from os import listdir

# JSON to JSON lines

# 将单个JSON文件转换成JSON Lines文件
def json2jsonl(jsonFileName):
    with open(jsonFileName) as jsonFile:
        data = json.load(jsonFile)
        with jsonlines.open("{}l".format(jsonFileName), mode='w') as writer:
            writer.write_all(data)
    return 

# 将目录下的所有json文件转换成json lines文件
def json2jsonlByFolder(folder,limit=3):
    count = 0
    files = listdir(folder)
    print(files) 
    for file in files:
        if(count>=limit):
            break
        json2jsonl("{}/{}".format(folder,file))  
        count = count+1
    return 

# json2jsonl("/Users/zhangzhiwen/prices/2020-05-31.json")
json2jsonlByFolder("/Users/zhangzhiwen/prices")