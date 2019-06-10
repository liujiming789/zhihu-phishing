from defs import *
fron send_email import *
import json
import time

def Save_data(User_data,Completed,Wait_q):
    with open('User_data.json','w') as F:
        F.write(json.dumps(User_data))
    with open('Completed.txt','w') as F:
        F.write(json.dumps(Completed))
    with open('Wait_q.txt','w') as F:
        F.write(json.dumps(Wait_q))
def Load_data():
    with open('User_data.json','r') as F:
        User_data = json.loads(F.read())
    with open('Completed.txt','r') as F:
        Completed = json.loads(F.read())
    with open('Wait_q.txt','r') as F:
        Wait_q = json.loads(F.read())
    return User_data,Completed,Wait_q

try:
	User_data,Completed,Wait_q = Load_data()
	print('load data')
except:
	Fir_token = 'TechMonster'
	User_data = {}
	Completed = []
	Wait_q = []
	wait_q.append(Fir_token)

while True:
	start_t = time.time()
	try:
		token = Wait_q[0]
		url = 'https://www.zhihu.com/people/'+token
		user,res = Prase_user(url,1,act_limit=1000)
		User_data[user] = res
		for u in User_data[user]['following']:
			if u['url_token'] not in Wait_q and u['url_token'] not in Completed:
				Wait_q.append(u['url_token'])
		del Wait_q[0]
		Completed.append(user)

	except Exception as e:
		print(e)
		send_email()
		pass

	end_t = time.time()
	print(len(Completed),round((end_t-start_t)/60,2))
	if(len(Completed)>10):
		break
Save_data(User_data,Completed,Wait_q)