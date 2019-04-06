#案件查找模块

from athena_App.layer_dataOperating.es_search import searchInEs
from athena_App.layer_dataOperating.neo4j_search import neo4jQuery
from athena_App.layer_dataOperating.textParse_module import TripleExtractor
from athena_App.layer_dataOperating.sy_module import senCompare
from athena_App.layer_dataOperating.mongo_search import mongoSearch
import re

class caseQuery():

    def __init__(self,des):
        '''初始化模块'''

        self.graphQuery=neo4jQuery()
        self.parser=TripleExtractor()

        self.index='case_data'
        self.docType='caseText'
        self.key='abstract'
        self.res_limit=10
        self.des=des

        self.rela_score=0.7
        #达到标准分数就不再检索，直接返回答案，加快速度
        self.score_standard=0.8

    def es_preSearch(self):
        '''ES预搜索'''

        result=searchInEs(self.des,self.index,self.docType,self.key,self.res_limit)

        title_list=[]
        for res in result:
            title_list.append(res['_source']['title'])

        return title_list

    def destriptionParse(self):
        '''解析传入的描述'''

        return self.parser.triples_main(self.des)

    def titlePick(self):
        '''挑一个最好的title'''

        try:
            relaPick=self.destriptionParse()[1]

        #为了防止三元组解析失效，
        except Exception as e:
            print(e)
            relaPick=self.des

        highestScore=0
        highestTitle=''
        relative_relation=set()
        for title in self.es_preSearch():
            result=self.graphQuery.attrQuery('belong',title)

            title_score=0
            for record in result:
                tmp_score=senCompare(record["b"].type,relaPick)
                if title_score<tmp_score:
                    title_score=tmp_score

                if tmp_score>self.rela_score:
                    relative_relation.add(record["b"].type)

            if title_score>highestScore:
                highestScore=title_score
                highestTitle=title

            if title_score>self.score_standard:
                break
        #为了getTextData可以访问,特地设置成员
        self.bestTitle=highestTitle
        self.bestScore=highestScore

        return highestTitle,list(relative_relation)

    def pickBestGraph(self):
        '''调用后输出最好的画图数据'''

        coreTitle,coreRela=self.titlePick()
        graphData=self.graphQuery.attrQuery('belong',coreTitle)

        node_list=[]
        link_list=[]
        #控制节点大小
        node_count={}
        #统计匹配的关系数
        link_pick=0
        for record in graphData:
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

            if tmpLink in coreRela:
                linkItem["lineStyle"]={}
                linkItem["lineStyle"]["normal"]={}
                linkItem["lineStyle"]["normal"]["color"]="#34E52D"
                linkItem["label"]["normal"]["color"]="#34E52D"

                link_pick+=1

            link_list.append(linkItem)

            #链接计数
            try:
                node_count[tmpNode1] +=1
            except:
                node_count[tmpNode1]=0

            if tmpNode2 not in node_count:
                node_count[tmpNode2]=0

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
        allStat=[self.res_limit,node_total,link_total,node_short,node_long,node_text,link_pick]

        final={"data":node_data,"links":link_list,"nodeAnalyse":nodeStat,
               "linkAnalyse":linkStat,"totalStat":allStat}

        return final

    '''
        获取数据的主函数
    '''
    def getData(self):
        '''
            试图综合画图数据以及文字标签数据
        '''

        graphData=pickBestGraph()

    '''
        解析标签数据
    '''
    def getTextData(self):
        '''
            根据es预选的结果
            给出匹配度
            给出可能的判决
            给出可能相关的法条
        '''
        #以下函数的参数决定于数据库设置,注意这里对于嵌套字典的索引方式
        singleDoc=mongoSearch.singleFieldSearch('spider_data','lawText','judgement.title',self.bestTitle)

        textDataDict=dict()
        #相似度计算，算法待优化
        textDataDict["score"]=self.bestScore
        #现成的基本信息
        textDataDict["judgeDate"]=singleDoc['judgement']['judgeDate']
        textDataDict["court"]=singleDoc['judgement']['court']
        textDataDict['title']=singleDoc['judgement']['title']
        textDataDict['caseNo']=singleDoc['judgement']['caseNo']
        #需要RE解析的信息
        puretext=singleDoc['judgement']['plaintext']
        try:
            textDataDict['prosecutor']=re.search('(?<=公诉机关).*?((?=\\r)|(?=。))',puretext).group(0)
        except:
            pass
        try:
            textDataDict["defendant"]=re.search('(?<=被告人).*?(?=，)',puretext)
        except:
            pass


            







