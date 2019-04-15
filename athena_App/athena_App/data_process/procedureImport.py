#过程导入

import csv 
from neo4j import GraphDatabase as GD

driver = GD.driver("bolt://localhost:7687", auth = ("neo4j","123"))

def addData(gr, node1, rela, node2):

    #cypher
    gr.run(
        "MERGE (a:Object {name: $node1})"
        "MERGE (b:Object {name: $node2})"
        "MERGE (a)-[:"+rela+"]->(b)",
        node1 = node1,node2 = node2
        )

path = "C:\\User\\a_080\\Desktop\\test.csv"
csv_file = open(path, 'r')
csvReader=csv.reader(csv_file)

with driver.session() as session:

    for eachline in csvReader:

        print(eachline)
        input()

        try:
            session.write_transaction(addData,eachline[0],eachline[1],eachLine[2])
        except Exception as e:
            print(e)
            print(eachline)

