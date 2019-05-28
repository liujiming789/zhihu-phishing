'''
test
检验activities次数
'''

import requests
from bs4 import BeautifulSoup
import json
import re
import numpy as np

url = 'https://www.zhihu.com/people/TechMonster'
headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}

#使用1080端口的ssr代理，变成一个变相的代理池
proxies={'https':'127.0.0.1:1080'}

'''
第二页activities ，实际上前面只有两个activities，但是重新申请一次previous时，由于limit是7，会覆盖掉这个json包，所以这个要舍弃
重新从第一个个 next
'''
r = requests.get(url,headers=headers,proxies = proxies)
pattern = r'activities\?limit=7&session_id=[0-9]+&after_id=[0-9]+&desktop=True'
first_activ = re.findall(pattern,str(r.text))[0]
activ_url = 'https://www.zhihu.com/api/v4/members/'+url.split('/')[-1]+'/'+first_activ
r = requests.get(activ_url,headers=headers,proxies = proxies)

#获取第一页activities
previous_act_url = r.json()['paging']['previous']
r = requests.get(previous_act_url,headers=headers,proxies = proxies)

num_act = 0
kinds_act = []
for j in r.json()['data']:
    num_act += 1
    #print(num_act,j['action_text'])
    kinds_act.append(j['action_text'])

while r.json()['paging']['is_end'] == 0:
    try:
        #print(activ_url)
        activ_url = r.json()['paging']['next']
        r = requests.get(activ_url,headers=headers,proxies = proxies)
        #print(r.json()['data'])
        for j in r.json()['data']:
            num_act += 1
            #print(num_act,j['action_text'])
            '''
            answer = BeautifulSoup(j['target']['content'],'lxml')
            for p in answer.find_all('p'):
                print(p.text)
            '''
            kinds_act.append(j['action_text'])
    except:
        pass