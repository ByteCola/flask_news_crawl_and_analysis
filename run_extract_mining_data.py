import text_analysis.text_mining as tm

if __name__ == '__main__':



    # 初始化挖掘类
    text_mining = tm.TextMining(IP="localhost", PORT=27017)

    # 数据挖掘与分析步骤 注意各个步骤在执行时，对应数据是否已经存放在数据库中，防止重复数据

    # 步骤一 、对数据库中的新闻文章进行分词 抽取关联运动员和运动项目 新闻数据如果较多 时间可能会长一点
    text_mining.extractSportsMetaFromArticle("olympics_news_mining_db", "news_data")

    # 步骤二、整理运动员、运动项目数据 写入数据库中
    #text_mining.statisticsSportsData('olympics_news_mining_db', 'news_data')

    # 步骤三、分析聚合热点
    text_mining.polymericSportsArticle("olympics_news_mining_db", "news_data")


