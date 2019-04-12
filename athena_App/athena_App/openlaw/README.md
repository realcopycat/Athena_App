﻿# 相关知识解释

- 依存句法分析

其分析是基于词性标注的结果。    

返回的结果可以这样理解：有多少个词就会有多少个结果组，每个结果组对应一个词；结果组的顺序就是传入的每个词；结果组的第一个参数是：句中另一个词的索引；结果组的第二个参数是：与另一个词的关系

- 语义角色标注  

语义角色标注则是基于依存句法和词性标注的综合结果。  

其返回的结果可以这样理解：一个句子里可以有多个语义角色。  

>返回结果 roles 是关于多个谓词的语义角色分析的结果。由于一句话中可能不含有语义角色，所以结果可能为空。

>role.index 代表谓词的索引， role.arguments 代表关于该谓词的若干语义角色。

>arg.name 表示语义角色类型，arg.range.start 表示该语义角色起始词位置的索引，arg.range.end 表示该语义角色结束词位置的索引。

- 命名实体识别  

命名实体识别同样需要基于词性标注的结果

其返回结果见官方解释：

>LTP 采用 BIESO 标注体系。B 表示实体开始词，I表示实体中间词，E表示实体结束词，S表示单独成实体，O表示不构成命名实体。

>LTP 提供的命名实体类型为:人名（Nh）、地名（Ns）、机构名（Ni）。

>B、I、E、S位置标签和实体类型标签之间用一个横线 - 相连；O标签后没有类型标签。  
>更多解释见：  
>
>  
>O	  这个词不是NE    
S	  这个词单独构成一个NE  
B	  这个词为一个NE的开始  
I	  这个词为一个NE的中间  
E	  这个词位一个NE的结尾  