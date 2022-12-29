from carwler.crawler_163_BJ2022 import WebCrawlFromNetEasy
from carwler.crawler_bj2022cn import WebCrawlFromBJ2022CN
from carwler.crawler_china_BJ2022 import WebCrawlFromChina
from carwler.crawler_newscn_BJ2022 import WebCrawlFromNewsCN
from carwler.crawler_people_BJ2022 import WebCrawlFromPeople

if __name__ == '__main__':
    # 北京冬奥官网新闻数据爬取
    bj2022cn_news_total_page = 334
    bj2022cn_news_split_page = 10

    bj2022cn_news_crawler = WebCrawlFromBJ2022CN(bj2022cn_news_total_page, bj2022cn_news_split_page, ThreadsNum=4,
                                                 IP="localhost",
                                                 PORT=27017, \
                                                 dbName="olympics_news_mining_db", collectionName="news_data")
    # bj2022cn_news_crawler.coroutine_run()
    bj2022cn_news_crawler.single_run()
    # bj2022cn_news_crawler.multi_threads_run()

    # 网易冬奥新闻数据爬取
    neteasy_news_total_page = 20
    neteasy_news_split_page = 10

    neteasy_news_crawler = WebCrawlFromNetEasy(neteasy_news_total_page, neteasy_news_split_page, ThreadsNum=4,
                                                IP="localhost",
                                                PORT=27017, \
                                                dbName="olympics_news_mining_db", collectionName="news_data")
    # neteasy_news_crawler.coroutine_run()
    neteasy_news_crawler.single_run()
    neteasy_news_crawler.multi_threads_run()

    # 人民网冬奥新闻数据爬取
    people_news_total_page = 7
    people_news_split_page = 1

    people_news_crawler = WebCrawlFromPeople(people_news_total_page, people_news_split_page, ThreadsNum=4,
                                               IP="localhost",
                                               PORT=27017, \
                                               dbName="olympics_news_mining_db", collectionName="news_data")
    # neteasy_news_crawler.coroutine_run()
    people_news_crawler.single_run()
    # neteasy_news_crawler.multi_threads_run()

    # 新华网冬奥新闻数据爬取
    newscn_news_total_page = 20
    newscn_news_split_page = 1

    newscn_news_crawler = WebCrawlFromNewsCN(newscn_news_total_page, newscn_news_split_page, ThreadsNum=4,
                                              IP="localhost",
                                              PORT=27017, \
                                              dbName="olympics_news_mining_db", collectionName="news_data")
    # neteasy_news_crawler.coroutine_run()
    newscn_news_crawler.single_run()
    # neteasy_news_crawler.multi_threads_run()

    # 中国网冬奥新闻数据爬取
    china_news_total_page = 10
    china_news_split_page = 1

    china_news_crawler = WebCrawlFromChina(china_news_total_page, china_news_split_page, ThreadsNum=4,
                                             IP="localhost",
                                             PORT=27017, \
                                             dbName="olympics_news_mining_db", collectionName="news_data")
    # neteasy_news_crawler.coroutine_run()
    china_news_crawler.single_run()
    # neteasy_news_crawler.multi_threads_run()