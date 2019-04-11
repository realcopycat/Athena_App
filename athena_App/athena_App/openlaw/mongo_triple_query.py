#search the most suitable case for user

from athena_App.openlaw.fact_triple_1 import *
from pymongo import MongoClient as MC
import synonyms as sy

class tripleQuery():
    '''做三元组查询的类'''

    def __init__(self):
        '''initialize the database'''

        self.client=MC()
        self.db=self.client.spider_data
        self.collect=self.db.lawTextTriple

        self.extor=TripleExtractor()

    def matchBestTriple(self,des):
        '''match best triple by synonyms'''

        #analyse the question's triples
        des_triples=self.extor.triples_main(des)

        data=self.collect.find()

        #document's max score 
        domMaxScore=0
        domTitle=''

        for each in data:

            #read triple list from document
            triple_list=each["triples"]

            #set every documents score
            scoreSum=0

            #calculate a score for every triple in document
            for eachTriple in des_triples:

                #对于单个的三元组的评分
                single_triple_score=0
                
                relaScore=0
                n1Score=0
                n2Score=0

                for Triple in triple_list:

                    #calculate the score of relation description
                    relation_score=sy.compare(Triple[1],eachTriple[1],seg=True)
                    if relation_score<relaScore:
                        relaScore=relation_score

                    #calculate the similarity of two node
                    node1_score=sy.compare(Triple[2],eachTriple[2],seg=True)
                    node2_score=sy.compare(Triple[0],eachTriple[0],seg=True)
                    if n1Score>node1_score:
                        n1Score=node1_score
                    if n2Score>node2_score:
                        n2Score=node2_score

                single_triple_score=0.6*relaScore+0.2*n1Score+0.2*n2Score
                scoreSum=single_triple_score+single_triple_score

                if scoreSum>domMaxScore:
                    domMaxScore=scoreSum
                    domTitle=each['title']

        #catch the best triple_list
        bestDom=collect.find_one({'title':domTitle})
        bestTriple=bestDom["triples"]

        return bestTriple


test=tripleQuery()

des="我的信用卡被盗刷了一千块"            
print(test.matchBestTriple(des))


                    





