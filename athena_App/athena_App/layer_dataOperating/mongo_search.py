#获取Mongodb 的数据

from pymongo import MongoClient as MG

class mongoSearch():

    def __init__(self):

        self.client=MG()

    def singleFieldSearch(self,db_name,collect,key,value):
        '''
        指定数据库名称，collection，键值，以及查找的关键字
        返回整个查询结果，但是只有一个
        '''

        #初始化查询范围
        db=self.client[db_name]
        collection=db[collect]

        #直接返回单个文档
        querySet={key:value}
        return collection.find_one(querySet)
