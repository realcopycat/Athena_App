#search in the neo4j database

from neo4j import GraphDatabase as GD
#import synonyms as sy

class answerGraph():
    #designed to search in neo4j database and return a json file which contain answer

    def __init__(self):

        #initialize the database
        self.driver=GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

        self.session=self.driver.session()

    def entityQuery(self,node1,gr):
        '''
        !! Parameter:

        'gr' --is a session object

        'node1' --is a str which represent the entity we need to learn
        '''

        #construct the query script
        result=gr.run("MATCH (a:Node {name:'"+node1+"'})-[b]->(n)"
              "RETURN a,b,n")

        node_list=[{'name':node1,'category':'center'}]
        link_list=[]

        for record in result:

            #add end node
            end_node=record["n"]._properties
            end_node["category"]='end'
            node_list.append(end_node)

            #add link
            link_item={}
            link_item['source']=record["a"]._properties["name"]
            link_item['target']=record["n"]._properties["name"]
            link_item['value']=record["b"].type
            link_list.append(link_item)

        return self.jsonPack(node_list,link_list)

    def jsonPack(self,node_list,link_list):
        '''
        parameter instruction:

        node_list is a list ,in which is a number of dict which contians
        node's name and node's category

        link_list is a list ,in which is a number of dict which contains
        link's source,target and attribute of relation
        '''
        json_data={}

        json_data["data"]=node_list
        json_data["links"]=link_list

        #print(json_data)

        return json_data
