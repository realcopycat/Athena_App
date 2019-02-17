#机器人本地测试脚本

import aiml
import os
import jieba
import jieba.posseg as pseg
from pymongo import MongoClient as MG

class AiRobot():

    def __init__(self):
        mybot_path='./'
        self.mybot=aiml.Kernel()
        pathZ=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        print(pathZ)

        #加载机器人对答模板文件
        self.mybot.learn(pathZ+'/COMM_robot/std-startup.xml')
        self.mybot.learn(pathZ+'/COMM_robot/Common_conversation.aiml')
        self.mybot.learn(pathZ+'/COMM_robot/question_analyse.aiml')

        #加载预制字典
        jieba.load_userdict(pathZ+'/COMM_robot/text_dict.txt')

        #mongodb配置
        client=MG()
        db=client.spider_data
        self.collect=db.baidu_baike_3_test

    def start(self):
        while True:
            question=input()

            #预处理文本
            text=self.textProcess(question)

            #让模板系统解析
            print("text:"+text)
            answer=self.mybot.respond(text)

            print('解析结果是:'+answer)

            if answer=='':
                print('fail')
            elif answer[0]=='!':
                answer=self.identifyAnswer(answer)
            
    def identifyAnswer(self,answer):
        
        print('进入数据库查找答案！')

        preCut=answer.split(':')

        entity=str(preCut[1]).replace(" ",'')

        attr=str(preCut[2]).replace(" ",'')

        print("\n实体是："+entity)
        print("属性是："+attr+'\n')

        self.findInDatabase(entity,attr)

    def findInDatabase(self,entity,attr):

        data=self.collect.find()

        for item in data:
            if not item['title']==entity:
                continue
            else:
                print('已找到实体')

                keys=[]
                dict_BI=list(item['basic_info'].keys())
                dict_RI=list(item['relative_info'].keys())

                if attr in dict_BI:
                    print('属性已找到')
                    print(item['basic_info'][attr])
                    break
                if attr in dict_RI:
                    print('属性已找到')
                    print(item['relative_info'][attr])
                    break

                print('未找到属性')

    def textProcess(self,text):

        #分词,得到一个词与词之间用空格分开的句子
        text=text.strip()
        word_itor=jieba.cut(text)
        word_result=" ".join(word_itor)
        return word_result
       

bot=AiRobot()
bot.start()
