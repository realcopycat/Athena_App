from pymongo import MongoClient as MG
import jieba

client=MG()
db=client.spider_data
collect=db.baidu_baike_3_test

data=collect.find()

for item in data:
    list1=item['title']
    list2=list(item['basic_info'].keys())
    list3=list(item['relative_info'].keys())

    
    with open('./athena_App/COMM_robot/text_dic.txt','a') as f:
        f.write(list1+' '+'3\n')

        for str in list2:
            f.write(str+' '+'3\n')

        for str in list3:
            f.write(str+' '+'3\n')

         
    
    