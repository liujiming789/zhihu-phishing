import requests
from bs4 import BeautifulSoup
import json
import re

url = 'https://www.zhihu.com/people/TechMonster'
headers = {"user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36"}
proxies={'https':'127.0.0.1:1080'}
r = requests.get(url,headers=headers)
pattern = r'activities\?limit=7&session_id=[0-9]+&after_id=[0-9]+&desktop=True'
first_activ = re.findall(pattern,str(r.text))[0]
activ_url = 'https://www.zhihu.com/api/v4/members/'+url.split('/')[-1]+'/'+first_activ

r = requests.get(activ_url,headers=headers,proxies = proxies)
print(r.json()['data'])
while r.json()['paging']['is_end'] == 0:
    print(activ_url)
    activ_url = r.json()['paging']['next']
    r = requests.get(activ_url,headers=headers)
    print(r.json()['data'])