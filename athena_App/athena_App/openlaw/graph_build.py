#build graph of law text

from neo4j import GraphDatabase as GD
from pymongo import MongoClient as MC

#initialize the database driver
driver=GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

#initialize the mongodb
client=MC()
db=client.spider_data
collect=db.lawTextTriple

def addTripleData(gr,node1,rela,node2,title):

    #cypher script
    gr.run("MERGE (a:Des {text: $node1,belong: $title})"
           "MERGE (b:Des {text: $node2,belong: $title})"
           "MERGE (a)-[:"+rela+"{belong: $title}]->(b)",
           node1=node1,node2=node2,title=title)

with driver.session() as session:

    count=0

    #read data in the mongodb
    dataSet=collect.find()

    for item in dataSet:

        #read triple list
        triples=item['triples']
        title=item["title"]

        for triple in triples:

            try:
                session.write_transaction(addTripleData,triple[0],triple[1],triple[2],title)
            except Exception as e:
                print(triple[0],triple[1],triple[2],title,e)

            count +=1

            if count%100==0:
                print("Executing!")



