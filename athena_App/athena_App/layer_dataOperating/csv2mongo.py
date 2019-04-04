#处理csv的脚本


from pymongo import MongoClient as MG
import csv

path="C:\\Users\\a_080\\Desktop\\case\\case8.csv"

csv_file=open(path,'r', encoding='UTF-8')
csvReader=csv.reader(csv_file)

dataInRow=[]

client=MG()
db=client.spider_data
collection=db.tagged_case

for eachLine in csvReader:
    print(eachLine)

    tmp_data_dict={}
    if eachLine[0]:
        tmp_data_dict["title"]=eachLine[0]

    if eachLine[1]:
        tmp_data_dict["plainText"]=eachLine[1]

    if eachLine[2]:
        tmp_data_dict["city"]=eachLine[2]

    if eachLine[3]:
        tmp_data_dict["region"]=eachLine[3]

    if eachLine[4]:
        tmp_data_dict["province"]=eachLine[4]

    if eachLine[5]:
        tmp_data_dict['age']=eachLine[5]

    if eachLine[6]:
        tmp_data_dict["gender"]=eachLine[6]

    if eachLine[7]:
        tmp_data_dict["job"]=eachLine[7]

    if eachLine[8]:
        tmp_data_dict["month"]=eachLine[8]

    if eachLine[9]:
        tmp_data_dict["festival"]=eachLine[9]

    if eachLine[10]:
        tmp_data_dict["duration"]=eachLine[10]

    if eachLine[11]:
        tmp_data_dict["amont"]=eachLine[11]

    if eachLine[12]:
        tmp_data_dict["method"]=eachLine[12]

    if eachLine[13]:
        tmp_data_dict["type"]=eachLine[13]

    collection.insert_one(tmp_data_dict)

        