#use the api of openlaw ,and download relative text

import requests
import json
from datetime import datetime
import hashlib
import random
import time

from pymongo import MongoClient as MG

#create the utc time stamp
dt=datetime.now()

#######################################
stamp=str(int(round(time.time()*1000)))
#######################################

#set connect information
appkey='610c05a63d3940c7b9c7a9d2f51a2271'
appsec='d2228ddf6c9e43c6a50d9b0bdefe44e2'

#create random number
nonce=random.randint(0,9)
print(nonce)
print(stamp)
#calculate the hash number
hashStr=str(appsec)+str(nonce)+str(stamp)

print(type(hashStr))

hashNumber=hashlib.sha1(hashStr.encode('ascii'))
print(type(hashNumber))
hashNumber=hashNumber.hexdigest()

#set api interface
url='http://develop.openlaw.cn/judgement/search?keyword=诈骗'

#set header
header={
    "AppKey":appkey,
    "Nonce":str(nonce),
    "CurTime":stamp,
    "CheckSum":hashNumber
    }

print(header)
rq=requests.get(url,headers=header)

print(rq.text)

result=eval(rq.text)

###########################################3
#require text from ids

#get ids
judgelist=result["judgements"]

#set database
client=MG()
db=client.spider_data
collect=db.lawText

for each in judgelist:
    tmp_url='http://api.openlaw.cn/judgement/detail?id='
    id=each["judgement"]["id"]
    print(id)
    tmp_url=tmp_url+str(id)
    print(tmp_url)
    tmp_result=requests.get(tmp_url,headers=header)
    dataText=eval(tmp_result.text)
    
    data_id=collect.insert_one(dataText).inserted_id




