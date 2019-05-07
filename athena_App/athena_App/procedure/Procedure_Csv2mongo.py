#过程csv导入

import csv
from pymongo import MongoClient as MC
from neo4j import GraphDatabase as GD

path = "C:\\Users\\a_080\\Desktop\\procedure\\1.csv"

csv_file = open(path, 'r', encoding='UTF-8')
csvReader = csv.reader(csv_file)

client = MC()
db = client.spider_data
collection = db.procedure

count = 0
reslist = list()
for eachline in csvReader:
    count = count + 1
    
    if count==1:
        title = eachline[0]
    else:
        eachdict = {}
        eachdict['source'] = eachline[0]
        eachdict['rela'] = eachline[1]
        eachdict['target'] =eachline[2]
        reslist.append(eachdict)

print(reslist)

#data = {'title':title, 'dictpack':reslist}
#collection.insert_one(data)

driver = GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

with driver.session() as session:
    for each in reslist:
        rela = each['rela']
        nodetag = rela.split('To')
        nodename1 = each['source']
        nodename2 = each['target']
        if len(nodetag) == 2:
            nodetag1 = nodetag[0]
            nodetag2 = nodetag[1]
            
            mergeRES=session.run('MERGE (a: '+nodetag1+' {name: $name1})'
                        'MERGE (b: '+nodetag2+' {name: $name2})'
                        'MERGE (a)-[:'+rela+']-(b)'
                        'RETURN a,b',
                        name1 = nodename1, name2 = nodename2)
            print(type(mergeRES))

            for record in mergeRES:
                try:
                    exist_title=record['a']._properties['belong']
                    print(type(title))
                    if title not in exist_title:
                        exist_title.append(title)
                        session.run('MATCH (a: '+nodetag1+' {name: $name1}) SET a.belong='+exist_title+'}',
                                name1 = nodename1)
                except KeyError as e:
                    session.run('MATCH (a: '+nodetag1+' {name: $name1}) SET a += {belong:["'+title+'"]}',
                                name1 = nodename1)
                try:
                    exist_title=record['b']._properties['belong']
                    if title not in exist_title:
                        exist_title.append(title)
                        session.run('MATCH (a: '+nodetag2+' {name: $name2}) SET a.belong='+exist_title+'}',
                                name2 = nodename2)
                except KeyError as e:
                    session.run('MATCH (a: '+nodetag2+' {name: $name2}) SET a += {belong:["'+title+'"]}',
                                name2 = nodename2)

        else:
            mergeRES=session.run('MATCH (a {name: $name1})'
                        'MATCH (b {name: $name2})'
                        'MERGE (a)-[:'+rela+']-(b)'
                        'RETURN a.title,b.title',
                        name1 = nodename1, name2 = nodename2)
            print(type(mergeRES))



   