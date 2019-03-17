# fact triple rely
#pre-process of the sentence

import os
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller
class LtpParser:
    def __init__(self):

        #initialize every ltp tool
        LTP_DIR = "E:\code_Athena_Support"

        #分词器
        self.segmentor = Segmentor()
        self.segmentor.load(os.path.join(LTP_DIR, "cws.model"))

        #词性标注
        self.postagger = Postagger()
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))

        #依存句法分析
        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))

        #命名实体识别
        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(os.path.join(LTP_DIR, "ner.model"))

        #语义角色标注模块
        self.labeller = SementicRoleLabeller()
        self.labeller.load(os.path.join(LTP_DIR, 'pisrl_win.model'))

    '''语义角色标注'''
    def format_labelrole(self, words, postags):

        #依赖于词性的标注，做依存句法的分析
        #解释：
        #依存句法分析是基于词性标注的。
        arcs = self.parser.parse(words, postags)

        #根据依存句法的分析，标注语义角色
        roles = self.labeller.label(words, postags, arcs)

        #以字典储存，key为编号，value为列表
        #而且是嵌套字典，以arg.name作为key
        #这个字典的含义就是：每个角色的索引是一级key，二级字典以语义角色类型为key
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {arg.name:[arg.name,arg.range.start, arg.range.end] for arg in role.arguments}

        print(roles_dict)
        return roles_dict

    '''句法分析---为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def build_parse_child_dict(self, words, postags, arcs):

        #其数据结构是：
        #这个list底下是一个个字典,每个字典的key是关系名称，每个字典的value是这个关系所对应的词语，这样就得到了父节点们所拥有的关系及有这种关系的孩子
        child_dict_list = []

        #这个list的意义就是展示每个词的依存关系
        format_parse_list = []

        #一级循环：对每个词分析
        for index in range(len(words)):

            #预设孩子字典
            child_dict = dict()

            #二级循环：查每个词的语义角色
            for arc_index in range(len(arcs)):

                #这里无非就是查一下我到底有没有成为谁的爸爸，如果有的话就登记一下
                if arcs[arc_index].head == index+1:   #arcs的索引从1开始
                    if arcs[arc_index].relation in child_dict:
                        child_dict[arcs[arc_index].relation].append(arc_index)
                    else:
                        child_dict[arcs[arc_index].relation] = []
                        child_dict[arcs[arc_index].relation].append(arc_index)
            child_dict_list.append(child_dict)

        rely_id = [arc.head for arc in arcs]  # 提取依存父节点id
        relation = [arc.relation for arc in arcs]  # 提取依存关系
        heads = ['Root' if id == 0 else words[id - 1] for id in rely_id]  # 匹配依存父节点词语
        for i in range(len(words)):
            # ['ATT', '李克强', 0, 'nh', '总理', 1, 'n']
            a = [relation[i], words[i], i, postags[i], heads[i], rely_id[i]-1, postags[rely_id[i]-1]]
            format_parse_list.append(a)

        return child_dict_list, format_parse_list

    '''parser主函数'''
    def parser_main(self, sentence):
        '''显然这是一个类的主函数'''

        words = list(self.segmentor.segment(sentence))
        postags = list(self.postagger.postag(words))
        arcs = self.parser.parse(words, postags)
        child_dict_list, format_parse_list = self.build_parse_child_dict(words, postags, arcs)
        roles_dict = self.format_labelrole(words, postags)
        return words, postags, child_dict_list, roles_dict, format_parse_list

