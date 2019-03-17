#search the most suitable case for user

from athena_App.openlaw.fact_triple_1 import *
from pymongo import MongoClient as MC
import synonyms

class tripleQuery():
    '''做三元组查询的类'''

    def __init__():
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
        for each in data:
            triple_list=each["triples"]

            for eachTriple in triple_list:




