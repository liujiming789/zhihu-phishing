import requests
from bs4 import BeautifulSoup
import json
import re
import numpy as np
import time

headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}

#使用1080端口的ssr代理，变成一个变相的代理池
proxies={'https':'127.0.0.1:1080'}

def Get_user_info(url):
    user = url.split('/')[-1]
    r = requests.get('https://api.zhihu.com/people/{user}'.format(user),headers=headers,proxies=proxies)
    return r.json()

def Get_folloeing(url,test_time=False):
    user = url.split('/')[-1]
    offset = 0
    Followings = []
    
    start_t = time.time()
    while True:
        following_ = "https://www.zhihu.com/api/v4/members/{user}/followees?\
                    include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed\
                    %2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20".format(user=user,\
                                                                                                                   offset=offset)
        while True:
            try:
                r = requests.get(following_,headers=headers,proxies = proxies)
                break
            except:
                pass
        for d in r.json()['data']:
            Followings.append(d)

        if r.json()['paging']['is_end']:
            break
        offset += 20
    
    end_t = time.time()
    if test_time:
        take_t = round(end_t-start_t,2)
        print('time %.2f s:'%take_t)
        print('time %.2f min:'%(take_t/60))
    
    return Followings

def Get_Activities(url,test_time=False,visual=False):
    Activities = []    
    '''
    第二页activities ，实际上前面只有两个activities，但是重新申请一次previous时，由于limit是7，会覆盖掉这个json包，所以这个要舍弃
    重新从第一个个 next
    '''
    start_t = time.time()
    while True:
        try:
            r = requests.get(url,headers=headers,proxies = proxies)
            pattern = r'activities\?limit=7&session_id=[0-9]+&after_id=[0-9]+&desktop=True'
            first_activ = re.findall(pattern,str(r.text))[0]
            activ_url = 'https://www.zhihu.com/api/v4/members/'+url.split('/')[-1]+'/'+first_activ
            r = requests.get(activ_url,headers=headers,proxies = proxies)
            
             #获取第一页activities
            previous_act_url = ' '
            while r.json()['paging']['previous'] != previous_act_url:
                print(r.json()['paging']['previous'])
                previous_act_url = r.json()['paging']['previous']
                r = requests.get(previous_act_url,headers=headers,proxies = proxies)
                
            break
        except:
            pass

    num_act = 0
    kinds_act = []
    for j in r.json()['data']:
        num_act += 1
        if visual:
            print(num_act,j['action_text'])
        kinds_act.append(j['action_text'])
        Activities.append(j)

    while r.json()['paging']['is_end'] == 0:
        try:
            activ_next_url = r.json()['paging']['next']
            r = requests.get(activ_next_url,headers=headers,proxies = proxies)
            for j in r.json()['data']:
                num_act += 1
                if visual:
                    print(num_act,j['action_text'])
                kinds_act.append(j['action_text'])
                Activities.append(j)
                '''
                text = BeautifulSoup(j['target']['content'],'lxml')
                for p in text.find_all('p'):
                    print(p.text)
                '''
        except:
            pass

    '''
    result = {}
    for i in set(kinds_act):
        result[i] = kinds_act.count(i)
    print(result)
    '''
    end_t = time.time()
    if test_time:
        take_t = round(end_t-start_t,2)
        print('time %.2f s:'%take_t)
        print('time %.2f min:'%(take_t/60))
    return Activities