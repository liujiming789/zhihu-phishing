import requests
from bs4 import BeautifulSoup
import json
import re
import numpy as np
import time

headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}

#使用1080端口的ssr代理，变成一个变相的代理池
proxies={'https':'127.0.0.1:1080'}

def Get_r(url):
    while True:
        try :
            r = requests.get(url,headers=headers,proxies=proxies)
            if r.status_code == 200:
                return r
        except:
            pass

def Get_user_info(url,visual=False):
    user = url.split('/')[-1]
    r = Get_r('https://api.zhihu.com/people/{user}'.format(user=user))
    return r.json()

def Get_following(url,test_time=False):
    user = url.split('/')[-1]
    offset = 0
    Followings = []
    
    start_t = time.time()
    while True:
        following_ = "https://www.zhihu.com/api/v4/members/{user}/followees?\
                    include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed\
                    %2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20".format(user=user,\
                                                                                                                   offset=offset)
        r = Get_r(following_)
        for d in r.json()['data']:
            Followings.append(d)

        if r.json()['paging']['is_end']:
            break
        offset += 20
    
    end_t = time.time()
    if test_time:
        print('prase following')
        take_t = round(end_t-start_t,2)
        print('time %.2f s:'%take_t)
        print('time %.2f min:'%(take_t/60))
    
    return Followings

def Get_Activities(url,test_time=False,visual=False,limit=10**6):
    Activities = []    
    '''
    第二页activities ，实际上前面只有两个activities，但是重新申请一次previous时，由于limit是7，会覆盖掉这个json包，所以这个要舍弃
    重新从第一个个 next
    '''
    start_t = time.time()
    
    r = Get_r(url)
    pattern = r'activities\?limit=7&session_id=[0-9]+&after_id=[0-9]+&desktop=True'
    first_activ = re.findall(pattern,str(r.text))[0]
    activ_url = 'https://www.zhihu.com/api/v4/members/'+url.split('/')[-1]+'/'+first_activ
    r = Get_r(activ_url)
    
     #获取第一页activities
    previous_act_url = ' '
    while r.json()['paging']['previous'] != previous_act_url:
        if visual:
            print(r.json()['paging']['previous'])
        previous_act_url = r.json()['paging']['previous']
        r = Get_r(previous_act_url)

    num_act = 0
    for j in r.json()['data']:
        num_act += 1
        if visual:
            print(num_act,j['action_text'])
        Activities.append(j)
    # next 获取activities
    while True:
        try:
            activ_next_url = r.json()['paging']['next']
            r_ = Get_r(activ_next_url)

            if visual:
                print(activ_next_url)
                print(len(r_.json()['data']))
            for j in r_.json()['data']:
                num_act += 1
                Activities.append(j)

                if visual:
                    print(num_act,j['action_text'])
            
            if len(Activities) > limit or r_.json()['paging']['is_end'] == 1:
                break
            r = r_
        except:
            pass
    end_t = time.time()
    if test_time:
        print('prase activitties')
        take_t = round(end_t-start_t,2)
        print('time %.2f s:'%take_t)
        print('time %.2f min:'%(take_t/60))
    return Activities

def Prase_user(url,test_time=False,visual=False,act_limit=10**6):
    res = {}
    user = url.split('/')[-1]
    F = Get_following(url,test_time=test_time)
    Activities = Get_Activities(url,test_time=test_time,visual=visual,limit=act_limit)
    info = Get_user_info(url)
    res['following'] = F
    res['activities'] = Activities
    res['info'] = info
    return user,res

def Get_act_text(act):
    text = BeautifulSoup(act['target']['content'],'lxml')
    for p in text.find_all('p'):
        print(p.text)