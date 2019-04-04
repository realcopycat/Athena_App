#这是调用es进行搜索的统一接口
#参数：进行描述的字符串,在哪个索引里查找，文档属性是什么,要搜寻的键值,需要的结果数
#返回：原始结果 [hits][hits] 列表形式

from elasticsearch import Elasticsearch as ES

def searchInEs(des,tar_index,tar_docType,keyName,num_res):

    esDriver=ES([{"host":"127.0.0.1","port":9200}])

    #构造请求结构
    query_body={
        "query":{
            "match":{
                keyName:des
                }
            }
        }

    #在es中搜索
    result=esDriver.search(index=tar_index,doc_type=tar_docType,body=query_body,size=num_res)

    return result["hits"]["hits"]


####################################################################
#返回结果形式概览：
#来自kibana

'''
"hits" : {
    "total" : 9250,
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : ".kibana_1",
        "_type" : "doc",
        "_id" : "space:default",
        "_score" : 1.0,
        "_source" : {
          "space" : {
            "name" : "Default",
            "description" : "This is your default space!",
            "color" : "#00bfb3",
            "_reserved" : true
          },
          "type" : "space",
          "updated_at" : "2019-03-10T02:30:53.517Z"
        }
      },
      {
        "_index" : ".kibana_1",
        "_type" : "doc",
        "_id" : "config:6.6.1",
        "_score" : 1.0,
        "_source" : {
          "config" : {
            "buildNum" : 19513
          },
          "type" : "config",
          "updated_at" : "2019-03-10T02:30:58.459Z"
        }
      },
      {
        "_index" : ".kibana_1",
        "_type" : "doc",
        "_id" : "telemetry:telemetry",
        "_score" : 1.0,
        "_source" : {
          "telemetry" : {
            "enabled" : false
          },
          "type" : "telemetry",
          "updated_at" : "2019-03-10T02:31:34.078Z"
        }
      },
      {
        "_index" : ".kibana_1",
        "_type" : "doc",
        "_id" : "apm-telemetry:apm-telemetry",
        "_score" : 1.0,
        "_source" : {
          "apm-telemetry" : {
            "has_any_services" : false,
            "services_per_agent" : { }
          },
          "type" : "apm-telemetry",
          "updated_at" : "2019-03-10T04:41:24.389Z"
        }
      },
      {
        "_index" : "qa_data",
        "_type" : "qa",
        "_id" : "WTHyZWkB4294B6XHLx8b",
        "_score" : 1.0,
        "_source" : {
          "question" : "电信诈骗作文题目",
          "answer" : "随着现代科技的发展，我们的生活有了极大的改善，但这也促使了许多人利用高科技诈骗钱财，破坏人们的财产利益。现在的骗子无处不在，甚至就在你身边，可要多加小心你的口袋哦！  当今最为广泛的诈骗方法无非就是冒充“朋友”向你发QQ信息、打电话、发短信，“我遇难了！”拜托你马上“救急”汇款。看在朋友的份上，你汇了款后才得知你的“朋友”已经逃之夭夭。最后，遇难反成自己！  最令人哭笑不得的就是冒充公安机关逮捕你这个所谓的“犯罪嫌疑人”，说你绑架，贩毒等罪案，再通过打电话和发信息的方式，步步引诱，甚至绑票赎金，将银行账号的钱转走。“公安机关”反成“嫌疑犯”！真是让人哭笑不得，无语伦次！  “你中大奖啦！”这是最为普遍的诈骗方式，骗子往往冒充“我是歌手”“中国好声音”等知名节目，传来佳音，你中大奖，只要交一点“保险费”，“税金”就可以领取大奖，机会不容错过，再不来就没有啦！你付费以后，“大奖”消失的无影无踪。看来，这就是贪小便宜的“大奖”吧！  令人最不可思议的还是“欠费”，电话欠费是一件很平常的事情，但却还是有许多诈骗发生：我是中国电信的工作人员，您的电话、电视、宽带账户欠费了，请缴纳“滞纳金”！没想到“滞纳金”最后进了骗子的腰包。  “天上掉钱啦！”你在街头发现一大笔钱，跑去捡起。谁知，骗子在假钱上下药，趁你昏迷之时，取走所有的贵重物品，当你起来以后，发现财物被骗子一扫而空，后悔莫及啊！你见过天上掉钱吗？做事还是谨慎为好！  你发现了吗？网上购物往往要比市场价低得多，许多人为贪小便宜，谋利益，在网上汇款，数月后毫无音讯，“你上当了！”看来，不要总是想着会有好事发生哦，即使市场价贵点，但质量和品质还是有所保障的，可要当心啦！  骗子无处不在，利用数不胜数的手段处处诈骗，千方百计，步步引诱，你时刻小心着吗？防止诈骗，保护自己的财产利益，是一件很重要的事哟！只要我们处理得当，就一定不会上那些可恶诈骗团的“鱼钩”了。  小心“防”诈骗，安全“0”距离，只要我们谨慎行事，捂紧口袋，正确判断，就能远离诈骗，远离骗子！防止诈骗，从我做起，欧耶！"
        }
      },
'''