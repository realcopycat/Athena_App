#search in the neo4j database

from neo4j import GraphDatabase as GD
#import synonyms as sy
#from athena_App.openlaw.fact_triple_1 import *

class caseGraphQuery():
    #query in case graph

    def __init__(self):

        #initialize the database
        self.driver=GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

        #start query session
        self.session=self.driver.session()

        #triple catch
        #self.extor=TripleExtractor()

    def tripleQuery_Main(self,des):
        '''解析主函数'''

        #des_triples=self.extor.triples_main(des)

        return self.DEBUGGING_Qurey(des)

    def DEBUGGING_Qurey(self,test_word):
        '''
        只能用于前端测试！！！！！！

        暴力直接查询,就以关系名为查询突破口！！！！！！！

        假设数据库中有一个关系完全一样！！！！！！！

        而且假设用户输入的描述只能解析出一个三元组！！！！！

        实际中绝对不可用！！！！！！！！

        妈的垃圾！

        这是用于最最最最最最简单的情况下的前端图谱测试函数！！！！！！！

        绝对不可用！！！！！！11

        '''

        directRes=self.session.run("MATCH (a:Des)-[b:"+test_word+"]->(n:Des)"
                                   "RETURN b")

        for record in directRes:
            
            title=record["b"]._properties["belong"]
            #直接就取第一个答案
            break

        #取出整个案例的图谱
        finalRes=self.session.run("MATCH (a:Des {belong: $title})-[b {belong: $title}]->(c:Des {belong: $title})"
                                  "RETURN a,b,c",
                                  title=title)

        #用来储存最终的案例图谱数据
        link_list=[]

        for record in finalRes:
            
            #取出node标签数据
            tmpNode1=record["a"]._properties["text"]
            tmpNode2=record["c"]._properties["text"]

            #抽出linkType数据
            tmpLink=record["b"].type
            print(tmpLink)
            linkItem={}
            linkItem["source"]=tmpNode1
            linkItem["target"]=tmpNode2
            linkItem["rela"]=tmpLink
            linkItem["type"]="resolved"

            

            link_list.append(linkItem)

        return link_list


    def formalQurey(self,triple_list):
        '''有待拓展的正式方法'''

        relaResult=self.session.run("MATCH (:Des)-[a]->(:Des)"
                                    "RETURN a")

        relaScore=0
        maxRela=''

        for record in relaResult:
            print(record["a"].type)
            tmp_rela=record["a"].type
            tmp_score=sy.compare(tmp_rela,des)
            if relaScore<tmp_score:
                relaScore=tmp_score
                maxRela=tmp_rela

        print(maxRela)

    

   