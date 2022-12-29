# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present localhost
"""
import json
import os

from home import blueprint
from flask import render_template, request, redirect, url_for
from jinja2 import TemplateNotFound
import pandas as pd

from utils.database import Database


@blueprint.route('/')
def route_default():
    """
    网站访问默认跳转至index首页
    :return:
    """
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# 新闻聚类
@blueprint.route('/subjects')
def subjects():
    db = Database()
    data = db.get_data('olympics_news_mining_db', 'news_mining')

    df = pd.DataFrame(data)
    print(list(df.loc[(df["rank"] == 1), :].title)[0])
    # top_subjects = df.drop_duplicates(subset=['rank'], keep='first')
    # print(top_subjects)

    series = df.groupby(by=['rank'], as_index=False).size()
    series = series.sort_values('size', ascending=True)
    # series['rank'] = series['size'].rank(method='first', ascending=False)
    data = []
    for i in range(series.shape[0]):
        # print(series['athlete'][i]+'-----'+str(series['size'][i]))
        r_articles = df.loc[(df["rank"] == series['rank'][i]), :]
        data.append({
            "rank": int(series['rank'][i]),
            "title": list(df.loc[(df["rank"] == series['rank'][i]), :].title)[0],
            "index_value": r_articles.shape[0]
        })
    print(data.sort(key=lambda x: x["rank"]))

    print(list(df['pca_tsne']))

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

    # data = [
    #     {
    #         "rank": 1,
    #         "title": "中国短道速滑获得铜牌",
    #         "top_words": "短道速滑、铜牌、中国队",
    #         "index_value": 3040,
    #         "titles": [
    #             "先后搜到了哦哦是", "东阿科任老师地方", "噢诶让老伯恩利搜"
    #         ]
    #     },
    #     {
    #         "rank": 2,
    #         "title": "中国短道速滑获得铜牌",
    #         "top_words": "短道速滑、铜牌、中国队",
    #         "index_value": 3040,
    #         "titles": [
    #             "先后搜到了哦哦是", "东阿科任老师地方", "噢诶让老伯恩利搜"
    #         ]
    #     },
    #     {
    #         "rank": 3,
    #         "title": "中国短道速滑获得铜牌",
    #         "top_words": "短道速滑、铜牌、中国队",
    #         "index_value": 3040,
    #         "titles": [
    #             "先后搜到了哦哦是", "东阿科任老师地方", "噢诶让老伯恩利搜"
    #         ]
    #     },
    #     {
    #         "rank": 4,
    #         "title": "中国短道速滑获得铜牌",
    #         "top_words": "短道速滑、铜牌、中国队",
    #         "index_value": 3040,
    #         "titles": [
    #             "先后搜到了哦哦是", "东阿科任老师地方", "噢诶让老伯恩利搜"
    #         ]
    #     },
    #     {
    #         "rank": 5,
    #         "title": "中国短道速滑获得铜牌",
    #         "top_words": "短道速滑、铜牌、中国队",
    #         "index_value": 3040,
    #         "titles": [
    #             "先后搜到了哦哦是", "东阿科任老师地方", "噢诶让老伯恩利搜"
    #         ]
    #     },
    #     {
    #         "rank": 6,
    #         "title": "中国短道速滑获得铜牌",
    #         "top_words": "短道速滑、铜牌、中国队",
    #         "index_value": 3040,
    #         "titles": [
    #             "先后搜到了哦哦是", "东阿科任老师地方", "噢诶让老伯恩利搜"
    #         ]
    #     }
    # ]
    # print(data)
    return render_template('home/subjects.html', subjects=data, subjects_len=len(data), pca_tsne=list(df['pca_tsne']),
                           segment='subjects')


# 新闻聚类详情
# 新闻聚类
@blueprint.route('/subject/<rank>')
def subject_detail(rank):
    db = Database()
    data = db.get_data('olympics_news_mining_db', 'news_mining', query={"rank": int(rank)})
    list = data.values.tolist()
    # print(list)
    # 词云
    temp_words = {}
    words_list = []

    for d in list:
        a = d[4]
        a = a[a.index('[') + 1:len(a) - 1]
        a = a.split(',')
        for w in a:
            if w in temp_words:
                temp_words[w] += 1
            else:
                temp_words[w] = 0

    for key in temp_words:
        print(key, ":", temp_words[key])
        if temp_words[key] > 10:
            words_list.append({
                'name': key.replace("'",""),
                'value': temp_words[key]
            })

    print(temp_words)
    print(words_list)

    return render_template('home/subjects_detail.html', subjects=list, words_list=words_list,temp_words=temp_words,
                           segment='subjects')


# 运动员热门榜单
@blueprint.route('/athletes')
def athletes():
    db = Database()

    data = db.get_data('olympics_news_mining_db', 'sport_athlete_statistics_data')
    df = pd.DataFrame(data)

    series = df.groupby(by=['athlete'], as_index=False).size()
    series = series.sort_values('size', ascending=True)
    series['rank'] = series['size'].rank(method='first', ascending=False)
    data = []
    for i in range(series.shape[0]):
        # print(series['athlete'][i]+'-----'+str(series['size'][i]))
        r_articles = df.loc[(df["athlete"] == series['athlete'][i]), :]
        data.append({
            "rank": int(series['rank'][i]),
            "name": series['athlete'][i],
            "index_value": r_articles.shape[0]
        })
    print(data.sort(key=lambda x: x["rank"]))
    # data = [
    #     {
    #         "rank": 1,
    #         "name": "谷爱凌",
    #         "index_value": 3040,
    #         "articles": [
    #             {
    #                 'title': '谷爱凌今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             },
    #             {
    #                 'title': '谷爱凌今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             }
    #         ]
    #     },
    #     {
    #         "rank": 2,
    #         "name": "武大靖",
    #         "index_value": 1930,
    #         "articles": [
    #             {
    #                 'title': '武大靖今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             },
    #             {
    #                 'title': '武大靖今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             }
    #         ]
    #     },
    #     {
    #         "rank": 3,
    #         "name": "朱易",
    #         "index_value": 930,
    #         "articles": [
    #             {
    #                 'title': '朱易今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             },
    #             {
    #                 'title': '朱易今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             }
    #         ]
    #     },
    # ]
    # print(data)
    return render_template('home/athletes.html', athletes=data, segment='athletes')


# 运动项目数据挖掘
@blueprint.route('/events')
def events():
    db = Database()

    data = db.get_data('olympics_news_mining_db', 'sport_event_statistics_data')
    df = pd.DataFrame(data)

    series = df.groupby(by=['event'], as_index=False).size()
    series = series.sort_values('size', ascending=True)
    series['rank'] = series['size'].rank(method='first', ascending=False)

    events_df = pd.DataFrame()
    with open(os.getcwd() + '\\' + 'carwler\\events.json', 'r', encoding="utf-8") as load_f:
        events_df = pd.DataFrame(json.load(load_f))

    # print(events_df)
    print(events_df.iloc[0].label)
    print(list(events_df.loc[events_df['code'] == 'ALP'].label)[0])

    data = []
    for i in range(series.shape[0]):
        # print(series['athlete'][i]+'-----'+str(series['size'][i]))
        r_articles = df.loc[(df["event"] == series['event'][i]), :]

        # print(events_df.loc[events_df['code'] == str(series['event'][i])]['label'])
        data.append({
            "rank": int(series['rank'][i]),
            "name": list(events_df.loc[events_df['code'] == str(series['event'][i])]['label'])[0],
            "index_value": r_articles.shape[0]
        })
    print(data.sort(key=lambda x: x["rank"]))

    # data = [
    #     {
    #         "rank": 1,
    #         "name": "谷爱凌",
    #         "index_value": 3040,
    #         "articles": [
    #             {
    #                 'title': '谷爱凌今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             },
    #             {
    #                 'title': '谷爱凌今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             }
    #         ]
    #     },
    #     {
    #         "rank": 2,
    #         "name": "武大靖",
    #         "index_value": 1930,
    #         "articles": [
    #             {
    #                 'title': '武大靖今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             },
    #             {
    #                 'title': '武大靖今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             }
    #         ]
    #     },
    #     {
    #         "rank": 3,
    #         "name": "朱易",
    #         "index_value": 930,
    #         "articles": [
    #             {
    #                 'title': '朱易今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             },
    #             {
    #                 'title': '朱易今日斩获首金',
    #                 'url': 'https://www.beijing2022.cn'
    #             }
    #         ]
    #     },
    # ]
    return render_template('home/events.html', events=data, segment='events')


# 冰墩墩
@blueprint.route('/bingdundun')
def bingdundun():
    db = Database()
    # data = list(db.get_data('olympics_news_mining_db', 'news_data'))

    return render_template('home/bingdundun.html', bingdundun=[], segment='bingdundun')


# 爬虫统计
@blueprint.route('/crawler')
def crawler():
    db = Database()
    data = db.get_data('olympics_news_mining_db', 'news_data')
    df = pd.DataFrame(data)

    # series = df.groupby(by=['site'], as_index=False).size()
    # series = series.sort_values('size', ascending=True)

    # print(series)

    news_count = db.get_data('olympics_news_mining_db', 'news_data', query={"site": {"$eq": "beijing2022cn"}}).count()

    print(news_count[0])

    site_dicts = {
        'beijing2022cn': '北京冬奥官网',
        '163com': '网易新闻',
        'sohu': '搜狐新闻',
        'qq': '腾讯新闻',
        'peoplecomcn': '人民网',
        'newscn': '新华网',
        'china': '中国网'

    }

    sites_df = pd.DataFrame()
    with open(os.getcwd() + '\\' + 'carwler\\sites.json', 'r', encoding="utf-8") as load_f:
        sites_df = pd.DataFrame(json.load(load_f))

    data = []
    for i in range(sites_df.shape[0]):
        code = sites_df.iloc[i]['code']
        print(code)

        news_count = [0]
        try:
            news_count = db.get_data('olympics_news_mining_db', 'news_data',
                                     query={"site": {"$eq": code}}).count()
        except Exception:
            print(0)

        data.append(
            {
                "site_name": sites_df.iloc[i]['label'],
                "site_url": sites_df.iloc[i]['url'],
                "news_num": news_count[0]
            }
        )

    # print(events_df)
    # print(list(sites_df.loc[sites_df['code'] == 'beijing2022cn'].label)[0])

    # data = [
    #     {
    #         "site_name": '北京奥运官网',
    #         "site_url": "https://www.bj2022.com",
    #         "news_num": 0
    #     },
    #     {
    #         "site_name": '网易新闻',
    #         "site_url": "https://www.163.com",
    #         "news_num": 0
    #     },
    #     {
    #         "site_name": '搜狐新闻',
    #         "site_url": "https://www.sohu.com",
    #         "news_num": 0
    #     },
    #     {
    #         "site_name": '人民网',
    #         "site_url": "https://www.people.com.cn",
    #         "news_num": 0
    #     },
    #     {
    #         "site_name": '新华网',
    #         "site_url": "https://www.xinhua.net",
    #         "news_num": 0
    #     },
    # ]
    return render_template('home/crawler.html', crawlers=data, segment='crawler')


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
