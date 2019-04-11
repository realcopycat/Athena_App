#建造关键词

from pymongo import MongoClient as MG
import jieba

def build():
    client=MG()
    db=client.spider_data
    collect=db.baiduQaFormal
    data=collect.find()

    for item in data:
        precut=item['title']

        print(precut)
        cutted=jieba.lcut(precut,cut_all=True)

        collect.update({"_id":item["_id"]},{"$set":{"keyword":cutted}})

build()
