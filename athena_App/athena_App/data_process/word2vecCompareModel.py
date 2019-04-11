#词向量比对推荐模块

#from athena_App.VAR import *
import jieba.posseg as pseg

import numpy as np
from scipy.linalg import norm
from pymongo import MongoClient as MG
import gensim

model_file = 'C:/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True,limit=200000)
print('词向量模型已加载')
flag=['n','r','t','m','c','a','d','p']

class Answer():
     def __inti__(self):
         self.bestAnswer=''
         self.matchQ1=''
         self.best=0
         self.secAnswer=''
         self.matchQ2=''
         self.sec=0

def vector_similarity(s1, s2):
    def sentence_vector(s):
        words = []
        wordss = pseg.cut(s)
        for w in wordss:
            if w.flag in flag:
                words.append(w.word)
        v = np.zeros(64)
        for word in words:
            try:
                v += model[word]
            except:
                v = v
        v /= len(words)
        return v
    
    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    
    return np.dot(v1, v2) / (norm(v1) * norm(v2))
    

def vecCompare(cs):
    client=MG()
    db=client.spider_data
    collect=db.baiduqa_
    data=collect.find()

    #设置答案对象
    answer=Answer()

    #初始化比较值
    sim_best=0
    sim_sec=0

    for item in data:

        #两个问句的相似度比较
        sim_num=vector_similarity(item['pureQstr'],cs)

        if sim_num>sim_best:
            answer.matchQ1=item['title']
            answer.bestAnswer=item['answer']
            sim_best=sim_num
            continue
        if sim_num>sim_sec:
            answer.matchQ2=item['title']
            answer.secAnswer=item['answer']
            sim_sec=sim_num

    return answer
