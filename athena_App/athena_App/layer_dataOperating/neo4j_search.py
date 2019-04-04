# 此函数为在图数据库中搜索的函数，由于各个模块需求各异，这个模块设计为 类 的形式

from neo4j import GraphDatabase as GD

class neo4jQuery():
    #query in case graph

    def __init__(self):

        #initialize the database
        self.driver=GD.driver("bolt://localhost:7687",auth=("neo4j","123"))

        #start query session
        self.session=self.driver.session()

    def entityQuery(self,node1):
        '''
        实体查询
        !! Parameter:

        'gr' --is a session object

        'node1' --is a str which represent the entity we need to learn
        '''

        #construct the query script
        result=self.session.run("MATCH (a:Node {name:'"+node1+"'})-[b]->(n)"
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

            link_item["label"]={}
            link_item["label"]["normal"]={}
            link_item["label"]["normal"]["show"]=True
            link_item["label"]["normal"]["formatter"]=record["b"].type

            link_list.append(link_item)

        return node_list,link_list

    def attrQuery(self,attr_name,attr_value):
        '''
        neo4j数据库 属性查询模块
        参数1：属性的名称
        参数2：属性的值
        返回：原始答案
        DESIGN FOR case search
        '''

        result=self.session.run("MATCH (a:Des {"+attr_name+": '"+attr_value+"'})-[b]->(c)"
                                "RETURN a,b,c")
                                
        return result
        

    def jsonPackForEchart(self,node_list,link_list):
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

    