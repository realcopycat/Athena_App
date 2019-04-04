#本模块为语义相似度计算模块
#参数：两个字符串
#返回：相似度评分

import synonyms as sy

def senCompare(sen1,sen2):
    return sy.compare(sen1,sen2)

