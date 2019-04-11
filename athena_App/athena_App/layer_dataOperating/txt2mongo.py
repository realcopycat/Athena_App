#导入法条法规 刑法

from pymongo import MongoClient as MG
import re

file = open('D:\\Google Download\\#按日期管理的下载\\190404\\法律法规大全\\程序法\\中华人民共和国仲裁法.txt')
line = file.readline()

client=MG()
db=client.spider_data
collect=db.LAW
lawDoc=dict()
lawDoc['name']=line
lawDoc['content']=list()

#re规则
bian=re.compile('第.*编!')
zhang=re.compile('第.*章!')
jie=re.compile('第.*节!')
tiaoT=re.compile('第.*?条!')
tiao=re.compile('第.*?条')
fuze=re.compile('附!则')
#根据法条编制规则控制进程
ctrlcount=0
am_i_in_tiao=0

#写入进程开始
while line:
    print(line)
    pureline = line.replace(u'\u3000', '!')
    if re.findall(fuze, pureline):
        if ctrlcount == 0:
            ctrlcount = 1
            line = file.readline()
            continue
        if ctrlcount == 1:
            if tmp_tiao:
                lawDoc['content'].append(tmp_tiao)
            tmp_tiao = dict()
            break
    if ctrlcount == 1:
        tiaoTest = re.findall(tiaoT, pureline)
        if tiaoTest:
            try:
                if tmp_tiao:
                    lawDoc['content'].append(tmp_tiao)
            except:
                pass
            tiaoTest = re.findall(tiao, pureline)
            tmp_tiao = dict()
            tmp_tiao['lineNo'] = tiaoTest[0]
            tmp_tiao['line'] = pureline.replace('!', '').replace(tiaoTest[0], '')
            line = file.readline()
            continue
        else:
            if (bool((re.search(bian, pureline)))|bool((re.search(zhang, pureline)))|bool((re.search(jie, pureline)))):
                try:
                    if tmp_tiao:
                        lawDoc['content'].append(tmp_tiao)
                        tmp_tiao = dict()
                except:
                    pass
                line = file.readline()
                continue
            else:
                try:
                    if tmp_tiao:
                        tmp_tiao['line'] = tmp_tiao['line'] + pureline.replace('!', '')
                except:
                    pass

    line = file.readline()
    
file.close()
for each in lawDoc['content']:
    print(each)
    print('\n')
print(len(lawDoc['content']))
input()
collect.insert_one(lawDoc)