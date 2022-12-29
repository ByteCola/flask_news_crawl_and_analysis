# -*- coding: UTF-8 -*- 
"""
Created on Sat Jan 20 10:20:33 2022

@author: waiting
"""
import json
import os, re, csv, time, warnings, threading

from pandas import DataFrame
from pymongo import MongoClient
import pandas as pd
import numpy as np
from bson.objectid import ObjectId
import text_analysis.text_processing as tp

import sklearn.exceptions

from text_analysis import counter, modeling, drawing

warnings.filterwarnings("ignore", category=sklearn.exceptions.UndefinedMetricWarning)
warnings.filterwarnings("ignore", category=Warning, module='sklearn')
warnings.filterwarnings("ignore", category=UserWarning, module='gensim')
warnings.filterwarnings("ignore", category=RuntimeWarning, module='gensim')


class TextMining(object):
    '''Text analysis and prediction functions class.

    # Arguments:
        IP: IP address of mongodb database.
        PORT: Port number corresponding to IP.
    '''

    def __init__(self, **kwarg):
        self.IP = kwarg['IP']
        self.PORT = kwarg['PORT']
        self.ConnDB()
        self.tp = tp.TextProcessing(os.getcwd() + '\\' + 'chinese_stop_words.txt', \
                                    os.getcwd() + '\\' + 'athletes_dict.txt')
        if not os.path.exists(os.getcwd() + '\\' + 'athlete_dict_file'):
            os.makedirs(os.getcwd() + '\\' + 'athlete_dict_file')
        self.DictPath = os.getcwd() + '\\' + 'athlete_dict_file'

    def ConnDB(self):
        '''Connect to the mongodb.
        '''
        self._Conn = MongoClient(self.IP, self.PORT)

    def extractJSONData(self, json_array, tag_list):
        '''Extract data from specific json_data.

        # Arguments:
            json_array: json data.
            tag_list: List of tags that need to be extracted.
        '''
        Dict = {}
        for tag in tag_list:
            data = []
            for json in json_array:
                data.append(json[tag])
                Dict.update({tag: np.array(data)})

        dataFrame = pd.DataFrame(Dict, columns=tag_list)
        return dataFrame

    # 从mongodb中取出数据 注意数据包括重复值
    def extractData(self, dbName, colName, tag_list):
        '''Extract data from specific collection of specific database.

        # Arguments:
            dbName: Name of database.
            colName: Name of collection.
            tag_list: List of tags that need to be extracted.
        '''
        db = self._Conn[dbName]
        collection = db.get_collection(colName)
        data = []
        Dict = {}
        for tag in tag_list:
            # exec(tag + " = collection.distinct('" + tag + "')")
            print(tag + " = list(collection.find({},{'" + tag + "':1}))")
            exec(tag + " = list(collection.find({},{'" + tag + "':1}))")
            print(tag + " = [t['" + tag + "'] for t in " + tag + " ]")
            exec(tag + " = [t['" + tag + "'] for t in " + tag + " ]")
            exec("data.append(" + tag + ")")
            exec("Dict.update({'" + tag + "' : np.array(" + tag + ")})")

        data_frame = pd.DataFrame(Dict, columns=tag_list)
        return data_frame

    # 新闻分词 抽取运动员和运动项目
    def extractSportsMetaFromArticle(self, dbName, colName):
        '''Extract the al by each news(articles/documents).

        # Arguments:
            dbName: Name of database.
            colName: Name of collection.
        '''
        db = self._Conn[dbName]
        collection = db.get_collection(colName)
        idLst = self.extractData(dbName, colName, ['_id'])._id
        data = False
        with open(os.getcwd() + '\\' + 'carwler\\athletes.json', 'r', encoding="utf-8") as load_f:
            data = self.extractJSONData(json.load(load_f)['data'], tag_list=['name', 'dis'])
        articles = []
        for _id in idLst:
            title = collection.find_one({'_id': ObjectId(_id)})['title']
            article = collection.find_one({'_id': ObjectId(_id)})['article']
            articles.append(title + ' ' + article)
            # 对每篇文章进行分词并保存
            token, _, _ = self.tp.genDictionary([article], saveDict=False)
            _Article = ' '.join(token[0])
            print(_Article)
            collection.update_one({"_id": ObjectId(_id)}, {"$set": {"words": str(token[0]), "_article": _Article}})

        token, _, _ = self.tp.genDictionary(articles, saveDict=False)
        j = 0
        for tk in token:
            relevantAthletesName = []
            relevantDisciplineCode = []
            for k in range(len(tk)):
                if len(tk[k]) >= 3 and tk[k] in list(data.name):
                    relevantAthletesName.append(tk[k])
                    relevantDisciplineCode.append(list(data[(data.name == tk[k])].dis)[0])
            if len(relevantDisciplineCode) != 0:
                relevantAthletesDuplicateRemoval = list(set(relevantDisciplineCode))
                collection.update_one({"_id": idLst[j]}, {"$set": {"relevant_events": \
                                                                       ' '.join(relevantAthletesDuplicateRemoval),
                                                                   "relevant_athletes_name": \
                                                                       ' '.join(
                                                                           pd.unique(relevantAthletesName).tolist())
                                                                   }})
            j += 1

    # 提取新闻热点并聚合新闻数据
    def polymericSportsArticle(self, dbName, colName):
        '''提取新闻热点并聚合新闻数据.

        # Arguments:
            dbName: Name of database.
            colName: Name of collection.
        '''
        db = self._Conn[dbName]
        collection = db.get_collection(colName)

        df = self.extractData(dbName, colName, ['words', '_article', 'title', 'article', 'address'])
        # 标题去重
        df = df.drop_duplicates(subset=['title'], keep='first')
        word_library_list = counter.get_word_library(df['words'].tolist())
        single_frequency_words_list = counter.get_single_frequency_words(df['words'].tolist())
        max_features = len(word_library_list) - len(single_frequency_words_list) // 2
        matrix = modeling.feature_extraction(df['_article'], vectorizer='TfidfVectorizer',
                                             vec_args={'max_df': 0.95, 'min_df': 1, 'max_features': max_features})
        dbscan = modeling.get_cluster(matrix, cluster='DBSCAN',
                                      cluster_args={'eps': 0.4, 'min_samples': 15, 'metric': 'cosine'})
        labels = modeling.get_labels(dbscan)

        # 构造聚合data_frame
        res_df = DataFrame()
        res_df['words'] = df['words']
        res_df['title'] = df['title']
        res_df['article'] = df['article']
        res_df['label'] = labels
        ranks = modeling.label2rank(labels)
        res_df['rank'] = ranks
        res_df['address'] = df['address']
        # news_pandas.save_news(df, os.path.join(results_path, 'news_label.csv'))
        # 辅助向量
        res_df['matrix'] = matrix.toarray().tolist()
        df_non_outliers = res_df[res_df['label'] != -1].copy()
        if df_non_outliers.shape[0] == 0:
            print('没有聚类出任何热点，请重新设置聚类参数！')
            return
        data_pca_tsne = modeling.feature_reduction(df_non_outliers['matrix'].tolist(),
                                                   pca_n_components=3, tsne_n_components=2)
        df_non_outliers['pca_tsne'] = data_pca_tsne.tolist()
        del df_non_outliers['matrix']
        # news_pandas.save_news(df_non_outliers, os.path.join(results_path, 'news_non_outliers.csv'))

        rank_num = counter.get_num_of_value_no_repeat(df_non_outliers['rank'])
        print('新闻聚合完成，共' + str(rank_num) + '个热点')

        # 将热点信息循环写入到数据库中
        for i in range(rank_num):
            df_rank_i = df_non_outliers[df_non_outliers['rank'] == i + 1]
            # print(df_rank_i)
            row_l = df_rank_i.shape[0]
            #print(row_l)
            for j in range(row_l-1):
                # print("********************************************************")
                # print()
                # print(df_rank_i.iloc[j])
                # print("########################################################")

                data = {
                    'title': df_rank_i.iloc[j]['title'],
                    'article': df_rank_i.iloc[j]['article'],
                    # 'Date':df_rank_i['Date'],
                    'label': int(df_rank_i.iloc[j]['label']),
                    'words': df_rank_i.iloc[j]['words'],
                    'pca_tsne': df_rank_i.iloc[j]['pca_tsne'],
                    'address': df_rank_i.iloc[j]['address'],
                    'rank': int(df_rank_i.iloc[j]['rank'],
                     )
                }

                result_connection = db.get_collection('news_mining')
                result_connection.insert_one(data)
        # 热点词汇打印
        # print("###################热点词汇打印#########################")
        #
        # top_words_list = counter.get_most_common_words(df_rank_i['WordsToken'], top_n=5000, min_frequency=1)
        # top_words = '\n'.join(top_words_list)
        # print(top_words)
        #
        # print("##################热点词汇打印结束#######################")
        #
        # # 热点对应文章话题
        #
        # print("###################热点文章标题打印#########################")
        # all_title = '\n'.join(df_rank_i['title'].tolist())
        # hot_titles = modeling.get_key_sentences(all_title, num=200)
        # print(hot_titles)

        print("###################热点文章标题打印结束#########################")

        rank_num = counter.get_num_of_value_no_repeat(df_non_outliers['rank'])
        value = [df_non_outliers[df_non_outliers['rank'] == i].shape[0] for i in range(1, rank_num + 1)]
        yticks1 = [counter.get_most_common_words(df_non_outliers[df_non_outliers['rank'] == i]['words'],
                                                 top_n=5) for i in range(1, rank_num + 1)]
        # yticks2 = [modeling.get_key_sentences('\n'.join(df_non_outliers[df_non_outliers['rank'] == i]['title_']),
        #                                       num=1) for i in range(1, rank_num + 1)]
        drawing.draw_clustering_analysis_pie(rank_num, value, yticks1)

    # 统计运动员和运动项目的热度 并写入到数据库中
    def statisticsSportsData(self, dbName, colName):
        '''提取新闻热点并聚合新闻数据.

        # Arguments:
            dbName: 新闻数据库.
            colName: 新闻数据集合.
        '''
        db = self._Conn[dbName]
        collection = db.get_collection(colName)

        df = self.extractData(dbName, colName,
                              ['title', 'address', 'date', 'relevant_events', 'relevant_athletes_name'])
        # 标题去重
        df = df.drop_duplicates(subset=['title'], keep='first')

        length = df.shape[0]
        print(length)

        for i in range(length):
            if df.iloc[i]['relevant_events']:
                relevant_events = pd.unique(df.iloc[i]['relevant_events'].split(' '))
                for event in relevant_events:
                    data = {
                        'title': df.iloc[i]['title'],
                        'address': df.iloc[i]['address'],
                        'date': df.iloc[i]['date'],
                        'event': event,
                    }
                    sport_event_statistics_connection = db.get_collection('sport_event_statistics_data')
                    sport_event_statistics_connection.insert_one(data)

            if df.iloc[i]['relevant_athletes_name']:
                relevant_athletes_name = pd.unique(df.iloc[i]['relevant_athletes_name'].split(' '))
                for athlete in relevant_athletes_name:
                    data = {
                        'title': df.iloc[i]['title'],
                        'address': df.iloc[i]['address'],
                        'date': df.iloc[i]['date'],
                        'athlete': athlete,
                    }
                    sport_athlete_statistics_connection = db.get_collection('sport_athlete_statistics_data')
                    sport_athlete_statistics_connection.insert_one(data)

        return

        relevant_events_list = df['relevant_events'].tolist()
        for i, relevant_events in relevant_events_list:
            print(i)
            print(df['title'][i])
            print(df['relevant_events'][i])
            # if relevant_events:
            #     print(pd.unique(relevant_events.split(' ')))
            #
            #     sports_statistics_connection = db.get_collection('sports_statistics_data')
            #
            #     data = {
            #         'title':
            #     }

        # 将热点信息循环写入到数据库中
        # for i in range(rank_num):
        #     df_rank_i = df_non_outliers[df_non_outliers['rank'] == i + 1]
        #     row_l = df_rank_i.shape[1]
        #
        #     for j in range(row_l):
        #         print(df_rank_i.iloc[j]['title'], df_rank_i.iloc[j]['article'])
        #         data = {
        #             'title': df_rank_i.iloc[j]['title'],
        #             'article': df_rank_i.iloc[j]['article'],
        #             # 'Date':df_rank_i['Date'],
        #             'label': int(df_rank_i.iloc[j]['label']),
        #             'words': df_rank_i.iloc[j]['words'],
        #             'pca_tsne': df_rank_i.iloc[j]['pca_tsne'],
        #             'rank': int(df_rank_i.iloc[j]['rank'])
        #         }
        #
        #         result_connection = db.get_collection('news_mining')
        #         result_connection.insert_one(data)
