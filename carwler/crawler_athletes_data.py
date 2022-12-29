# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 10:01:40 2022

@author: waiting
"""

import time, re, requests
from concurrent import futures
from bs4 import BeautifulSoup
from pymongo import MongoClient
import text_analysis.text_mining as tm

import gevent
from gevent import monkey, pool

# monkey.patch_all()


class CrawlerAthletesData(object):

    print("北京冬奥官网（www.beijing2022.cn）有对应的运动员JSON数据文件，地址为：https://results.beijing2022.cn/beijing-2022/paralympic-games/zh/results/all-sports/zzeej01a.json")