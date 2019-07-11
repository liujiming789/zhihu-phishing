import requests
import random
import numpy as np
import pandas as pd
from selenium import webdriver
import time 
import sys, urllib, re, json, socket, string
from bs4 import BeautifulSoup
import queue
from defs import *

headers = {"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3"}
driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

#爬取状态与保存的参数设定
source_url = 'https://www.zhihu.com/people/TechMonster'
wait_q = queue.Queue()
wait_q.put(source_url)
completed_urls = []
nums = 0
forbid_times = 0

#设置代理 通过ssr 本地1080端口
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://127.0.0.1:1080')
browser = webdriver.Chrome(executable_path=driver_path,chrome_options=chrome_options)

#主爬取程序
while not wait_q.empty():
    try:
        source_url = wait_q.get()
        '''
        #about himself
        Parse_user(source_url,browser)
        Parse_answers(source_url,browser)
        Parse_asks(source_url,browser)
        Parse_posts(source_url,browser)
        Parse_columns(source_url,browser)
        Parse_pins(source_url,browser)
        
        #about social network following
        Parse_following(source_url,browser)
        Parse_follower(source_url,browser)
        Parse_follow_topics(source_url,browser)
        Parse_follow_columns(source_url,browser)
        Parse_follow_questions(source_url,browser)
        '''
        print(nums+1)
        Parse_user(source_url,browser)
        nums += 1
        if nums>100:
            break
        follow = Parse_following(source_url,browser)
        completed_urls.append(source_url)
        
        for url in follow:
            if url not in completed_urls:
                wait_q.put(url)
        
        print('the num of users in the wait queue:',wait_q.qsize(),'/n/n')
        
    except:
        time.sleep(20)
        forbid_times += 1
        if forbid_times>20:
            break
        pass

browser.quit()