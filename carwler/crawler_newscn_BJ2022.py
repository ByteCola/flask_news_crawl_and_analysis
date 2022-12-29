# -*- coding: utf-8 -*-
import json
import time, re, requests
from concurrent import futures
from bs4 import BeautifulSoup
from pymongo import MongoClient
import text_analysis.text_mining as tm

import gevent
from gevent import monkey, pool


# monkey.patch_all()


class WebCrawlFromNewsCN(object):
    '''从新华网获取冬奥新闻数据 'http://www.news.cn/beijing2022/erji.htm?page=dadt' 抓取新闻数据.列表采用API_JSON方式，不用解析HTML

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

    def getUrlInfo(self, url):
        '''Analyze website and extract useful information.
               '''

        article = ''
        try:
            print(url)
            respond = requests.get(url, timeout=10)
            respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding
        except Exception:
            print("请求异常：" + url)
            return article

        bs = BeautifulSoup(respond.text, "lxml")

        _content = bs.find('div', attrs={'id': 'detail'})
        if not _content:
            return article
        part = _content.find_all('p')

        for paragraph in part:
            chnstatus = self.countchn(str(paragraph))
            possible = chnstatus[1]
            '''Porb: Standard frequency of Chinese occurrence among 
               each parts of one news(article/document), used
               to judge whether any part is main body or not.
            '''
            if possible > self.Porb:
                article += str(paragraph)

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
        return  article

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
            url_Part_1 = 'http://da.wa.news.cn/nodeart/page?nid=11246487&cnt=50&attr=&tp=1&orderby=1&callback=jQuery1124038008295607298237_1649503062594&_=1649503062596&pgnum='
            for pageId in range(startPage, endPage + 1):
                urls.append(url_Part_1 + str(pageId))

            for url in urls:
                print(url)
                self.craw_and_storage(url)
        else:
            urls = []
            url_Part_1 = 'http://da.wa.news.cn/nodeart/page?nid=11246487&cnt=50&attr=&tp=1&orderby=1&callback=jQuery1124038008295607298237_1649503062594&_=1649503062596&pgnum='
            for pageId in range(startPage, endPage + 1):
                urls.append(url_Part_1 + str(pageId))

            for url in urls:
                print(' <Re-Crawl url> ', url)
                self.craw_and_storage(url)

    def craw_and_storage(self,url):

        resp = requests.get(url)
        resp_text = resp.text
        resp_text_json = resp_text[resp_text.index('(') + 1:(len(resp_text) - 2)]

        resp_json = json.loads(resp_text_json)
        if resp_json['status'] == 0:
            news_list = resp_json['data']['list']
            for a in news_list:
                article = self.getUrlInfo(a['LinkUrl'])
                if article != '':
                    data = {
                        'title': a['Title'],
                        'date': a['PubTime'],
                        'address': a['LinkUrl'],
                        'keywords': a['keyword'],
                        'summary': a['Abstract'],
                        'article': article,
                        'site': 'newscn',
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
    total_page = 20
    split_page = 5

    crawler = WebCrawlFromNewsCN(total_page, split_page, ThreadsNum=4, IP="localhost", PORT=27017, \
                                   dbName="olympics_news_mining_db", collectionName="news_data")
    # web_crawl_obj.coroutine_run()
    crawler.single_run()
    # web_crawl_obj.multi_threads_run()
