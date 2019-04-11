# research the structure of plain text

from pymongo import MongoClient as MG

#set database
client=MG()
db=client.spider_data
collect=db.lawText

data=collect.find()

for item in data:
    print(item["judgement"]["plaintext"])
    input()

