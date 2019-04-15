# “过程库”建设概要

- 节点类型规定
  - Object ：对象 （举例：基层法院、刑事案件）
  - Function ：方法（举例：审理、判断是否为普通刑事案件）
- 关系类型规定
  - ToFunction ：对“指向物”执行“被指向方法”
  - ToObject ：从Function指向一个Object，表示返回的对象
- 关于人的特殊规定
  - 我们定义一个name：USER的Object，相当于使用的用户。所拥有的都是“判断”性的“Function”
  - 判断性的Function举例（总之就是IF-ELIF-ELSE）
    - 是否为普通刑事案件
    - 是否有加重情节     
- 人工三元组举例
  - （刑事案件，ToFunction{}，是否为普通刑事案件）
  - （是否为普通刑事案件，ToFunction）  
