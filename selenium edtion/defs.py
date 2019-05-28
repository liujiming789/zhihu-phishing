import requests
import numpy as np
import pandas as pd
from selenium import webdriver
import time 
import sys, urllib, re, json, socket, string
from bs4 import BeautifulSoup

headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}
driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

#用户简介
def Prase_user(source_url,browser):
    browser.get(source_url)
    browser.find_element_by_xpath('//button[@class="Button ProfileHeader-expandButton Button--plain"]').click()
    html = browser.page_source
    time.sleep(2)
    
    soup = BeautifulSoup(html,'lxml')
    s = soup.find_all('h1',attrs={'class':'ProfileHeader-title'})[0]
    print(s.find_all('span',attrs={'class':'ProfileHeader-name'})[0].text ,\
            s.find_all('span',attrs={'class':'ztext ProfileHeader-headline'})[0].text)
    
    s = soup.find_all('div',attrs={'class':'ProfileHeader-detailItem'})
    for i in s:
        print(i.find_all(attrs={'ProfileHeader-detailLabel'})[0].text, \
              i.find_all(attrs={'ProfileHeader-detailValue'})[0].text)
        
    s = soup.find_all('ul',attrs={'class':'Tabs ProfileMain-tabs'})[0]
    for i in s.find_all('li')[1:-1]:
        print(i.find_all(attrs={'class':'Tabs-link'})[0].text[:2],
             i.find_all(attrs={'class':'Tabs-link'})[0].text[2:])
        

#anawers 所有回答
def Get_Answer(answer_url,browser):
    browser.get(answer_url)
    html = browser.page_source
    time.sleep(2)

    soup = BeautifulSoup(html,'lxml')
    s = soup.find_all('span',attrs={'class':'RichText ztext CopyrightRichText-richText'})
    for p in s[0].find_all('p'):
        print(p.text)

def Prase_answers(source_url,browser):        
    answer_url = source_url+'/answers'
    r = requests.get(answer_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except :
        pages = 1
        pass
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('answers pages',p)
        browser.get(answer_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        #url_text = soup.find_all('a',attrs={'class':'UserLink-link'})
        patten = 'www.zhihu.com/question/[0-9]+/answer/[0-9]+'
        urls = re.findall(patten,str(soup))
        for u in urls:
            u = 'https://'+u
            print(u)
            Get_Answer(u,browser)
    #browser.quit()


#asks 提问
def Prase_asks(source_url,browser):
    asks_url = source_url+'/asks'
    r = requests.get(asks_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('asks pages',p)
        browser.get(asks_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('div',attrs={'class':'QuestionItem-title'})
        for t in titles:
            patten = r'/question/[0-9]+'
            s = re.findall(patten,str(t))[0]
            print('https://www.zhihu.com'+s)
            print(t.text)
    #browser.quit()


#posts 文章
def Prase_posts(source_url,browser):
    posts_url = source_url+'/posts'
    r = requests.get(posts_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('posts pages',p)
        browser.get(posts_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('h2',attrs={'class':'ContentItem-title'})
        for t in titles:
            patten = r'//zhuanlan.zhihu.com/p/[0-9]+'
            s = re.findall(patten,str(t))[0]
            print('https:'+s)
            print(t.text)
    #browser.quit()
    

#columns 专栏
def Prase_columns(source_url,browser):
    columns_url = source_url+'/columns'
    r = requests.get(columns_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('columns pages',p)
        browser.get(columns_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('div',attrs={'class':'ContentItem-head'})
        for t in titles:
            t = t.find_all('a',attrs={'class':'ColumnLink'})[0]
            patten = r'//zhuanlan.zhihu.com/[a-zA-Z0-9,-]+'
            s = re.findall(patten,str(t))[0]
            print('https:'+s)
            print(t.text)
    #browser.quit()

# pins 想法
def Prase_pins(source_url,browser):
    pins_url = source_url + '/pins'
    r = requests.get(pins_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
        
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('pins pages',p)
        browser.get(pins_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('div',attrs={'class':'RichContent'})
        for t in titles:
            patten = r'www.zhihu.com/pin/[a-zA-Z0-9,-]+'
            s = re.findall(patten,str(t))[0]
            print('https://'+s)
            temps = t.find_all('blockquote',attrs={'class':'PinItem-3lineBlockquote'})
            for temp in temps:
                print(temp.text,'\n')
    #browser.quit()# -*- coding: utf-8 -*-

    
#following 他关注的人
def Prase_following(source_url,browser):
    following_url = source_url+'/following'
    r = requests.get(following_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    follow = []
    
    try:
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except :
        pages = 1
        pass
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        #print('following pages',p)
        browser.get(following_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        url_text = soup.find_all('a',attrs={'class':'UserLink-link'})
        patten = 'www.zhihu.com/people/[a-zA-Z0-9,-]+'
        urls = re.findall(patten,str(url_text))
        for i in range(int(len(urls)/2)):
            s = 'https://'+urls[2*i]
            follow.append(s)
            #print(s)
    return follow
    #browser.quit()


#follower 关注他的人
def Prase_follower(source_url,browser):
    follower_url = source_url+'/followers'
    r = requests.get(follower_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('follower pages',p)
        browser.get(follower_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        url_text = soup.find_all('a',attrs={'class':'UserLink-link'})
        patten = 'www.zhihu.com/people/[a-zA-Z0-9,-]+'
        urls = re.findall(patten,str(url_text))
        for i in range(int(len(urls)/2)):
            print('https://'+urls[2*i])
    #browser.quit()


#fellow topics 话题
def Prase_follow_topics(source_url,browser):
    topics_url = source_url+'/following/topics'
    r = requests.get(topics_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('questions pages',p)
        browser.get(topics_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('h2',attrs={'class':'ContentItem-title'})
        for t in titles:
            patten = r'www.zhihu.com/topic/[0-9]+'
            s = re.findall(patten,str(t))[0]
            print('https://'+s)
            print(t.text,'\n')
    #browser.quit()


#fellow columns 专栏
def Prase_follow_columns(source_url,browser):
    columns_url = source_url+'/following/columns'
    r = requests.get(columns_url,headers=headers)
    soup = BeautifulSoup(r.text,'lxml')
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('zhuanlan pages',p)
        browser.get(columns_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('h2',attrs={'class':'ContentItem-title'})
        for t in titles:
            patten = r'zhuanlan.zhihu.com/[a-zA-Z0-9,-]+'
            s = re.findall(patten,str(t))[0]
            print('https://'+s)
            print(t.text,'\n')
    #browser.quit()# -*- coding: utf-8 -*-

#fellow questions
def Prase_follow_questions(source_url,browser):
    questions_url = source_url+'/following/questions'
    r = requests.get(questions_url,headers=headers)
    print(r)
    soup = BeautifulSoup(r.text,'lxml')
    try :
        pages = int(soup.find_all('button',attrs={'class':'Button PaginationButton Button--plain'})[-1].text)
    except:
        pages = 1
    
    #browser = webdriver.Chrome(executable_path=driver_path)
    for p in range(1,pages+1):
        print('questions pages',p)
        browser.get(questions_url+'?page='+str(p))
        time.sleep(5)
        soup = BeautifulSoup(browser.page_source,'lxml')
        titles = soup.find_all('div',attrs={'class':'QuestionItem-title'})
        for t in titles:
            patten = r'/question/[0-9]'
            s = re.findall(patten,str(t))[0]
            print('https://www.zhihu.com'+s)
            print(t.text,'\n')
    #browser.quit()# -*- coding: utf-8 -*-
    
    
        

if __name__ == '__main__' :
    source_url = 'https://www.zhihu.com/people/TechMonster' 
    browser = webdriver.Chrome(executable_path=driver_path)
    try:
        '''
        #about himself
        Prase_user(source_url,browser)
        Prase_answers(source_url,browser)
        Prase_asks(source_url,browser)
        Prase_posts(source_url,browser)
        Prase_columns(source_url,browser)
        Prase_pins(source_url,browser)
        
        #about social network following
        Prase_following(source_url,browser)
        Prase_follower(source_url,browser)
        Prase_follow_topics(source_url,browser)
        Prase_follow_columns(source_url,browser)
        Prase_follow_questions(source_url,browser)
        '''
        Prase_columns(source_url,browser)
        
    except:
        pass
    browser.quit()

