from defs import *
url = 'https://www.zhihu.com/people/TechMonster'

Activities = Get_Activities(url,1,1)
print(len(Activities))

F = Get_folloeing(url,1)
print(len(F))