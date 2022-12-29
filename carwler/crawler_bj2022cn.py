# -*- coding: utf-8 -*-

import time, re, requests
from concurrent import futures
from bs4 import BeautifulSoup
from pymongo import MongoClient
import text_analysis.text_mining as tm

import gevent
from gevent import monkey, pool


# monkey.patch_all()


class WebCrawlFromBJ2022CN(object):
    '''从北京冬奥官网新闻列表页 'https://www.beijing2022.cn/cn/paralympics/newslist.htm' 抓取新闻数据.采用API_JSON方式，不用解析HTML

    # Arguments:
        totalPages: 要抓取数据的总页数(int type).
        Range: 多线程处理每个现成处理的页数(int type).
        ThreadsNum: 启动线程数(int type).
        dbName: 数据库名称(string type).
        colName: 数据库集合名称(string type).
        IP: 数据库连接IP(string type).
        PORT: 数据库连接端口s(int type).
    '''

    def __init__(self, *arg, **kwarg):
        self.totalPages = arg[0]  # totalPages
        self.Range = arg[1]  # Range
        self.ThreadsNum = kwarg['ThreadsNum']
        self.dbName = kwarg['dbName']
        self.colName = kwarg['collectionName']
        self.IP = kwarg['IP']
        self.PORT = kwarg['PORT']
        self.Porb = .5
        self.realtimeNewsURL = []
        self.tm = tm.TextMining(IP="localhost", PORT=27017)

    def countchn(self, string):
        '''计算中文数字和中文出现的频率。

        # Arguments:
            string: Each part of crawled website analyzed by BeautifulSoup.
        '''
        pattern = re.compile(u'[\u1100-\uFFFDh]+?')
        result = pattern.findall(string)
        chnnum = len(result)
        possible = chnnum / len(str(string))
        return (chnnum, possible)

    def getUrlInfo(self, news_id, url):
        '''Analyze website and extract useful information.
               '''
        news_data_url = "https://api.beijing2022.cn/bj2022/newsDetail?from=web&callback=__jp0&id=" + news_id
        respond = requests.get(news_data_url)
        article = ''
        date = ''
        summary = ''
        keyWords = ''
        code = respond.json()['code']
        if code == 0:
            news_data = respond.json()['data']
            date = news_data['pub_time']
            title = news_data['title']
            summary = news_data['title']
            keyWords = (",".join(str(tag) for tag in news_data['tags']))
            article = news_data['cntHtml']

            time1 = time.time()
            while article.find('<') != -1 and article.find('>') != -1:
                string = article[article.find('<'):article.find('>') + 1]
                article = article.replace(string, '')
                time2 = time.time()
                if time2 - time1 > 60:
                    print(' [*] 循环超时60s，跳出循环 ... ')
                    break

            time1 = time.time()
            while article.find('\u3000') != -1:
                article = article.replace('\u3000', '')
                time2 = time.time()
                if time2 - time1 > 60:
                    print(' [*] 循环超时60s，跳出循环 ... ')
                    break

            article = ' '.join(re.split(' +|\n+', article)).strip()

        return url, title, summary, keyWords, date, article

    def GenPagesLst(self):
        '''Generate page number list using Range parameter.
        '''
        PageLst = []
        k = 1
        while k + self.Range - 1 <= self.totalPages:
            PageLst.append((k, k + self.Range - 1))
            k += self.Range
        if k + self.Range - 1 < self.totalPages:
            PageLst.append((k, self.totalPages))
        return PageLst

    def CrawlHistoryOlympicsNews(self, startPage, endPage):
        '''Crawl historical company news 
        '''
        self.ConnDB()
        AddressLst = self.extractData(['address'])[0]
        if AddressLst == []:
            urls = []
            url_Part_1 = 'https://api.beijing2022.cn/search/web?callback=getList3287&language=zh&limit=50&is_filter=2&column=focusnews&_=1646888743448&page='
            for pageId in range(startPage, endPage + 1):
                if startPage < 10:
                    urls.append(url_Part_1 + str(pageId))
                else:
                    urls.append(url_Part_1 + str(pageId))
            for url in urls:
                print(url)
                resp = requests.get(url)
                news_list = resp.json()['data']['list']

                for a in news_list:
                    url, title, summary, keyWords, date, article = self.getUrlInfo(a['newsId'], a['url'])

                    if article != '':
                        data = {
                            'title': title,
                            'date': date,
                            'address': url,
                            'keywords': keyWords,
                            'summary': summary,
                            'article': article,
                            'site': 'beijing2022cn',
                            'relevant_athletes_name':'',
                            'relevant_events':''
                        }
                        self._collection.insert_one(data)
        else:
            urls = []
            url_Part_1 = 'https://api.beijing2022.cn/search/web?callback=getList3287&language=zh&limit=50&is_filter=2&column=focusnews&_=1646888743448&page='

            for pageId in range(startPage, endPage + 1):
                urls.append(url_Part_1 + str(pageId))
            for url in urls:
                print(' <Re-Crawl url> ', url)
                resp = requests.get(url)
                news_list = resp.json()['data']['list']

                for a in news_list:
                    url, title, summary, keyWords, date, article = self.getUrlInfo(a['newsId'], a['url'])

                    if article != '':
                        data = {
                            'title': title,
                            'date': date,
                            'address': url,
                            'keywords': keyWords,
                            'summary': summary,
                            'article': article,
                            'site': 'beijing2022cn',
                            'relevant_athletes_name': '',
                            'relevant_events': ''
                        }
                        self._collection.insert_one(data)

    def ConnDB(self):
        '''Connect mongodb.
        '''
        Conn = MongoClient(self.IP, self.PORT)
        db = Conn[self.dbName]
        self._collection = db.get_collection(self.colName)

    def extractData(self, tag_list):
        '''Extract column data with tag in 'tag_list' to the list.
        '''
        data = []
        for tag in tag_list:
            exec(tag + " = self._collection.distinct('" + tag + "')")
            exec("data.append(" + tag + ")")
        return data

    def single_run(self):
        '''Single threading running.
        '''
        page_ranges_lst = self.GenPagesLst()
        for ind, page_range in enumerate(page_ranges_lst):
            self.CrawlHistoryOlympicsNews(page_range[0], page_range[1])

    def coroutine_run(self):
        '''Coroutines running.
        '''
        jobs = []
        page_ranges_lst = self.GenPagesLst()
        for page_range in page_ranges_lst:
            jobs.append(gevent.spawn(self.CrawlHistoryOlympicsNews, page_range[0], page_range[1]))
        gevent.joinall(jobs)

    def multi_threads_run(self, **kwarg):
        '''Multi-threading running.
        '''
        page_ranges_lst = self.GenPagesLst()
        print(' Using ' + str(self.ThreadsNum) + ' threads for collecting news ... ')
        with futures.ThreadPoolExecutor(max_workers=self.ThreadsNum) as executor:
            future_to_url = {executor.submit(self.CrawlHistoryOlympicsNews, page_range[0], page_range[1]): \
                                 ind for ind, page_range in enumerate(page_ranges_lst)}


if __name__ == '__main__':

    total_page = 334
    split_page = 10

    crawler = WebCrawlFromBJ2022CN(total_page, split_page, ThreadsNum=4, IP="localhost", PORT=27017, \
                                         dbName="olympics_news_mining_db", collectionName="news_data")
    # web_crawl_obj.coroutine_run()
    crawler.single_run()
    # web_crawl_obj.multi_threads_run()
