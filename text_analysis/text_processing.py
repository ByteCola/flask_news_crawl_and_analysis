# -*- coding: UTF-8 -*- 
"""
Created on Fri Feb 23 12:37:46 2022

@author: waiting
"""
from collections import defaultdict

import numpy as np

import jieba, os
from gensim import corpora, similarities, models, matutils, utils


class TextProcessing(object):
    '''Text pre-processing functions class.

    # Arguments
        chnSTWPath: chinese stop words txt file path.
        finance_dict: latest financial related words txt file path.
    '''

    def __init__(self, chnSTWPath, finance_dict):
        self.chnSTWPath = chnSTWPath
        self.finance_dict = finance_dict

    def renewFinanceDict(self, new_Word_list):
        '''Add latest necessary financial words into financial dictionary
            for improving tokenization effect.

        # Arguments:
            new_Word_list: New financial words list, eg: ["区块链"，"离岸金融"].
        '''
        with open(self.finance_dict, 'a', encoding='utf-8') as file:
            for word in new_Word_list:
                file.write(word + '\n')

    def getchnSTW(self):
        '''Load the stop words txt file.
        '''
        stopwords = [line.strip() for line in open(self.chnSTWPath, 'r').readlines()]
        return stopwords

    def jieba_tokenize(self, documents):
        '''Cut the documents into a sequence of independent words.

        # Arguments:
            documents: List of news(articles).
        '''
        chnSTW = self.getchnSTW()
        corpora_documents = []
        jieba.load_userdict(self.finance_dict)
        for item_text in documents:
            outstr = []
            sentence_seged = list(jieba.cut(item_text))
            for word in sentence_seged:
                if word not in chnSTW and word != '\t' \
                        and word != ' ':
                    outstr.append(word)
            corpora_documents.append(outstr)
        return corpora_documents

    def RemoveWordAppearOnce(self, corpora_documents):
        '''Remove the words that appear once among all the tokenized news(articles).

        # Arguments:
             corpora_documents: List of tokenized news(articles).
        '''
        frequency = defaultdict(int)
        for text in corpora_documents:
            for token in text:
                frequency[token] += 1
        corpora_documents = [[token for token in text if frequency[token] > 1] for text in corpora_documents]
        return corpora_documents

    def genDictionary(self, documents, **kwarg):
        '''Generate dictionary and bow-vector of all tokenzied news(articles).

        # Arguments:
            documents: List of news(articles).
            saveDict: Save dictionary or not(bool type).
            saveBowvec: Save bow-vector or not(bool type).
            returnValue: Return value or not(bool type).
        '''
        self._raw_documents = documents
        token = self.jieba_tokenize(documents)  # jieba tokenize
        # corpora_documents = self.RemoveWordAppearOnce(token)  # remove thw words appearing once in the dictionary
        self._dictionary = corpora.Dictionary(token)  # generate dictionary using tokenized documents  
        if kwarg['saveDict']:
            self._dictionary.save(kwarg['saveDictPath'])  # store the dictionary, for future reference
        self._BowVecOfEachDoc = [self._dictionary.doc2bow(text) for text in
                                 token]  # convert tokenized documents to vectors
        # if kwarg['saveBowvec']:
        #     corpora.MmCorpus.serialize(kwarg['saveBowvecPath'], self._BowVecOfEachDoc)  # store to disk, for later use
        # if kwarg['returnValue']:
        #     return token, self._dictionary, self._BowVecOfEachDoc
        return token, self._dictionary, self._BowVecOfEachDoc

    def CallTransformationModel(self, Dict, Bowvec, **kwarg):
        '''Invoke specific transformation models of Gensim module.

        # Arguments:
            Dict: Dictionary made by all tokenized news(articles/documents).
            Bowvec: Bow-vector created by all tokenized news(articles/documents).
            modelType: Transformation model type, including 'lsi', 'lda' and 'None', 'None' means TF-IDF mmodel.
            tfDim: The number of topics that will be extracted from each news(articles/documents). 
            renewModel: Re-train the transformation models or not(bool type).
            modelPath: The path of saving trained transformation models.
        '''
        if kwarg['renewModel']:
            tfidf = models.TfidfModel(Bowvec)  # initialize tfidf model
            tfidfVec = tfidf[Bowvec]  # use the model to transform whole corpus
            tfidf.save(kwarg['modelPath'] + "tfidf_model.tfidf")
            if kwarg['modelType'] == 'lsi':
                model = models.LsiModel(tfidfVec, id2word=Dict,
                                        num_topics=kwarg['tfDim'])  # initialize an LSI transformation
                modelVec = model[tfidfVec]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
                model.save(kwarg['modelPath'])  # same for tfidf, lda, ...
            elif kwarg['modelType'] == 'lda':
                model = models.LdaModel(tfidfVec, id2word=Dict, num_topics=kwarg['tfDim'])
                modelVec = model[tfidfVec]  # 每个文本对应的LDA向量，稀疏的，元素值是隶属与对应序数类的权重
                model.save(kwarg['modelPath'])  # same for tfidf, lda, ...
            elif kwarg['modelType'] == 'None':
                model = tfidf
                modelVec = tfidfVec
        else:
            if not os.path.exists(kwarg['modelPath'] + "tfidf_model.tfidf"):
                tfidf = models.TfidfModel(Bowvec)  # initialize tfidf model
                tfidfVec = tfidf[Bowvec]  #
                tfidf.save(kwarg['modelPath'] + "tfidf_model.tfidf")
            else:
                tfidf = models.TfidfModel.load(kwarg['modelPath'] + "tfidf_model.tfidf")
                tfidfVec = tfidf[Bowvec]  # use the model to transform whole corpus
            if kwarg['modelType'] == 'lsi':
                if not os.path.exists(kwarg['modelPath'] + "lsi_model.lsi"):
                    tfidf = models.TfidfModel.load(kwarg['modelPath'] + "tfidf_model.tfidf")
                    tfidfVec = tfidf[Bowvec]  # use the model to transform whole corpus
                    model = models.LsiModel(tfidfVec, id2word=Dict,
                                            num_topics=kwarg['tfDim'])  # initialize an LSI transformation
                    modelVec = model[
                        tfidfVec]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
                    model.save(kwarg['modelPath'] + "lsi_model.lsi")  # same for tfidf, lda, ...
                else:
                    model = models.LsiModel.load(kwarg['modelPath'] + "lsi_model.lsi")
                    modelVec = model[tfidfVec]
            elif kwarg['modelType'] == 'lda':
                if not os.path.exists(kwarg['modelPath'] + "lda_model.lda"):
                    tfidf = models.TfidfModel.load(kwarg['modelPath'] + "tfidf_model.tfidf")
                    tfidfVec = tfidf[Bowvec]  # use the model to transform whole corpus
                    model = models.LdaModel(tfidfVec, id2word=Dict, num_topics=kwarg['tfDim'])
                    modelVec = model[tfidfVec]  # 每个文本对应的LDA向量，稀疏的，元素值是隶属与对应序数类的权重
                    model.save(kwarg['modelPath'] + "lda_model.lda")  # same for tfidf, lda, ...
                else:
                    model = models.LdaModel.load(kwarg['modelPath'] + "lda_model.lda")
                    modelVec = model[tfidfVec]
            elif kwarg['modelType'] == 'None':
                model = tfidf
                modelVec = tfidfVec
        return tfidfVec, modelVec

    def CalSim(self, test_document, Type, best_num):
        '''Calculate similarities between test document wth all news(articles/documents).

        # Arguments:
            test_document: List of raw documents.
            Type: Models of calculating similarities.
            best_num: refer to 'num_best' parameter in Gensim module.
        '''
        if Type == 'Similarity-tfidf-index':
            tfidf = models.TfidfModel(self._BowVecOfEachDoc)
            tfidfVec = tfidf[self._BowVecOfEachDoc]
            self._num_features = len(self._dictionary.token2id.keys())
            self._similarity = similarities.Similarity(Type, tfidfVec, \
                                                       num_features=self._num_features, num_best=best_num)
            test_cut_raw = list(jieba.cut(test_document))
            test_BowVecOfEachDoc = self._dictionary.doc2bow(test_cut_raw)
            self._test_BowVecOfEachDoc = tfidf[test_BowVecOfEachDoc]
        elif Type == 'Similarity-LSI-index':
            lsi_model = models.LsiModel(self._BowVecOfEachDoc)
            corpus_lsi = lsi_model[self._BowVecOfEachDoc]
            self._num_features = len(self._dictionary.token2id.keys())
            self._similarity = similarities.Similarity(Type, corpus_lsi, \
                                                       num_features=self._num_features, num_best=best_num)
            test_cut_raw = list(jieba.cut(test_document))
            test_BowVecOfEachDoc = self._dictionary.doc2bow(test_cut_raw)
            self._test_BowVecOfEachDoc = lsi_model[test_BowVecOfEachDoc]
        self.Print_CalSim()
        IdLst = []
        SimRltLst = []
        SimTxLst = []
        for Id, Sim in self._similarity[self._test_BowVecOfEachDoc]:
            IdLst.append(Id)
            SimRltLst.append(Sim)
            SimTxLst.append(self._raw_documents[Id])
        return IdLst, SimTxLst, SimRltLst

    def PrintWorfCloud(self, documents, backgroundImgPath, fontPath):
        '''Print out the word cloud of all news(articles/documents).

        # Arguments:
            documents: Overall raw documents.
            backgroundImgPath: Background image path.
            fontPath: The path of windows fonts that used to create the word-cloud.
        '''
        from scipy.misc import imread
        import matplotlib.pyplot as plt
        from wordcloud import WordCloud
        corpora_documents = self.jieba_tokenize(documents)  # 分词
        for k in range(len(corpora_documents)):
            corpora_documents[k] = ' '.join(corpora_documents[k])
        corpora_documents = ' '.join(corpora_documents)
        color_mask = imread(backgroundImgPath)  # "C:\\Users\\lenovo\\Desktop\\Text_Mining\\3.jpg"
        cloud = WordCloud(font_path=fontPath, mask=color_mask, background_color='white', \
                          max_words=2000, max_font_size=40)  # "C:\\Windows\\Fonts\\simhei.ttf"
        word_cloud = cloud.generate(corpora_documents)
        plt.imshow(word_cloud, interpolation='bilinear')
        plt.axis("off")


if __name__ == '__main__':
    tp = TextProcessing(os.getcwd() + '\\' + 'Chinese_Stop_Words.txt', \
                        os.getcwd() + '\\' + 'finance_dict.txt')
    doc = ['苏翊鸣在社交媒体上表示，自己不训练的时候曾到海南冲浪。苏翊鸣的社交媒体上也有在海南乘风破浪的画面。他在视频中介绍，单板滑雪最早是由冲浪演变而来，两个运动非常相似。 \
    \
虽然，谷爱凌从事的是自由式滑雪项目，但性格活泼且勇于尝试各种挑战的她对到海南冲浪充满好奇。“我听说那里很暖和，还能冲浪。” \
    \
得知这一消息后，国家体育总局水上运动管理中心和国家冲浪队邀请二人到国家冲浪训练基地——海南万宁日月湾进行冲浪体验和训练，并提供全面的保障。邀请函这样表述：“热切地欢迎你们能来日月湾感受冲浪运动的乐趣和魅力，并和国家冲浪队的运动员进行交流学习和互动。” \
    \
相信对于喜欢极限运动的二人来说，冲浪应该不在话下，期待冰雪“双子星”的表现。 \
    \
单板滑雪最早兴起于20世纪60年代的美国，其产生与滑板和冲浪运动有关。一位叫波普的滑雪爱好者仿照海上冲浪板为自己的孩子制作了一块滑雪板，取名“斯纳菲尔”，意即雪上冲浪。后来，这种滑雪板开始批量生产，然而在10年的时间里，这种滑雪板一直被作为儿童和少年雪上的玩具销售。 \
 \
            对单板滑雪运动发展和项目形成具有决定意义的是高山滑雪和自由式滑雪以及陆地滑板爱好者的加入。他们将高山滑雪、自由式滑雪和陆地滑板中的一些技术、技巧和运动形式引进到单板滑雪中来，如高山滑雪的回转、自由式滑雪的雪上技巧和空中技巧以及陆地滑板的“U”形池技巧等，从而使单板滑雪逐渐形成了一个独立的竞技项目。1980年，在美国滑雪联盟的组织下，制定了第一个单板滑雪竞赛规则，并于1983年在美国举行了首届国际单板滑雪赛。随着1990年国际滑板滑雪联合会的正式成立，从事单板滑雪运动的人数逐渐增加，在一定程度上促进了单板滑雪运动的发展。 \
 \
           国家冲浪队表示，对于苏翊鸣成为一名卓越的冲浪高手，并参加奥运会冲浪比赛充满期待。值得一提的是，去年的东京奥运会上，冲浪已经成为正式比赛项目，期待2024年的巴黎奥运会上，能再次看见苏翊鸣的精彩表现。']
    DictPath = os.getcwd() + '\\' + 'athletes_dict_file'
    athletesName = '苏翊鸣'
    print(DictPath)
    print(DictPath + '\\' + athletesName + '\\' + athletesName + '_dict.dict')
    print(DictPath + '\\' + athletesName + '\\' + athletesName + '_bowvec.mm')
    if not os.path.exists(DictPath + '\\' + athletesName):
        os.makedirs(DictPath + '\\' + athletesName)
    # tp.genDictionary(doc, saveDict=True, saveDictPath=DictPath + '\\' + athletesName + '\\' + athletesName + '_dict.dict', \
    #                  saveBowvec=True, saveBowvecPath=DictPath + '\\' + athletesName + '\\' + athletesName + '_bowvec.mm',
    #                  returnValue=False)

    doc = ["新中国今天成立了"]
    token, _, _ = tp.genDictionary(doc, saveDict=False)
    print(token)
