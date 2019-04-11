#search in the neo4j database

from neo4j import GraphDatabase as GD
import random
import synonyms as sy
from athena_App.openlaw.fact_triple_1 import *

class caseGraphQuery():
    #query in case graph

    def __init__(self):

        #initialize the database
        self.driver=GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

        #start query session
        self.session=self.driver.session()

        #triple catch
        self.extor=TripleExtractor()

    def tripleQuery_Main(self,des):
        '''解析主函数'''

        des_triples=self.extor.triples_main(des)

        return self.DEBUGGING_Qurey(des[1])

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
        #数据统计：总计数
        titleSet=set()

        for record in directRes:
            
            title=record["b"]._properties["belong"]
            titleSet.add(title)
            print(title)
            #暂取最后一个答案

        totalcase=len((list(titleSet)))

        title=random.sample(titleSet,1)[0]


        #取出整个案例的图谱
        finalRes=self.session.run("MATCH (a:Des {belong: $title})-[b {belong: $title}]->(c:Des {belong: $title})"
                                  "RETURN a,b,c",
                                  title=title)

        #用来储存最终的案例图谱数据
        link_list=[]
        node_list=[]

        #控制节点大小
        node_count={}

        #统计匹配的关系数
        link_pick=0

        for record in finalRes:
            
            #取出node标签数据
            tmpNode1=record["a"]._properties["text"]
            tmpNode2=record["c"]._properties["text"]
            node_list.append(tmpNode1)
            node_list.append(tmpNode2)

            #抽出linkType数据
            tmpLink=record["b"].type
            print(tmpLink)
            linkItem={}
            linkItem["source"]=tmpNode1
            linkItem["target"]=tmpNode2
            linkItem["value"]=tmpLink

            linkItem["label"]={}
            linkItem["label"]["normal"]={}
            linkItem["label"]["normal"]["show"]=True
            linkItem["label"]["normal"]["formatter"]=tmpLink

            if tmpLink==test_word:
                linkItem["lineStyle"]={}
                linkItem["lineStyle"]["normal"]={}
                linkItem["lineStyle"]["normal"]["color"]="#34E52D"
                linkItem["label"]["normal"]["color"]="#34E52D"

                link_pick+=1


            try:
                node_count[tmpNode1] +=1
            except:
                node_count[tmpNode1]=0

            if tmpNode2 not in node_count:
                node_count[tmpNode2]=0

            link_list.append(linkItem)

        node_set=list(set(node_list))
        node_data=[]

        #数据统计部分：node
        node_short=0
        node_long=0
        node_text=0

        #数据统计部分：link
        link_A=0
        link_B=0
        link_C=0
        link_D=0

        for node in node_set:
            data={}
            data["name"]=node
            data["draggable"]=True

            if node_count[node]>=10:
                link_A+=1
            elif ((node_count[node]>=6)&(node_count[node]<10)):
                link_B+=1
            elif ((node_count[node]>=3)&(node_count[node]<6)):
                link_C+=1
            elif ((node_count[node]>=0)&(node_count[node]<3)):
                link_D+=1
            

            if len(node)>=15:
                data["category"]="text"
                node_text=node_text+1
            elif ((len(node)>=7)&(len(node)<15)):
                data["category"]="long"
                node_long=node_long+1
            elif ((len(node)>0)&(len(node)<7)):
                data["category"]="short"
                node_short=node_short+1

            if node_count[node]==0:
                data["symbolSize"]=30
            else:
                data["symbolSize"]=30+node_count[node]*3

            node_data.append(data)

        #数据统计部分:node
        nodeStat=[{"value":node_short,"name":'短文本节点'},
                 {"value":node_long,"name":'长文本节点'},
                 {"value":node_text,"name":'描述性节点'}]
        print(nodeStat)

        #数据统计部分：link
        linkStat=[{"name":'A级节点',"value":link_A},
                  {"name":'B级节点',"value":link_B},
                  {"name":'C级节点',"value":link_C},
                  {"name":'D级节点',"value":link_D},]
        print(linkStat)

        #数据统计部分：All
        node_total=node_long+node_short+node_text
        link_total=link_A+link_B+link_C+link_D
        allStat=[totalcase,node_total,link_total,node_short,node_long,node_text,link_pick]



        final={"data":node_data,"links":link_list,"nodeAnalyse":nodeStat,
               "linkAnalyse":linkStat,"totalStat":allStat}

        return final


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

    

   