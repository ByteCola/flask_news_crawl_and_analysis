# -*- coding: utf-8 -*-
import datetime
import time, re, requests
from concurrent import futures
from bs4 import BeautifulSoup
from pymongo import MongoClient
from requests import ReadTimeout
from urllib3.exceptions import InvalidChunkLength, ReadTimeoutError

import text_analysis.text_mining as tm

import gevent
from gevent import monkey, pool


# monkey.patch_all()


class WebCrawlFromChina(object):
    '''从中国网冬奥会新闻列表页 'http://about.china.com.cn/node_8027858.htm' 抓取新闻数据.

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
        title = ''
        article = ''
        date = ''
        summary = ''
        keyWords = ''
        try:
            print(url)
            respond = requests.get(url, timeout=10)
            respond.encoding = BeautifulSoup(respond.content, "lxml").original_encoding

        except Exception:
            print("请求异常：" + url)
            return title,summary, keyWords, date, article

        bs = BeautifulSoup(respond.text, "lxml")
        # 新闻meta
        meta_list = bs.find_all('meta')
        # 新闻内容
        _content = bs.find('div', attrs={'class': 'center_box'})
        # print(_content)
        if not _content:
            print("不是普通新闻格式，不用采集：" + url)
            return title,summary, keyWords, date, article
        # 文章标题
        title = _content.find('h1').text
        # 文章发布日期
        _date_str = _content.find('b')
        _date_start_index = _date_str.text.index('发布时间：') + 5
        _date_end_index = _date_start_index + 19
        date = _date_str.text[_date_start_index:_date_end_index]
        # 文章内容
        part = _content.find_all('p')

        for meta in meta_list:
            if 'name' in meta.attrs and meta['name'] == 'description':
                summary = meta['content']
            elif 'name' in meta.attrs and meta['name'] == 'keywords':
                keyWords = meta['content']
            if summary != '' and keyWords != '':
                break

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

        return title, summary, keyWords, date, article

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
        urls = []
        url_Part_1 = 'http://about.china.com.cn/node_8027858_'
        url_Part_2 = '.htm'
        urls.append("http://about.china.com.cn/node_8027858.htm")
        for pageId in range(startPage, endPage + 1):
            if pageId > 1:
                urls.append(url_Part_1 + str(pageId) + url_Part_2)
        if AddressLst == []:
            for url in urls:
                print(url)
                self.craw_and_storage(url)
        else:
            for url in urls:
                print(' <Re-Crawl url> ', url)
                self.craw_and_storage(url)

    def craw_and_storage(self, url):
        resp = requests.get(url)
        resp.encoding = BeautifulSoup(resp.content, "lxml").original_encoding
        bs = BeautifulSoup(resp.text, "lxml")
        news_div = bs.find("div", attrs={"class": "new_com"})
        news_ul = news_div.find('ul')
        a_list = news_ul.find_all("a")
        for a in a_list:
            if 'href' in a.attrs and a.string:
                title, summary, keyWords, date, article = self.getUrlInfo(a['href'])
                if article != '':
                    data = {'date': date,
                            'address': a['href'],
                            'title': title,
                            'keywords': keyWords,
                            'summary': summary,
                            'article': article,
                            'site': 'china',
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
    # 查看网站新闻页数量
    total_page = 10
    split_page = 1

    crawler = WebCrawlFromChina(total_page, split_page, ThreadsNum=4, IP="localhost", PORT=27017, \
                                 dbName="olympics_news_mining_db", collectionName="news_data")
    # crawler.coroutine_run()
    crawler.single_run()
    # crawler.multi_threads_run()
