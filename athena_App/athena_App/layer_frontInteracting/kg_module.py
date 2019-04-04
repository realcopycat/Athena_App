#知识搜索

from athena_App.layer_dataOperating.neo4j_search import neo4jQuery
from athena_App.layer_dataOperating.es_search import searchInEs
from athena_App.layer_dataOperating.ltp_module import ltpTools
from athena_App.layer_dataOperating.mongo_search import mongoSearch
from athena_App.layer_dataOperating.sy_module import senCompare

import operator
#本包可以根据字典值在列表中对字典排序

class knowledgeSearch():

    def __init__(self):

        self.index="baike_data_abstract"
        self.type="knowledge"
        self.key="abstract"
        self.num=20

        self.graphQuery=neo4jQuery()

        self.mongoSearch=mongoSearch()
        self.dbName='spider_data'
        self.collection='baidu_baike_3_test'
        self.collection2='baidu_baike_BIG'

        self.ltpTool=ltpTools()

        self.min_similarity_score=0.5

    def es_presearch(self,des):
        '''
        根据描述进行预搜索
        '''

        result=searchInEs(des,self.index,self.type,self.key,self.num)

        #取出title
        return [a['_source']['title'] for a in result]

    def getDrawingData(self,title_list):
        '''
        接受es预选的实体数据
        返回可供es作图的打包数据
        '''

        total_node=[]
        total_link=[]
        duplicateNodeCheck=set()

        for title in title_list:
            node_list,link_list=self.graphQuery.entityQuery(title)

            for node in node_list:
                tmp_nodeName=node["name"]

                if tmp_nodeName not in duplicateNodeCheck:
                    total_node.append(node)

                duplicateNodeCheck.add(tmp_nodeName)

            for link in link_list:
                total_link.append(link)

        drawingData={}
        drawingData["data"]=total_node
        drawingData["links"]=total_link
        return drawingData

    def getSpecifyData(self,title_list,des):
        '''
        借助pyltp，同时利用es预选的答案，返回mongodb内相关的详细的百科文档数据
        '''

        word_list,tag_list=self.ltpTool.segANDpos(des)

        #得到传入描述的核心词
        coreWord=[]
        for index,tag in enumerate(tag_list):
            if tag in ['n','v']:
                coreWord.append(word_list[index])

        #搜索相关的详细描述
        #这个循环结束后，得到一个列表，列表里的每个元素是每个实体下与描述最为有关的relativeInfo
        relaInfo_forDes=[]
        for title in title_list:
            if self.mongoSearch.singleFieldSearch(self.dbName,self.collection,'title',title):
                singleResult=self.mongoSearch.singleFieldSearch(self.dbName,self.collection,'title',title)
            else:
                singleResult=self.mongoSearch.singleFieldSearch(self.dbName,self.collection2,'title',title)

            singleDoc_specificInfo={}
            #为了应对没有relative_info的情况，使用try
            try:
                list_specifyKeys=list(singleResult['relative_info'].keys())
                
            except Exception as e:
                print(e)
                print(singleResult)
                continue

            #得到一个文档里得分最高的key
            highest_key_score=0
            bestkey=''
            for key in list_specifyKeys:

                highest_score=0 #取出一组词中的最高分
                for eachWord in coreWord:

                    tmp_score=senCompare(eachWord,key)
                    if (tmp_score>highest_score):
                        highest_score=tmp_score
                
                #选出一个文档里最高的key
                if highest_score>highest_key_score:
                    highest_key_score=highest_score
                    bestkey=key

            #经过上面的循环得到这个文档里最合适的relative_info
            try:
                if not singleDoc_specificInfo:
                    singleDoc_specificInfo["info"]=singleResult['relative_info'][bestkey]
                    singleDoc_specificInfo["key"]=bestkey
                    singleDoc_specificInfo["score"]=int(highest_key_score)
                    relaInfo_forDes.append(singleDoc_specificInfo)
            except Exception as e:
                print(e)

        sorted_relainfo=sorted(relaInfo_forDes,key=operator.itemgetter('score'))

       
        return sorted_relainfo

    def getTotalData_forKnowledgeSearch(self,des):

        titleList=self.es_presearch(des)
        totalData={}

        drawingData=self.getDrawingData(titleList)
        totalData["data"]=drawingData["data"]
        totalData["links"]=drawingData["links"]

        #最后那个框是一个切片操作
        totalData["specificData"]=self.getSpecifyData(titleList,des)[0:5:1]
        print(totalData["specificData"])

        return totalData













