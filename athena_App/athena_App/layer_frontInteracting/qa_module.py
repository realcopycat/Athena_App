#问答库中搜索答案

from athena_App.layer_dataOperating.es_search import searchInEs 
from athena_App.layer_dataOperating.sy_module import senCompare
from athena_App.layer_frontInteracting.qa_answer import QAanswer

#为了抽取指定元素
import heapq

class answerFinder():

    def __init__(self):

        #可修改:需要从哪个索引中查找
        self._index="qa_data"
        self._indexCase="news_case"

        #寻找的文档的属性
        self.doc_type="qa"
        self.doc_type_case='case'

        #最低分数控制
        self.minScore=0.4

        #es搜寻字段
        self.targetKey="question"
        self.caseKey='plaintext'

        #es预选答案个数
        self.num_res=30

    def findAnswer(self,des):
        '''答案查找主函数'''

        result=searchInEs(des,self._index,self.doc_type,self.targetKey,self.num_res)

        answer=[]
        #process the result
        for each in result:

            #use dict to store every answer
            answer_dict={}

            #build answer dict
            answer_dict["score"]=each["_score"]
            answer_dict["sim_question"]=each["_source"]["question"]
            answer_dict['answer']=each["_source"]["answer"]
            
            answer.append(answer_dict)

        #return 这一句里的作用是字典去重
        return [dict(t) for t in set([tuple(d.items()) for d in answer])]

    def pickAnswer(self,answer_list,num_pick,des):
        '''
        第一个参数是self.findAnswer的结果
        第二个参数是需要挑选的答案的个数
        第三个参数是问题的描述
        '''

        print(answer_list)
        #分数的列表
        score_list=[]

        #目标答案的列表
        target_answer=[]

        #写入分数
        for answer_item in answer_list:
            score_list.append(senCompare(des,answer_item["sim_question"]))

        #获取指定个数内的答案
        for index_ofDict in list(map(score_list.index,heapq.nlargest(num_pick,score_list))):
            if score_list[index_ofDict]>self.minScore:
                target_answer.append(answer_list[index_ofDict])
                print(index_ofDict)

        return target_answer

    def findANDpack(self,des):
        '''
        view函数直接调用的函数
        '''
        result=self.pickAnswer(self.findAnswer(des),2,des)
        answer=QAanswer()

        answer.bestAnswer=result[0]["answer"]
        answer.matchQ1=result[0]["sim_question"]
        answer.best=0
        answer.secAnswer=result[1]["answer"]
        answer.matchQ2=result[1]["sim_question"]
        answer.sec=0

        caseResult=self.pickCase(des)
        answer.title=caseResult[0]["_source"]["title"]
        answer.plaintext=caseResult[0]["_source"]["plaintext"]
        answer.city=caseResult[0]["_source"]["city"]
        answer.region=caseResult[0]["_source"]["region"]
        answer.province=caseResult[0]["_source"]["province"]
        answer.age=caseResult[0]["_source"]["age"]
        answer.gender=caseResult[0]["_source"]["gender"]
        answer.job=caseResult[0]["_source"]["job"]
        answer.month=caseResult[0]["_source"]["month"]
        answer.duration=caseResult[0]["_source"]["duration"]
        answer.amount=caseResult[0]["_source"]["amount"]
        answer.method=caseResult[0]["_source"]["method"]
        answer.type=caseResult[0]["_source"]["type"]

        return answer

    def pickCase(self,des):
        #用于搜索相似的新闻案例，基于Elastic

        result=searchInEs(des,self._indexCase,self.doc_type_case,self.caseKey,1)

        return result

