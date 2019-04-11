#本函数被设计为通用函数，用于给es建立索引并导入数据
#需要具体修改本文件以适应具体情况
#执行本脚本集合直接完成导入操作，执行前确认mongo的数据及相关服务是否开启

import time
from elasticsearch import Elasticsearch as ES
from elasticsearch.helpers import bulk
from pymongo import MongoClient as MG

class dataImporter():
    '''用于在mongodb和elastic之间转接导入数据'''

    def __init__(self):
        '''初始化设置'''

        #可修改：定义索引名称
        self._index="law_data"

        #可修改，但一般不需要，定义es服务器设置
        self.es=ES([{"host":"127.0.0.1","port":9200}])

        #可修改：定义文档类型
        self.doc_type="line"

        #无需修改，链接mongodb
        self.MGclient=MG()

        #可修改，指定数据库名称
        self.db=self.MGclient.spider_data

        #可修改,指定collection的名称
        self.collect=self.db.LAW

    def create_mapping(self):
        '''用于创建映射'''

        #可修改，定义映射的具体内容，需要根据mongodb的内容来具体修改
        data_mapping={
            "mappings":{
                #指定文档类型 #注意！据说是官方已不再建议使用的一种特性
                self.doc_type:{
                    "properties":{
                        "LawTitle":{

                            #type indicates the type of this field
                            #不能使用string，这是版本问题，text似乎表示可以索引的意思
                            "type":"text",

                            #ik是一个需要另外安装的中文分词器
                            "analyzer":"ik_max_word",

                            #指定搜索时可用在可分词字段的分词器
                            "search_analyzer":"ik_smart",

                            #决定字段是否可以被用户搜索
                            "index":False

                            },#注意此处的逗号！

                        "lineNo":{

                            #同上
                            "type":"text",

                            "analyzer":"ik_max_word",

                            "search_analyzer":"ik_smart",

                            "index":False

                            },
                        
                        "line":{

                            #同上
                            "type":"text",

                            "analyzer":"ik_max_word",

                            "search_analyzer":"ik_smart",

                            "index":True

                            },

                        }
                    }
                }}

        #如果不存在该名称的索引则进行下一步
        if not self.es.indices.exists(index=self._index):

            #如果不存在则建立索引
            self.es.indices.create(index=self._index,body=data_mapping)

            print("create {} mapping successfully!".format(self._index))

        else:

            #如果已存在，则打印相关的消息
            print("index: {} has already create!".format(self._index))

    def insert_data(self,data_list):
        '''插入数据'''

        #bulk插入操作,关键在于bulk支持一个可迭代对象的插入
        try:
            success,_=bulk(self.es,data_list,index=self._index,raise_on_error=True)
        except Exception as e:
            print(e)
            input()

        #print("execute insert {0} operation :{1}".format(success,_))

def main_exe():
    '''插入数据的主执行函数'''

    #工作对象初始化
    worker=dataImporter()

    #创建mapping
    worker.create_mapping()

    #工作记时
    start=time.time()

    #初始化参数
    index=0
    count=0
    data_list=[]

    #用于设置数据列表达到多少个的时候执行一次插入
    list_max=10

    #构建遍历游标
    qaData=worker.collect.find(no_cursor_timeout=True)

    #执行插入
    for item in qaData:
        index +=1
        print(index)

        for line in item['content']:
            #制造插入es的数据
            action={
                "_index":worker._index,
                "_type":worker.doc_type,
                "_source":{
                    "LawTitle":item['name'],
                    "lineNo":line['lineNo'],
                    "line":line['line']
                    }
                }

            data_list.append(action)

            #一旦达到设置的上限就执行插入
            if index>list_max:

                #input()
                worker.insert_data(data_list)
                #input()

                index=0
                count +=1
            
                print(count)

                #重置
                data_list=[]

    end=time.time()

    print("Time Cost:{}".format(end-start))

main_exe()