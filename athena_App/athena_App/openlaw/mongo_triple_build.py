# put triple into the mongodb

from athena_App.openlaw.fact_triple_1 import *
from pymongo import MongoClient as MC

client=MC()
db=client.spider_data

collect=db.lawText
writeCollect=db.lawTextTriple

data=collect.find()

check=writeCollect.find()

extor=TripleExtractor()

for item in data:

    set=0
    for each in check:
        if each['title']==item['judgement']['title']:
            set=1
            check=writeCollect.find()
            break

    check=writeCollect.find()

    if set==0:
        content=item["judgement"]["plaintext"]
        triples=extor.triples_main(content)
        insertData={"title":item["judgement"]["title"],"triples":triples}
        writeCollect.insert_one(insertData)
        print("成功写入一个文档！")