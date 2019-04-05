#探索mongodb数据

from pymongo import MongoClient as MG

client=MG()
db=client['spider_data']
collect=db.lawText

data=collect.find()

for item in data:
    print(item['judgement']['plaintext'])
    input()
