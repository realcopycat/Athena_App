#做关键词的比对，交集决定答案好坏

from pymongo import MongoClient as MG
import jieba

class Answer():
     def __inti__(self):
         self.bestAnswer=''
         self.matchQ1=''
         self.best=0
         self.secAnswer=''
         self.matchQ2=''
         self.sec=0

def Keyword_Compare(cs):
    client=MG()
    db=client.spider_data
    collect=db.baiduqa_
    data=collect.find()

    collect2=db.baiduQaFormal
    data2=collect2.find()

    csx=jieba.lcut(cs,cut_all=True)

    tmplen=0
    best=0
    sec=0
    bestAns=''
    matchQ1=''
    secAns=''
    matchQ2=''

    for item in data:
        lx=item['keyword']
        ret=[x for x in csx if x in lx ]
        tmplen=len(ret)

        if tmplen>best:
            matchQ1=item['title']
            bestAns=item['answer']
            best=tmplen
            continue
        if tmplen>sec:
            matchQ2=item['title']
            secAns=item['answer']
            sec=tmplen

    for item in data2:
        lx=item['keyword']
        ret=[x for x in csx if x in lx ]
        tmplen=len(ret)

        if tmplen>best:
            matchQ1=item['title']
            bestAns=item['answer']
            best=tmplen
            continue
        if tmplen>sec:
            matchQ2=item['title']
            secAns=item['answer']
            sec=tmplen

    answer=Answer
    answer.bestAnswer=bestAns
    answer.matchQ1=matchQ1
    answer.best=best
    answer.secAnswer=secAns
    answer.matchQ2=matchQ2
    answer.sec=sec

    return answer

