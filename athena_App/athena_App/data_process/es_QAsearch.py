#elastic search : answer searching module

import os
import time

from elasticsearch import Elasticsearch as ES
import numpy as np 
import jieba.posseg as pseg

from athena_App.data_process.qa_answer import QAanswer

#设置词向量的路径
#注意：从windows下复制下来的路径
#在python里要改成反斜杠
#（\） --> （/）
vecDict_path="E:/BaiduNetdiskDownload/word_vec_300.bin"

def load_vec(path):

    print("[ATTENTION]:\n##正在加载词向量！##\n")

    #初始化字典
    vecDict={}

    count = 0

    #the line below is for those encode by utf-8
    for line in open(path,encoding='UTF-8'):
    #for line in open(path,encoding='gb18030'):

        #此行保持疑问
        line=line.strip().split(' ')
        #print(line)

        #仍保持疑问
        if len(line)<300:
            continue

        #取出这个字
        word=line[0]

        #这个语法是指取第二个开始的元素
        vector=np.array([float(i) for i in line[1:]])

        #把向量弄到词典里
        vecDict[word]=vector

        count +=1

        if count%10000 == 0:
            print("加载完毕？")

        if count>10000000:
            break

    print("加载了%s个词"%count,)

    return vecDict

#预加载词向量

vecDict=load_vec(vecDict_path)

class answerFinder():

    def __init__(self):

        #可修改:需要从哪个索引中查找
        self._index="qa_data"

        #可修改，es服务器设置
        self.es=ES([{"host":"127.0.0.1","port":9200}])

        #寻找的文档的属性
        self.doc_type="qa"

        #设定句子向量空间的维数
        self.embedSize=300

        #匹配的分数控制
        self.min_score=0.4
        self.min_sim=0.4

    def queryInES(self,question,key="question"):
        '''构造请求并在es中执行搜索'''

        #构造请求结构
        query_body={
            "query":{
                "match":{
                    key:question
                    }
                }
            }

        #在es中搜索
        result=self.es.search(index=self._index,doc_type=self.doc_type,body=query_body,size=40)

        return result["hits"]["hits"]

    def search_es(self,question):
        '''调用queryInES来返回答案，并对答案做一定的处理'''

        answer=[]

        #search in ES
        result=self.queryInES(question)

        #process the result
        for each in result:

            #use dict to store every answer
            answer_dict={}

            #build answer dict
            answer_dict["score"]=each["_score"]
            answer_dict["sim_question"]=each["_source"]["question"]
            answer_dict['answer']=each["_source"]["answer"]
            
            answer.append(answer_dict)

        #return a list which contains formalized answer with a score
        return answer

    def sentencePreCut(self,st):
        '''select word by its POS tag'''

        #we use jieba now ,but Standford's tools seems better
        wds=[i.word for i in pseg.cut(st) if i.flag not in ['x','u','c','p','m','t']]

        return wds

    def sentenceVector(self,sentence,tag="cut"):
        '''create a vector which represent a sentence ,based on word2vec'''

        if tag == 'cut':

            #this line make no sense in this class ,delete it later
            word_list=[i for i in sentence.split(' ') if i]

        else:

            #if the sentence is completely raw ,cut it
            word_list=self.sentencePreCut(sentence)

        #initialize the sentence vector
        stVector=np.zeros(self.embedSize)

        #record the lenth of sentence
        stLen=0

        for index,wd in enumerate(word_list):

            #if the word is in our dict,add its vector into the stVector
            if wd in vecDict:

                #Important!!#

                #this line explain the reason why we don't need the vector whose dimension is less than 300
                #because we need add this vector into a same matrix,we must keep it in a same standard
                stVector +=vecDict.get(wd)

                #count the length
                stLen +=1
            else:
                #discard the word we don't have
                continue

        return stVector,stLen

    def simByVector(self,v1,v2):
        '''calculate the similarity of two sentence by vector'''

        #calculate the vectorical angle cosine
        #numpy provide a faster way to calculate it ,change the function here later
        dot_product=np.sum(v1*v2)
        norm1=np.sqrt(sum(v1**2))
        norm2=np.sqrt(sum(v2**2))

        similarity=dot_product/float(norm1*norm2)

        #if the result is infinity,return 0
        if similarity=='nan':
            return 0
        else:
            return similarity

    def main(self,question):
        '''the main function in this class'''

        #create a answer object
        ans_object=QAanswer()

        #search answer in ES
        es_result=self.search_es(question)

        #calculate the stVector of question
        questionVec,question_len=self.sentenceVector(question,tag="noCut")

        #to store final answer
        answer_dict={}

        #answerRank
        r1=0
        r2=0
        r3=0

        for indx,item in enumerate(es_result):
            
            #fetch out the question
            tmp_question=item["sim_question"]

            score=item["score"]/100

            tmp_questionVec,tmp_len=self.sentenceVector(tmp_question,tag="noCut")

            #the similarity between two sentence
            sim=self.simByVector(questionVec,tmp_questionVec)

            #if the result has reach the lowest standard,accept it
            if sim>self.min_sim:
                if sim>r1:
                    ans_object.bestAnswer=item["answer"]
                    ans_object.matchQ1=item["sim_question"]
                    r1=sim
                    continue
                if sim>r2:

                    #if the answer is the same with best answer ,discard it
                    if ans_object.matchQ1==tmp_question:
                        continue

                    ans_object.secAnswer=item["answer"]
                    ans_object.matchQ2=item["sim_question"]
                    r2=sim
                    continue
                

        #if we don't have any answer for it 
        if ans_object.bestAnswer=='':
            ans_object.bestAnswer='请您到公安机关咨询'
        else:
            return ans_object


