#model文件管理器

class JOKE():

    model=None

    def load(self):

        #加载gensim
        import gensim

        #加载词向量模型
        model_file = 'C:/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
        self.model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True,limit=5000)
        print('词向量模型已加载')
