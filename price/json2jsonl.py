
import json
import jsonlines
from os import listdir
import os
# JSON to JSON lines

# 将单个JSON文件转换成JSON Lines文件
def json2jsonl(jsonFileName,jsonlFileName):
    with open(jsonFileName) as jsonFile:
        data = json.load(jsonFile)
        with jsonlines.open(jsonlFileName, mode='w') as writer:
            writer.write_all(data)
    return 

# 将目录下的所有json文件转换成json lines文件
def json2jsonlByFolder(folder,limit=-1):
    count = 0
    files = listdir(folder)
    jsonlFolderName = "{}/jsonl/".format(folder)
    if not os.path.exists(jsonlFolderName):
        os.makedirs(jsonlFolderName)
    for file in files:
        if not file.endswith(".json"):
            continue

        if(limit != -1 and count>=limit):
            break

        json2jsonl("{}/{}".format(folder,file),"{}/jsonl/{}l".format(folder,file))  
        count = count+1
    return 

# json2jsonl("/Users/zhangzhiwen/prices/2020-05-31.json")
json2jsonlByFolder("/Users/zhangzhiwen/prices")