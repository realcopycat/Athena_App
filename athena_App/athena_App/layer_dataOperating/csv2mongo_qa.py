#处理csv的脚本


from pymongo import MongoClient as MG
import csv

path="C:\\Users\\a_080\\Desktop\\case\\qa1.csv"

csv_file=open(path,'r', encoding='UTF-8')
csvReader=csv.reader(csv_file)

dataInRow=[]

client=MG()
db=client.spider_data
collection=db.qa_byHand

for eachLine in csvReader:
    print(eachLine)

    tmp_data_dict={}

    tmp_data_dict['title']=eachLine[0]
    tmp_data_dict['answer']=eachLine[1]

    collection.insert_one(tmp_data_dict)
