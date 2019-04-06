# ES数据说明

- 有关问答库 
    -  __index_ : "qa_data"
    - _doc_type_ : "qa"
    - _properties_ :
        - "question"
        - "answer"

- 有关百科知识库 
 

    - __index_ : "baike_data_abstract"
    - _doc_type_ : "knowledge"
    - _properties_:
        -  "title"
        -  "abstract"
        

- 有关案例库  
    - __index_ : "case_data"
    - _doc_type_ : "case"
    - _properties_ : 
        - "title"
        - "plainText" 

- 有关新闻案例库
    - __index_ : "news_case"
    - _doc_type_ : "case"
    - _properties_ :
        - "title"
        - "plaintext"
        - "city"
        - "region"  
        - "province"
        - "age"
        - "gender"
        - "job"
        - "month"
        - "duration"
        - "amount"
        - "method"
        - "type"

- 法条库
    - __index_ : "Law_data"
    - _doc_type_ : "line"
    - _properties_ :
        - "LawTitle"
        - "lineNo"
        - "line"