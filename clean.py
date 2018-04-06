import mwclient
from mwclient.errors import APIError
import time

zh = mwclient.Site('zh.wikipedia.org')
dp = mwclient.Site('zhdel.miraheze.org')
logdir = ''

dp.login('','') #Bot user name & password
print('Login successfully!')

def status(title):
	wpp = zh.Pages[title]
	wpt = wpp.text()
	dpp = dp.Pages[title]
	dpt = dpp.text()
	examt = wpt.lower()
	if not wpp.exists:
		return 'deleted'
	elif '!nobot!' in dpt:
		return 'nobot'
	elif wpp.exists and not ((r'{{d|' in examt) or (r'{{delete|' in examt) or (r'{{vfd|' in examt) or (r'{{afd|' in examt)):
		return 'kept'
	else:
		return 'well'

def deletePage(title):
	dpp = dp.Pages[title]
	dpp.delete('Page kept on zhwp.')
	logdelete(title)
	print(title,'kept on zhwp and deleted on zhdel.')

def clean():
	titlist = list(open(logdir))

	for i in range(len(titlist)):
		title = titlist[i].rstrip()
		sta = status(title)
		if sta == 'nobot':
			continue
		
		elif  sta == 'deleted':
			logdelete(title)
			print(title,'deleted on zhwp.')
		
		elif sta == 'kept':
			try:
				deletePage(title)
			except APIError as e:
				if e.code =='badtoken':
					print('Got bad token, retrying')
					dp.tokens = {}   # clear token cache
					deletePage(title)	#Retry
		
		elif sta == 'well':
			print(title,': well')

def logdelete(title):
	with open(logdir,'r') as log:
		logtext = log.read()
	logtext = logtext.replace(title+'\n','')
	with open(logdir,'w') as log:
		log.write(logtext)

def kill():
	talk = dp.Pages['']     #Bot control page
	talktxt = talk.text()
	if '!stop!' in  talktxt:
		return True
	else:
		return False

while True:
	if kill():
		break
	else:
		clean()
		print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),'Sleeping: 3 hours...',end='\n\n')
		time.sleep(10800)
