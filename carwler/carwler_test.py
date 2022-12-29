# coding=utf8
import datetime
import json
import os
import re
import time

import pandas as pd
from bs4 import BeautifulSoup

from pymongo import MongoClient
import numpy as np

import requests


a = "['马宝军', '王璐', '统筹', '杜', '屹然', '策划', '李琳', '陈睿', '戴', '天放', '新', '媒体', '陈睿', '别培辉', '中国', '新华', '电视网', 'CNC', '出品']"

a = a[a.index('[')+1:len(a)-1]
print(a)

a = a.split(',')

for i in a:
    print(i)

#print(a.split(","))

# for i in a:
#     print(i)

##### python json数据操作
#
# j = {}
#
#
#
# if 'test' in j:
#     j['test'] += 1
# else:
#     j['test'] = 0
#
# print(j['test'])


##### 中国网数据采集
# url_list = "http://about.china.com.cn/node_8027858_2.htm"
# respond = requests.get(url_list)
#
# bs = BeautifulSoup(respond.text, "lxml")
# news_div = bs.find("div", attrs={"class": "new_com"})
# news_ul = bs.find('ul')
# print(news_div)
#
# a_list = news_ul.find_all("a")
#
# for a in a_list:
#     print(a['href'])
#     print(a.text[2:len(a.text)])


# 文章详情

# url = "http://about.china.com.cn/2022-02/24/content_78069239.htm"
# respond = requests.get(url, timeout=1)
# respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
# bs = BeautifulSoup(respond.text, "lxml")
#
# _content = bs.find('div', attrs={'class': 'center_box'})
#
# _title = _content.find('h1')
#
# print(_title.text)
#
# _date_str = _content.find('b')
# _date_start_index = _date_str.text.index('发布时间：') + 5
# _date_end_index = _date_start_index + 19
# print(_date_str.text[_date_start_index:_date_end_index])
#
# p_list = _content.find_all('p')
# for p in p_list:
#     print(p.get_text())

##### 新华网数据采集
# url_list = "http://da.wa.news.cn/nodeart/page?nid=11246494&pgnum=5&cnt=50&attr=&tp=1&orderby=1&callback=jQuery112406766552067849669_1649501415239&_=1649501415241"
# respond = requests.get(url_list)
# respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
# bs = BeautifulSoup(respond.text, "lxml")


#
#
# resp_text = resp.text
#
# resp_text_json = resp_text[resp_text.index('(') + 1:(len(resp_text) - 2)]
#
# print(resp_text_json)
# resp_json = json.loads(resp_text_json)
#
# if resp_json['status'] == 0:
#     list_data = resp_json['data']['list']
#     if len(list_data) > 0:
#         for data in list_data:
#             print(data['Title'])
#             print(data['PubTime'])
#             print(data['keyword'])
#             print(data['LinkUrl'])
#
# # 详情请求
#
# url = "http://www.news.cn/2022-02/08/c_1211559565.htm"
# respond = requests.get(url, timeout=1)
# respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
# bs = BeautifulSoup(respond.text, "lxml")
#
# _content = bs.find('div', attrs={'id': 'detail'})
# p_list = _content.find_all('p')
# for p in p_list:
#     print(p.get_text())

# resp.json()
#
# resp.encoding = BeautifulSoup(resp.content,"lxml").original_encoding
# bs = BeautifulSoup(resp.text,"lxml")


###### 人民网列表及详情页爬虫

# url_list = "http://sports.people.com.cn/GB/419056/index1.html"
# resp = requests.get(url_list)
# resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding
# bs = BeautifulSoup(resp.text, "lxml")
#
# headingNews = bs.find('div',attrs={'class':'headingNews'})
# strong_list = headingNews.find_all('strong')
#
# for strong in strong_list:
#     a = strong.find('a')
#     print("http://sports.people.com.cn"+a['href'])
#     print(a.string)

# 详情页

# url = "http://sports.people.com.cn/n1/2020/0922/c14820-31869946.html"
# respond = requests.get(url, timeout=1)
# respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
# bs = BeautifulSoup(respond.text, "lxml")
# # span_list = bs.find_all('span')
# date_info = bs.find('div', attrs={'class': 'box01'})
# dtext = date_info.find('div', attrs={'class': 'fl'})
# print(dtext.get_text().lstrip())

# print(date_info.get_text())
#
# dtext = dtext.get_text().lstrip()
# if len(dtext) > 18:
#     dt = dtext[0:16]
#     print(dt)
#     time = datetime.datetime.strptime(dt, "%Y年%m月%d日%H:%M")
#     time2 = datetime.datetime.strftime(time, "%Y-%m-%d %H:%M:%S")
#     print(time2)
#
# _content = bs.find('div', attrs={'class': 'box_con'})
# p_list = _content.find_all('p')
# for p in p_list:
#     print(p.get_text())


# post_body = bs.find('div', attrs={'class': 'post_body'})
#
# p_list = post_body.find_all('p')
#
# for p in p_list:
#     print(p.get_text())


# mongodb 追加字段
# Conn = MongoClient('localhost', 27017)
# db = Conn['olympics_news_mining_db']
# collection = db.get_collection('news_data')
#
#
#
# #list = list(collection.find({"relevant_events": {"$exists": False}}))
#
# relevant_events = list(collection.find({},{'relevant_athletes_name':1}))

# print(relevant_events)


#
# relevant_events = [t['relevant_athletes_name'] for t in relevant_events ]
#
# print(['relevant_athletes_name'])


# collection.update_many({"relevant_events": {"$exists": False}}, {"$set": {"relevant_events": '', "relevant_athletes_name": ''}})

# print(len(list))
# for o in list:
#     #print(o['title'])
#     collection.update_one()
#     print(o['relevant_events'])


# python 数组去重
# data = ['羽生结弦', "羽生结弦" ,"羽生结弦", "键山优真" ,"宇野昌磨", "羽生结弦", "羽生结弦", "羽生结弦" ,"金博洋", "金博洋"]
# print(pd.unique(data).tolist())


# beautifulsoup 网易新闻爬虫test
# url = "https://www.163.com/sports/article/H0JG560200059CHO.html"
# respond = requests.get(url,timeout=1)
# respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
# bs = BeautifulSoup(respond.text, "lxml")
# # span_list = bs.find_all('span')
# post_info = bs.find('div', attrs={'class': 'post_info'})
# print(post_info.get_text())
#
# dtext = post_info.get_text().lstrip()
# if len(dtext) > 20:
#     dt = dtext[0:19]
#     print(dt)
#
# post_body = bs.find('div', attrs={'class': 'post_body'})
#
# p_list = post_body.find_all('p')
#
# for p in p_list:
#     print(p.get_text())

# pandas dataframe 转list 插入数据库
# import pandas as pd
#
# df = pd.DataFrame({'a': [1, 3, 5, 7, 4, 5, 6, 4, 7, 8, 9],
#                    'b': [3, 5, 6, 2, 4, 6, 7, 8, 7, 8, 9]})
#
#
# # print(df)
# print(df.iloc[0][0])
#
# print(df.shape[0])
# length = df.shape[0]
# Conn = MongoClient('localhost', 27017)
# db = Conn['test_data_db']
# collection = db.get_collection('test_data')
# for i in range(length):
#     print(df.iloc[i]['a'], df.iloc[i]['b'])
#     data = {
#         'a': int(df.iloc[i][0]),
#         'b': int(df.iloc[i][1])
#         # 'a': 1,
#         # 'b': 2
#     }
#     collection.insert_one(data)
#
#
# def ConnDB(self):
#     '''Connect to the mongodb.
#     '''
#     self._Conn = MongoClient(self.IP, self.PORT)

#
# json = df.to_json()
# print(json)

# array = df.to_xarray()

# print(array)

# 腾讯新闻抓取
# url_part = 'https://app.sports.qq.com/area/itemMore?sceneFlag=100500_pchome&from=pchome&moreContext='
#
# url_moreContext = '{"type":815,"pks":["1_11003_24802","2_11001_24802"],"lastID":"1_d332922rp27","count":20}'
#
# dataHasMore = True
# while dataHasMore:
#     resp = requests.get(url_part+url_moreContext)
#     resp_json = resp.json()
#     print(resp_json)
#     code = resp_json['code']
#     print(code)
#     if code == 0:
#         print('返回code为0')
#         type815 = resp_json['list'][0]['type815']
#         moreContext = type815['moreContext']
#         hasMore = type815['hasMore']
#         if hasMore != '1':
#             dataHasMore = False
#         news_list = type815['list']
#         print("获取新闻数量:"+str(len(news_list)))
#         print("列表lastid为："+moreContext)
#
#         url_moreContext = moreContext


# a = ['北京', '时间', '8', '月', '12', '日', '国际', '滑联', '官网', '报道', '越来越', '运动员', '回到', '冰场', '开启', '冰上', '训练', '包括', '两位', '荷兰', '名将', '国际', '滑联', '全能', '世锦赛', '冠军', '罗', '伊斯特', '女', '运动员', '德容', '4', '月', '6', '月', '新冠', '肺炎', '病毒', '影响', '运动员', '只能', '居家', '陆地', '训练', '7', '月初', '荷兰人', '罗', '伊斯特', '因策尔', '第一场', '冰上', '训练', '上周', '回到', '家乡', '海伦', '芬', '蒂亚夫', '冰场', '夏季', '训练', '国际', '滑联', '全能', '世锦赛', '冠军', '罗', '伊斯特', '说', '熟悉', '地方', '训练', '更好', '事情', '重返', '冰场', '轮滑', '爱', '冰上', '滑行', '感觉', '体能', '世界级', '名将', '只能', '利用', '轮滑', '公路', '滑行', '运动量', '回到', '冰场', '罗', '伊斯特', '感到', '舒适', '说', '重返', '冰场', '感觉', '太好了', '身体', '感觉良好', '抱怨', '德容', '享受', '上冰', '日子', '说', '因策尔', '训练', '10', '天', '恢复', '膝盖', '弯曲', '程度', '两周', '这太难', '回到', '冰上', '开心', '德容', '承认', '喜欢', '陆地', '训练', '说', '有时候', '希望', '离开', '冰面', '一段时间', '冬天', '回到', '冰上', '夏天', '骑车', '做', '冬天', '基础']
# print(' '.join(a))
# a = 1597192285000/1000
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a)))
#

# a = 'a'
# b = 'b'
# print(a+b)
#
# c = '{"data":[{"brief":"\n北京时间8月12日，据国际滑联官网报道，已经有越来越多的运动员重新回到了冰场开启了冰上训练，这其中就包括了两位荷兰名将：国际滑联全能世锦赛冠军罗伊斯特和女运动员德容。我很高兴，我们重返冰场了。德容也很享受…","imageInfoList":[{"width":0,"url":"http://p1.itc.cn/images01/20200812/196f225e0b204018a1d9e680122fe048.jpeg","height":0}],"images":["//p1.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200812/196f225e0b204018a1d9e680122fe048.jpeg"],"cmsId":0,"mobileTitle":"荷兰两名将开启冰上训练 世锦赛冠军：珍惜机会","mobilePersonalPage":"//m.sohu.com/media/99985320","type":2,"authorId":99985320,"authorPic":"http://sucimg.itc.cn/avatarimg/b5a7a6666d95475583ee028298246c50_1503286329312","title":"荷兰两名将开启冰上训练 世锦赛冠军：珍惜机会","url":"//www.sohu.com/a/412680751_99985320?scm=0.0.0.0","cover":"//p1.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200812/196f225e0b204018a1d9e680122fe048.jpeg","publicTime":1597192285000,"authorName":"搜狐综合体育","id":412680751,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXpvbmdoZXRpeXVAc29odS5jb20=","bigCover":"//p1.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200812/196f225e0b204018a1d9e680122fe048.jpeg","resourceType":1},{"brief":"本次调查是在2月份应体育部的要求启动的，此前10届法国冠军萨拉-阿比特博尔在一本书中说，她在1990-1992年期间被滑冰教练吉勒-拜尔强奸，当时她还是个青少年。根据体育部的说法，2月份有一名教练被拘留，另外…","imageInfoList":[{"width":0,"url":"http://p1.itc.cn/images01/20200806/03a533f46bd14b6abcf73c206f487bc0.jpeg","height":0}],"images":["//p1.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200806/03a533f46bd14b6abcf73c206f487bc0.jpeg"],"cmsId":0,"mobileTitle":"法国滑冰界深陷性丑闻 20多名教练被指控曾施暴","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"法国滑冰界深陷性丑闻 20多名教练被指控曾施暴","url":"//www.sohu.com/a/411701671_114977?scm=0.0.0.0","cover":"//p1.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200806/03a533f46bd14b6abcf73c206f487bc0.jpeg","publicTime":1596677146000,"authorName":"搜狐体育","id":411701671,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p1.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200806/03a533f46bd14b6abcf73c206f487bc0.jpeg","resourceType":1},{"brief":"他表示，中国联通致力于聚合产业生态优势资源，提出了“领航者计划”，与合作伙伴联合发起的“中国联通5G应用创新联盟”将孵化更多5G产业创新应用。此外，发布会现场还举行了智慧冬奥产业圆桌论坛，北京冬奥组委技术部部…","imageInfoList":[{"width":0,"url":"http://5b0988e595225.cdn.sohucs.com/images/20191226/f9a2dd033fe14d10bb14e987f7263788.png","height":0},{"width":0,"url":"http://5b0988e595225.cdn.sohucs.com/images/20191226/3fb7ce00e6f747879fde47a6680371a5.png","height":0}],"images":["//5b0988e595225.cdn.sohucs.com/q_70,c_lfill,w_300,h_200,g_faces/images/20191226/f9a2dd033fe14d10bb14e987f7263788.jpg"],"cmsId":0,"mobileTitle":"5G赋能智慧冬奥 中国联通打造三大场景十大应用","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"5G赋能智慧冬奥 中国联通打造三大场景十大应用","url":"//www.sohu.com/a/362978013_114977?scm=0.0.0.0","cover":"//5b0988e595225.cdn.sohucs.com/q_70,c_lfill,w_300,h_200,g_faces/images/20191226/f9a2dd033fe14d10bb14e987f7263788.jpg","publicTime":1577360910000,"authorName":"搜狐体育","id":362978013,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//5b0988e595225.cdn.sohucs.com/q_70,c_lfill,w_640,h_320,g_faces/images/20191226/f9a2dd033fe14d10bb14e987f7263788.jpg","resourceType":1},{"brief":"据北京国家速滑馆经营有限责任公司常务副总经理宋家峰介绍，冰丝带的冰面“非常有特色”，“因为这是一个全冰面设计，一般速滑馆只有一个400米跑道（是冰面），而我们把整个场心也全部做成了冰面。”据宋家峰介绍，冰丝带…","imageInfoList":[{"width":0,"url":"http://p8.itc.cn/images01/20200729/723454bee5294000869342eb05fb841e.jpeg","height":0}],"images":["//p8.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200729/723454bee5294000869342eb05fb841e.jpeg"],"cmsId":0,"mobileTitle":"探秘“冰丝带”里的“田径场”冬奥会后这里不只是速滑馆","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"探秘“冰丝带”里的“田径场”冬奥会后这里不只是速滑馆","url":"//www.sohu.com/a/410287241_114977?scm=0.0.0.0","cover":"//p8.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200729/723454bee5294000869342eb05fb841e.jpeg","publicTime":1595987411000,"authorName":"搜狐体育","id":410287241,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p8.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200729/723454bee5294000869342eb05fb841e.jpeg","resourceType":1},{"brief":"昨天，中国反兴奋剂中心在其官网公布了最新的兴奋剂违规处理结果，其中速度滑冰名帅冯庆波因为“组织、授意他人伪造证据，提供虚假信息”而被追加禁赛2年并负担20例兴奋剂检测费用，禁赛结束日期为2021年4月9日。这…","imageInfoList":[{"width":0,"url":"http://p2.itc.cn/images01/20200801/30626509fccf46b2beed4366b8cde964.jpeg","height":0}],"images":["//p2.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200801/30626509fccf46b2beed4366b8cde964.jpeg"],"cmsId":0,"mobileTitle":"东窗事发！ 速滑名帅组织授意伪造证据被追加禁赛","mobilePersonalPage":"//m.sohu.com/media/99985320","type":2,"authorId":99985320,"authorPic":"http://sucimg.itc.cn/avatarimg/b5a7a6666d95475583ee028298246c50_1503286329312","title":"东窗事发！ 速滑名帅组织授意伪造证据被追加禁赛","url":"//www.sohu.com/a/410887633_99985320?scm=0.0.0.0","cover":"//p2.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200801/30626509fccf46b2beed4366b8cde964.jpeg","publicTime":1596249562000,"authorName":"搜狐综合体育","id":410887633,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXpvbmdoZXRpeXVAc29odS5jb20=","bigCover":"//p2.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200801/30626509fccf46b2beed4366b8cde964.jpeg","resourceType":1},{"brief":"自1955年以来，FIL世界雪橇锦标赛一直在人工赛道上进行，而FIL世界雪橇自然赛道锦标赛则是在1979年推出。FIL加大了在人工赛道上引入女子双人滑雪橇的力度，该管理机构在5月宣布，计划从2021-2022…","imageInfoList":[{"width":0,"url":"http://p4.itc.cn/images01/20200727/e71c439065ec47179a70763c3a9cab55.jpeg","height":0}],"images":["//p4.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200727/e71c439065ec47179a70763c3a9cab55.jpeg"],"cmsId":0,"mobileTitle":"2026年冬奥会或增加两新项目 女子双人滑获力挺","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"2026年冬奥会或增加两新项目 女子双人滑获力挺","url":"//www.sohu.com/a/409873993_114977?scm=0.0.0.0","cover":"//p4.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200727/e71c439065ec47179a70763c3a9cab55.jpeg","publicTime":1595808567000,"authorName":"搜狐体育","id":409873993,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p4.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200727/e71c439065ec47179a70763c3a9cab55.jpeg","resourceType":1},{"brief":" \n北京时间7月21日，国际滑联（ISU）官网宣布，受疫情影响2020-2021赛季青年组大奖赛系列赛全部取消。国际滑联获悉，旅行和入境限制增加将使青少年花样滑冰运动员的旅行严重复杂化，其结果是一些国际滑联成…","imageInfoList":[{"width":0,"url":"http://p8.itc.cn/images01/20200721/21191931203c4f6882026c9e776f0c85.jpeg","height":0}],"images":["//p8.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200721/21191931203c4f6882026c9e776f0c85.jpeg"],"cmsId":0,"mobileTitle":"国际滑联：取消2020-2021赛季花样滑冰青年组大奖赛","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"国际滑联：取消2020-2021赛季花样滑冰青年组大奖赛","url":"//www.sohu.com/a/408835818_114977?scm=0.0.0.0","cover":"//p8.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200721/21191931203c4f6882026c9e776f0c85.jpeg","publicTime":1595308649000,"authorName":"搜狐体育","id":408835818,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p8.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200721/21191931203c4f6882026c9e776f0c85.jpeg","resourceType":1},{"brief":"身体半蹲，协调摆臂，快速疾跑-保持高频率  保持注意力集中听清口令 快速做出反应2分30秒滑冰姿势-协调性1分30秒保持滑冰姿势，双腿快速向外侧分腿再快速向内侧收腿身体保持俯卧姿势，绷直上体，双手虚放于双耳侧…","imageInfoList":[{"width":0,"url":"http://p9.itc.cn/images01/20200723/9d548b46e83b472998d60c7b0eea3886.jpeg","height":0},{"width":0,"url":"http://p8.itc.cn/images01/20200723/4e80c4edcf744d01bb525e642c5067b6.png","height":0},{"width":0,"url":"http://p4.itc.cn/images01/20200723/d05ff42de98a4e88811494148f49f06d.png","height":0},{"width":1080,"url":"http://p4.itc.cn/images01/20200723/d05ff42de98a4e88811494148f49f06d.png","height":602},{"width":277,"url":"http://p8.itc.cn/images01/20200723/e8d70ce154e64ced84ac9297e0bd7ee5.gif","height":157},{"width":277,"url":"http://p1.itc.cn/images01/20200723/d1b1f2e57d254e55a48df3e85d1ffbe4.gif","height":157},{"width":277,"url":"http://p2.itc.cn/images01/20200723/1cba5a4a3eac41ceb363c561fac7c5dd.gif","height":157},{"width":277,"url":"http://p9.itc.cn/images01/20200723/a6c7421f5ee049b98955fae4592899a1.gif","height":157},{"width":316,"url":"http://p3.itc.cn/images01/20200723/b1658b2bc5b642c984ecbf10493e8ec8.gif","height":179},{"width":316,"url":"http://p9.itc.cn/images01/20200723/180f9fd8321f4e3b8f910bb9167e0ffc.gif","height":179},{"width":277,"url":"http://p2.itc.cn/images01/20200723/fb74cadb51b74d5a95203eb602b07427.gif","height":157},{"width":277,"url":"http://p9.itc.cn/images01/20200723/e832f9f9ce404b9b913700d4d2cf511f.gif","height":157},{"width":277,"url":"http://p1.itc.cn/images01/20200723/1d959ec4adf740e6abf33d71085fea68.gif","height":157},{"width":316,"url":"http://p5.itc.cn/images01/20200723/54d324aec5704dfb8f31d08f40d0d63a.gif","height":179},{"width":316,"url":"http://p2.itc.cn/images01/20200723/b56ad862ec26406e91aba814cef3d6e1.gif","height":179},{"width":277,"url":"http://p1.itc.cn/images01/20200723/88e2652ffd794309b531d053da7518c6.gif","height":157},{"width":316,"url":"http://p9.itc.cn/images01/20200723/adc5fb88df1948d19f4ba9bffb76a09d.gif","height":179}],"images":["//p9.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200723/9d548b46e83b472998d60c7b0eea3886.jpeg"],"cmsId":0,"mobileTitle":"全国青少年U系列滑冰比赛 参赛资格体能达标测试说明","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"全国青少年U系列滑冰比赛 参赛资格体能达标测试说明","url":"//www.sohu.com/a/409190355_114977?scm=0.0.0.0","cover":"//p9.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200723/9d548b46e83b472998d60c7b0eea3886.jpeg","publicTime":1595464999000,"authorName":"搜狐体育","id":409190355,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p9.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200723/9d548b46e83b472998d60c7b0eea3886.jpeg","resourceType":1},{"brief":"北京时间7月15日，据美联社报道，日本奥委会主席表示，如果东京能够成功举办明年的夏季奥运会，那么札幌市就可以有条件举办2030年的冬季奥运会。札幌举办了1972年冬季奥运会，盐湖城是2002年的东道主，巴塞罗…","imageInfoList":[{"width":0,"url":"http://p7.itc.cn/images01/20200715/075e11f99ca14bc3935e3de8da3155b1.jpeg","height":0}],"images":["//p7.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200715/075e11f99ca14bc3935e3de8da3155b1.jpeg"],"cmsId":0,"mobileTitle":"日本札幌欲申办2030冬奥会 两大竞争对手实力强","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"日本札幌欲申办2030冬奥会 两大竞争对手实力强","url":"//www.sohu.com/a/407679076_114977?scm=0.0.0.0","cover":"//p7.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200715/075e11f99ca14bc3935e3de8da3155b1.jpeg","publicTime":1594773850000,"authorName":"搜狐体育","id":407679076,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p7.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200715/075e11f99ca14bc3935e3de8da3155b1.jpeg","resourceType":1},{"brief":"北京时间7月19日，据国际奥委会（IOC）透露，江原道2024年冬季青年奥林匹克运动会组委会将于今年年底前成立。江原道在1月获得2024年冬季青年奥运会的举办权。青奥会已被用作新的比赛项目的试验场，可能会有更…","imageInfoList":[{"width":0,"url":"http://p3.itc.cn/images01/20200719/ac304a14ee0f443393001993a062c9a1.jpeg","height":0}],"images":["//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200719/ac304a14ee0f443393001993a062c9a1.jpeg"],"cmsId":0,"mobileTitle":"2024冬青奥会组委会年底成立 江原道将利用平昌遗产","mobilePersonalPage":"//m.sohu.com/media/99985320","type":2,"authorId":99985320,"authorPic":"http://sucimg.itc.cn/avatarimg/b5a7a6666d95475583ee028298246c50_1503286329312","title":"2024冬青奥会组委会年底成立 江原道将利用平昌遗产","url":"//www.sohu.com/a/408447826_99985320?scm=0.0.0.0","cover":"//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20200719/ac304a14ee0f443393001993a062c9a1.jpeg","publicTime":1595120084000,"authorName":"搜狐综合体育","id":408447826,"scm":"0.0.0.0","personalPage":"http://mp.sohu.com/profile?xpt=c29odXpvbmdoZXRpeXVAc29odS5jb20=","bigCover":"//p3.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20200719/ac304a14ee0f443393001993a062c9a1.jpeg","resourceType":1},{"brief":"王启宏向新京报记者回忆，他作品里第一个被张艺谋选中的，是八达岭长城的一段航拍，拍摄于去年3月，后来，它成为二十四节气倒计时的开场画面，“张导对我说，这段视频拍出了一种‘水墨长城’的意境，长城的脉络走向恰似巨龙…","imageInfoList":[{"width":2254,"url":"https://p3.itc.cn/q_70/images03/20220303/4b1dd29aecc14bbb86f49b504b05180a.jpeg","height":1234},{"width":3597,"url":"https://p3.itc.cn/q_70/images03/20220303/f27041d073544706886e958adf9cb866.jpeg","height":2257},{"width":3000,"url":"https://p8.itc.cn/q_70/images03/20220303/d17ac40e901d432c9166974f8b4723c2.jpeg","height":1687},{"width":5227,"url":"https://p4.itc.cn/q_70/images03/20220303/10bf0af0e0824285ad072dbdc0d5ae6f.jpeg","height":2942},{"width":2276,"url":"https://p9.itc.cn/q_70/images03/20220303/5f65b9691ab044818f7480c844ca5164.jpeg","height":1280},{"width":1101,"url":"https://p2.itc.cn/q_70/images03/20220303/a7635db39460470ea33c072d60c1770b.png","height":598},{"width":1706,"url":"https://p4.itc.cn/q_70/images03/20220303/e29216128d1f4f499cbda8e8579a99c2.jpeg","height":1279},{"width":1279,"url":"https://p8.itc.cn/q_70/images03/20220303/88fb87bc14f7475585c294f90754d681.jpeg","height":1706},{"width":3000,"url":"https://p4.itc.cn/q_70/images03/20220303/12147a41045848318107c7bd3bec9547.jpeg","height":1688},{"width":2276,"url":"https://p5.itc.cn/q_70/images03/20220303/cbd0a976572d4d8d911d607bd385be35.jpeg","height":1280},{"width":1108,"url":"https://p0.itc.cn/q_70/images03/20220303/e58e6a44ffaf4f31b5992ebf4d89248b.png","height":623}],"images":["//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220303/4b1dd29aecc14bbb86f49b504b05180a.jpeg"],"cmsId":0,"mobileTitle":"冬奥24节气短片背后的两位摄影“狂人”","mobilePersonalPage":"//m.sohu.com/media/114988","type":2,"authorId":114988,"authorPic":"//5b0988e595225.cdn.sohucs.com/a_auto,c_cut,x_39,y_0,w_302,h_302/images/20200405/b45b5c391f7e48fd9dc699f6bbed02ef.png","title":"冬奥24节气短片背后的两位摄影“狂人”","url":"//www.sohu.com/a/526972112_114988?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220303/4b1dd29aecc14bbb86f49b504b05180a.jpeg","publicTime":1646307911000,"authorName":"新京报","id":526972112,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdDNqdHpnY0Bzb2h1LmNvbQ==","bigCover":"//p3.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220303/4b1dd29aecc14bbb86f49b504b05180a.jpeg","resourceType":1},{"brief":"3日，中国体育代表团宣布，郭雨洁、汪之栋将担任北京冬残奥会开幕式中国体育代表团旗手。残奥越野滑雪和冬季两项女运动员郭雨洁，2004年3月出生，来自河北，曾获得2021年芬兰欧洲杯冬季两项女子站姿组短距离第三名…","imageInfoList":[{"width":1024,"url":"https://p8.itc.cn/q_70/images03/20220303/7ac5fa22bf624b5ba576f37df4deb4ba.jpeg","height":681},{"width":1024,"url":"https://p7.itc.cn/q_70/images03/20220303/2cc7b9f56e5f4e30a6f156e9697b2d58.jpeg","height":680}],"images":["//p9.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220303/d31adeb1865d455ebeaf86341c0fd355.jpeg"],"cmsId":0,"mobileTitle":"开幕式旗手公布！","mobilePersonalPage":"//m.sohu.com/media/116237","type":2,"authorId":116237,"authorPic":"//p5.itc.cn/c_cut,x_68,y_132,w_666,h_666/images01/20200729/cfadafd7343548888dd03bc2f81394f4.jpeg","title":"开幕式旗手公布！","url":"//www.sohu.com/a/526892020_116237?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p9.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220303/d31adeb1865d455ebeaf86341c0fd355.jpeg","publicTime":1646290794000,"authorName":"红星新闻","id":526892020,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdGp4emFlc0Bzb2h1LmNvbQ==","bigCover":"//p9.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220303/d31adeb1865d455ebeaf86341c0fd355.jpeg","resourceType":1},{"brief":"北京时间3月3日，根据NBC消息，中国运动员将不会参加2022年的花样滑冰世界锦标赛，这意味着在北京冬奥会刚刚拿下双人滑冠军的隋文静/韩聪不会出现在法国蒙彼利埃。隋文静/韩聪在2018年的平昌冬奥会上以0.4…","imageInfoList":[{"width":1024,"url":"https://p6.itc.cn/q_70/images01/20220303/b1982a294fde4b8bb233550353c002ea.jpeg","height":576}],"images":["//p6.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20220303/b1982a294fde4b8bb233550353c002ea.jpeg"],"cmsId":0,"mobileTitle":"外媒：中国运动员不参加2022花滑世锦赛 陈巍宣布回归校园","mobilePersonalPage":"//m.sohu.com/media/114977","type":2,"authorId":114977,"authorPic":"http://5b0988e595225.cdn.sohucs.com/avatar/picon/2012/05/18/1337337319030.png","title":"外媒：中国运动员不参加2022花滑世锦赛 陈巍宣布回归校园","url":"//www.sohu.com/a/526829289_114977?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p6.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20220303/b1982a294fde4b8bb233550353c002ea.jpeg","publicTime":1646280720000,"authorName":"搜狐体育","id":526829289,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHlwbHRodEBzb2h1LmNvbQ==","bigCover":"//p6.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20220303/b1982a294fde4b8bb233550353c002ea.jpeg","resourceType":1},{"brief":"关于冬残奥会的六大知识点可你知道3月13日就闭幕了吗你想要的，都有因为少了刷冰这一过程剩下的就只能靠冰壶自己了知识点四：球杆的小秘密残奥冰球是坐着冰橇进行的冬残奥会的“金牌大户”足以看出这项目的分量知识点六：…","imageInfoList":[{"width":500,"url":"https://p6.itc.cn/q_70/images03/20220303/5f26fd7afc554e3a86f76c310e74a088.gif","height":217},{"width":570,"url":"https://p8.itc.cn/q_70/images03/20220303/3e2e7e7eb0dc49faa4b444c176a6bde4.jpeg","height":310},{"width":570,"url":"https://p8.itc.cn/q_70/images03/20220303/4611b82a78454be8ba611345cba4be90.jpeg","height":380},{"width":360,"url":"https://p1.itc.cn/q_70/images03/20220303/13551276606f454fa20e0dea483142d0.gif","height":225},{"width":540,"url":"https://p2.itc.cn/q_70/images03/20220303/52d7dbfa3b9547d9981353f66870e06f.gif","height":804}],"images":["//p6.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220303/5f26fd7afc554e3a86f76c310e74a088.gif"],"cmsId":0,"mobileTitle":"追光丨冬残奥会的六大知识点，小编不允许你不知道","mobilePersonalPage":"//m.sohu.com/media/267106","type":2,"authorId":267106,"authorPic":"https://statics.itc.cn/mp-new/xinhuashe-logo.jpg","title":"追光丨冬残奥会的六大知识点，小编不允许你不知道","url":"//www.sohu.com/a/526819389_267106?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p6.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220303/5f26fd7afc554e3a86f76c310e74a088.gif","publicTime":1646276968000,"authorName":"新华社","id":526819389,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHNiZ3E2ZnFAc29odS5jb20=","bigCover":"//p6.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220303/5f26fd7afc554e3a86f76c310e74a088.gif","resourceType":1},{"brief":"冬奥结束后，武大靖开启了直播，作为嘉宾，花样滑冰名将张昊似乎无法理解短道速滑运动员的困难，而且在直播说出“你们短道的伤好恢复”等争议言论。为此，冰迷无法接受这样的奇葩言论，集体攻陷了张昊的微博。张昊曾因疑似摔…","imageInfoList":[{"width":818,"url":"https://p1.itc.cn/images01/20220303/5f3687588b824730818576181aeff79c.png","height":1036},{"width":989,"url":"https://p4.itc.cn/images01/20220303/14192889902e427bb3b83f2308f23596.png","height":710},{"width":726,"url":"https://p8.itc.cn/images01/20220303/e6f31cc924df4ea79276668ed99e1c53.png","height":562},{"width":869,"url":"https://p8.itc.cn/images01/20220303/9a7baf513d0c4771a469b37cf5defa18.png","height":1237}],"images":["//p1.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20220303/5f3687588b824730818576181aeff79c.jpg"],"cmsId":0,"mobileTitle":"花滑传奇微博又被攻陷！对武大靖的迷惑言论：你们短道的伤好恢复","mobilePersonalPage":"//m.sohu.com/media/495997","type":2,"authorId":495997,"authorPic":"http://sucimg.itc.cn/avatarimg/2fb7ec899619405fa135d939cbbb9f1d_1473850743768","title":"花滑传奇微博又被攻陷！对武大靖的迷惑言论：你们短道的伤好恢复","url":"//www.sohu.com/a/526762135_495997?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p1.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20220303/5f3687588b824730818576181aeff79c.jpg","publicTime":1646265880000,"authorName":"天外居","id":526762135,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=cHBhZzIwMzE5NzVhZjhlMEBzb2h1LmNvbQ==","bigCover":"//p1.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20220303/5f3687588b824730818576181aeff79c.jpg","resourceType":1},{"brief":"原本以为谷爱凌是一个全方位发展的学霸，在各方面都是非常优异，但是让人没想到的是谷爱凌的字迹与我们普通人也是差别不大呀，可能还有很多人会很自豪地说，“我比谷爱凌强多了！”况且对于我们普通人来说，并没有谷爱凌那么…","imageInfoList":[{"width":632,"url":"https://p3.itc.cn/images01/20220303/60d3d1f5fa624bfc9f694b6825236367.png","height":356},{"width":537,"url":"https://p0.itc.cn/images01/20220303/cdb791c7fbc04506a4ff7f62283329be.png","height":759},{"width":716,"url":"https://p2.itc.cn/images01/20220303/836677a140b04ef789e83195138133ce.png","height":490},{"width":821,"url":"https://p4.itc.cn/images01/20220303/50f68135b97c41018578a2890946672c.png","height":790},{"width":592,"url":"https://p4.itc.cn/images01/20220303/33eee1d4f5df4989baaf16479e1fe8f6.png","height":621},{"width":590,"url":"https://p2.itc.cn/images01/20220303/666f7cf9f2ad44b3857a548c55830199.png","height":492},{"width":590,"url":"https://p2.itc.cn/images01/20220303/71a3cd48cbb24dab979287ae049d740c.png","height":390},{"width":593,"url":"https://p3.itc.cn/images01/20220303/6e0292930be048a69abba16beb4fc656.png","height":759}],"images":["//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20220303/60d3d1f5fa624bfc9f694b6825236367.jpg"],"cmsId":0,"mobileTitle":"原以为谷爱凌是全方位发展的学霸，没想到这一点和普通人差不多","mobilePersonalPage":"//m.sohu.com/media/100153652","type":2,"authorId":100153652,"authorPic":"//5b0988e595225.cdn.sohucs.com/a_auto,c_cut,x_27,y_1,w_314,h_314/images/20180416/00ae9a8e401e4e06b4d471bd6fd3004e.jpeg","title":"原以为谷爱凌是全方位发展的学霸，没想到这一点和普通人差不多","url":"//www.sohu.com/a/526759757_100153652?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images01/20220303/60d3d1f5fa624bfc9f694b6825236367.jpg","publicTime":1646264271000,"authorName":"张女子育儿","id":526759757,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=Qjg4RkM3NTE5MkY4QkJBNURGQTI2ODA4OUE4QjNCRDJAcXEuc29odS5jb20=","bigCover":"//p3.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images01/20220303/60d3d1f5fa624bfc9f694b6825236367.jpg","resourceType":1},{"brief":"有超过20余位运动员参与了快手直播活动，包括张会、陈雨菲、邓亚萍，王大雷、潘晓婷等明星运动员都在快手平台上讲述了他们与冬奥的故事；快手调动了40个以上的垂直门类达人积极参与奥运内容制作，为用户提供了更多的视角…","imageInfoList":[{"width":640,"url":"https://p7.itc.cn/q_70/images03/20220302/66d938c1fb70472280ce8800e0ec46a9.png","height":620},{"width":419,"url":"https://p3.itc.cn/q_70/images03/20220302/0228126f929248a4b4522fe3a8d7ee55.png","height":749},{"width":640,"url":"https://p4.itc.cn/q_70/images03/20220302/7a35b54226eb4f53b43dbfeef3afff09.png","height":357},{"width":640,"url":"https://p6.itc.cn/q_70/images03/20220302/818592d84e9c4bc297d283e1624f623f.png","height":463},{"width":640,"url":"https://p3.itc.cn/q_70/images03/20220302/bf864f4c0be1402d8868db52871a2993.png","height":427},{"width":640,"url":"https://p4.itc.cn/q_70/images03/20220302/c6844728dc5d4fbab4e3fd19bf3be1c6.png","height":363},{"width":640,"url":"https://p3.itc.cn/q_70/images03/20220302/cd2ea2c5b01d48beb4153d96b47d1e1d.png","height":440},{"width":640,"url":"https://p7.itc.cn/q_70/images03/20220302/89e856caf8e9454eb5551a1bc9bd8029.png","height":428}],"images":["//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/0228126f929248a4b4522fe3a8d7ee55.jpg"],"cmsId":0,"mobileTitle":"快手的“体育版图”不止冬奥会","mobilePersonalPage":"//m.sohu.com/media/104421","type":2,"authorId":104421,"authorPic":"http://sucimg.itc.cn/avatarimg/a1edab8603984519b47edd8d2c3890de_1411866165856","title":"快手的“体育版图”不止冬奥会","url":"//www.sohu.com/a/526701268_104421?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p3.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/0228126f929248a4b4522fe3a8d7ee55.jpg","publicTime":1646226785000,"authorName":"砍柴网","id":526701268,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=NTYxNTY3NTE0RjAzREYzRkI2MDI2QzVBQzdFNzQyNjlAcXEuc29odS5jb20=","bigCover":"//p3.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220302/0228126f929248a4b4522fe3a8d7ee55.jpg","resourceType":1},{"brief":"品牌对于谷爱凌的青睐，随着赛事的来临愈加明显，而对于早期就开始押宝的品牌来说，显然更有先发之势。当然，正如晓燕所说，冬奥这种赛事也不是每年都有，对于这些品牌来说，体育赛事的存在，更像是一个固定的营销节点，而2…","imageInfoList":[{"width":640,"url":"https://p6.itc.cn/q_70/images03/20220302/6a26d090da6948c2bcc56476706cd3a6.png","height":220},{"width":628,"url":"https://p0.itc.cn/q_70/images03/20220302/0176710049de4ebab40df589705cd7fb.png","height":495},{"width":640,"url":"https://p7.itc.cn/q_70/images03/20220302/02e0fb8100944057aaf6e5d9bd9f82e9.png","height":422},{"width":640,"url":"https://p9.itc.cn/q_70/images03/20220302/1e1aef8f9b3a4b9691b06185da2de287.png","height":285},{"width":640,"url":"https://p1.itc.cn/q_70/images03/20220302/09e30b2c93a442d5a8dfda036eeef73f.png","height":437},{"width":640,"url":"https://p4.itc.cn/q_70/images03/20220302/72463c08a52e4fd4934785785ab6a8de.png","height":342}],"images":["//p9.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/1e1aef8f9b3a4b9691b06185da2de287.jpg"],"cmsId":0,"mobileTitle":"冬奥、亚运会、世界杯，顶级运动员与头部品牌们的营销盛宴","mobilePersonalPage":"//m.sohu.com/media/104421","type":2,"authorId":104421,"authorPic":"http://sucimg.itc.cn/avatarimg/a1edab8603984519b47edd8d2c3890de_1411866165856","title":"冬奥、亚运会、世界杯，顶级运动员与头部品牌们的营销盛宴","url":"//www.sohu.com/a/526699571_104421?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p9.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/1e1aef8f9b3a4b9691b06185da2de287.jpg","publicTime":1646226044000,"authorName":"砍柴网","id":526699571,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=NTYxNTY3NTE0RjAzREYzRkI2MDI2QzVBQzdFNzQyNjlAcXEuc29odS5jb20=","bigCover":"//p9.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220302/1e1aef8f9b3a4b9691b06185da2de287.jpg","resourceType":1},{"brief":"除了在自制优质内容上与品牌的深度共建，快手还发挥短视频平台天然具备的强互动优势，通过冬奥倒计时、短视频大赛、赛事预测、轻互动游戏、定制魔表挑战赛等创意互动玩法，引爆冬奥氛围主场，由此为品牌提供冠名、场景植入、…","imageInfoList":[{"width":577,"url":"https://p1.itc.cn/q_70/images03/20220302/709ea74138764304a03075edb1553a0c.png","height":936},{"width":553,"url":"https://p1.itc.cn/q_70/images03/20220302/4295e391dc1d4d8b8779d190a2bd00f9.png","height":809},{"width":555,"url":"https://p4.itc.cn/q_70/images03/20220302/b725583781bb4b5ea8858f1513a043e0.png","height":818},{"width":960,"url":"https://p4.itc.cn/q_70/images03/20220302/cce06f81e3034fada4d2939d2d88ce42.png","height":884},{"width":662,"url":"https://p7.itc.cn/q_70/images03/20220302/83e968ac51344229b3826808c0556ac1.png","height":857}],"images":["//p4.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/cce06f81e3034fada4d2939d2d88ce42.jpg"],"cmsId":0,"mobileTitle":"快手冬奥相关内容播放量超1544.8亿，二十余品牌共赴磁力引擎冰雪之约","mobilePersonalPage":"//m.sohu.com/media/104421","type":2,"authorId":104421,"authorPic":"http://sucimg.itc.cn/avatarimg/a1edab8603984519b47edd8d2c3890de_1411866165856","title":"快手冬奥相关内容播放量超1544.8亿，二十余品牌共赴磁力引擎冰雪之约","url":"//www.sohu.com/a/526677019_104421?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p4.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/cce06f81e3034fada4d2939d2d88ce42.jpg","publicTime":1646220311000,"authorName":"砍柴网","id":526677019,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=NTYxNTY3NTE0RjAzREYzRkI2MDI2QzVBQzdFNzQyNjlAcXEuc29odS5jb20=","bigCover":"//p4.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220302/cce06f81e3034fada4d2939d2d88ce42.jpg","resourceType":1},{"brief":"直播吧3月2日讯据接近EA的记者TomHenderson的消息称，EA将从FIFA和NHL（冰球大联盟）游戏中移除俄罗斯国家队的形象。记者表示EA是通过一封邮件宣布了这一决定，目前尚不清楚俄罗斯的俱乐部球队、…","imageInfoList":[{"width":750,"url":"https://p8.itc.cn/q_70/images03/20220302/4b1e1000e54149e6b106a8fffde292ab.jpeg","height":334}],"images":["//p8.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/4b1e1000e54149e6b106a8fffde292ab.jpeg"],"cmsId":0,"mobileTitle":"记者：EA将在FIFA和NHL游戏中移除俄罗斯国家队","mobilePersonalPage":"//m.sohu.com/media/362070","type":2,"authorId":362070,"authorPic":"http://sucimg.itc.cn/avatarimg/075c9f9e449948a0bc41eca1c4034f61_1479869067548","title":"记者：EA将在FIFA和NHL游戏中移除俄罗斯国家队","url":"//www.sohu.com/a/526684832_362070?scm=1002.27140046.0.SHARINGAN_SPORTS","cover":"//p8.itc.cn/q_70,c_lfill,w_300,h_200,g_faces/images03/20220302/4b1e1000e54149e6b106a8fffde292ab.jpeg","publicTime":1646220240000,"authorName":"直播吧","id":526684832,"scm":"1002.27140046.0.SHARINGAN_SPORTS","personalPage":"http://mp.sohu.com/profile?xpt=c29odXptdHZlcW5hOGRAc29odS5jb20=","bigCover":"//p8.itc.cn/q_70,c_lfill,w_640,h_320,g_faces/images03/20220302/4b1e1000e54149e6b106a8fffde292ab.jpeg","resourceType":1}],"message":"success","status":0}'
#
# cj = json.loads(c.replace('\n',''))
# print(cj)

# json_array = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}, {'a': 5, 'b': 6}]
# a = []
# for json in json_array:
#     a.append(json['a'])
# print(a)
#
# a = 'jQuery112404795035418247082_1646742803500({"data":[{"brie}}}}'
# print(a.find('{'))
# print(a.rfind('}'))
# print(a[a.find('{'):a.rfind('}')])

# j = {'a': 1, 'b': 2}
# print(json.dumps(j))
#
# a={'a': 1, 'b': 2}
# result=json.dumps(a)
# print(json.dumps(a))
# print(type(result))

# def extractData(json_array, tag_list):
#     '''Extract data from specific json_data.
#
#     # Arguments:
#         json_array: json data.
#         tag_list: List of tags that need to be extracted.
#     '''
#
#
#     Dict = {}
#     for tag in tag_list:
#         data = []
#         for json in json_array:
#             data.append(json[tag])
#             Dict.update({tag: np.array(data)})
#
#         # exec("for json in json_array:")
#         # exec("  data.append(json["+'tag'+"])")
#         # exec("  Dict.update({'" + tag + "' : np.array(data)})")
#
#     dataFrame = pd.DataFrame(Dict, columns=tag_list)
#     for tag in tag_list:
#         print(dataFrame.get(tag))
#     print(dataFrame)
#     return dataFrame
#
# extractData(json_array,['a','b'])

# respond = requests.get(
#     "//api.beijing2022.cn/search/web?callback=getList1447&language=zh&page=1&limit=50&isPar=1&is_filter=2&column=26&_=1646742126903")
# #
# for news in respond.json()['data']['list']:
#     print(news)

# data = [1,2,3,4]
# print ("|".join(str(i) for i in data))


# def countchn( string):
#     '''计算中文数量和中文出现的频率。
#
#     # Arguments:
#         string: Each part of crawled website analyzed by BeautifulSoup.
#     '''
#     pattern = re.compile(u'[\u1100-\uFFFDh]+?')
#     result = pattern.findall(string)
#     chnnum = len(result)
#     possible = chnnum / len(str(string))
#     return (chnnum, possible)
#
# print(countchn("秦飞"))
#
# with open("athletes.json",'r',encoding="utf-8") as load_f:
#     load_dict = json.load(load_f)
#    # print(load_dict)
#     for dict in load_dict['data']:
#         print(dict['name'])

# print(str(os.getcwd()+"\\athletes.json"))


# def extractData(self, dbName, colName, tag_list):
#     '''Extract data from specific collection of specific database.
#
#     # Arguments:
#         dbName: Name of database.
#         colName: Name of collection.
#         tag_list: List of tags that need to be extracted.
#     '''
#
#
#     db = self._Conn[dbName]
#     collection = db.get_collection(colName)
#     data = []
#     Dict = {}
#     for tag in tag_list:
#         exec(tag + " = collection.distinct('" + tag + "')")
#         exec("data.append(" + tag + ")")
#         exec("Dict.update({'" + tag + "' : np.array(" + tag + ")})")
#     dataFrame = pd.DataFrame(Dict, columns=tag_list)
#     return dataFrame
#
# extractData('BJ2022CN_News_DB','bj2022cn_news',['Title','Date'])
# IP="localhost"
# PORT=27017
# dbName="BJ2022CN_News_DB"
# collectionName="bj2022cn_news"
# _Conn = MongoClient(IP, PORT)
# db = _Conn[dbName]
# collection = db.get_collection(collectionName)
# data = []
# Dict = {}
# title = collection.distinct('Title')
# print(title)
# data.append(title)
# print(np.array(title))
#
# Dict.update({'Tittle':np.array(title)})
# # for tag in tag_list:
# #     exec(tag + " = collection.distinct('" + tag + "')")
# #     exec("data.append(" + tag + ")")
# #     exec("Dict.update({'" + tag + "' : np.array(" + tag + ")})")
# #
# dataFrame = pd.DataFrame(Dict, columns=['Title'])
