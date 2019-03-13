#build graph by data in the mongo

from neo4j import GraphDatabase as GD
from pymongo import MongoClient as MC

#initialize the database driver
driver=GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

#initialize the mongodb`
client=MC()
db=client.spider_data
collect=db.baidu_baike_3_test

#write in graph`
def addData(gr,node1,rela,node2):

    #cypher script
    gr.run("MERGE (a:Node {name: $node1})"
           "MERGE (b:Node {name: $node2})"
           "MERGE (a)-[:"+rela+"]->(b)",
           node1=node1,node2=node2)

with driver.session() as session:
    
    count=0

    #read data in the mongodb
    dataSet=collect.find()

    for item in dataSet:
        node1=item['title']
        infoSet=item['basic_info']

        #search every key-value pair
        for key,value in infoSet.items():
            rela=key
            node2=value

            #execute cypher script
            try:
                session.write_transaction(addData,node1,rela,node2)
            except Exception as e:
                print(node1,rela,node2,e)

            count +=1

            if count%100==0:
                print("loaded")




