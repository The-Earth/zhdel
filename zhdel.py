import mwclient
from mwclient.errors import EditError
import time

stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
print(stime,'Bot started.')

zh = mwclient.Site('zh.wikipedia.org')
dp = mwclient.Site('zhdel.miraheze.org')
logdir = ''

dp.login('','') #Bot user name & password
print('Login successfully!')

def fetch(title,typ):
	sta = status(title,typ)
	print('Checking',title,':',sta)
	if sta == 'update' or sta == 'new':
		page = zh.Pages[title]
		txt = page.text()
		new = dp.Pages[title]
		if sta == 'update':
			try:
				new.save(txt,'Bot: Page updated.')
			except EditError:
				revoke()	#revoke auto-confirmed
				new.save(txt,'Bot: Page updated.')	#retry
		elif sta == 'new':
			try:
				new.save(txt,'Bot: New page collected.')
				with open(logdir,'a') as log:
					log.write(title+'\n')
			except EditError:
				revoke()	#revoke auto-confirmed
				new.save(txt,'Bot: New page collected.')	#retry
				with open(logdir,'a') as log:
					log.write(title+'\n')

	elif sta == 'deleted':
		pass
	elif sta == 'nobot':
		pass
	elif sta == 'well':
		pass

def revoke():
	print('Autoconfirmed, revoke it.')
	talk = dp.Pages['User talk:Tiger-bot']
	try:
		talk.save('!revoke!')
	except EditError:
		pass

def status(title,typ=''):
	wpp = zh.Pages[title]
	wpt = wpp.text()
	dpp = dp.Pages[title]
	dpt = dpp.text()
	loglist = list(open(logdir))
	if not title+'\n' in loglist:
		return 'new'
	if not wpp.exists:
		return 'deleted'
	if wpt != dpt:
		return 'update'
	if '!nobot!' in dpt:
		return 'nobot'
	else:
		return 'well'

def d():
	for nom in zh.search(r'insource:/\{\{(D|d)\|/'):
		fetch(nom['title'],'{{d|')

def delt():
	for nom in zh.search(r'insource:/\{\{(D|d)elete\|/'):
		fetch(nom['title'],'{{delete|')

def afd():
	for nom in zh.search(r'insource:/\{\{(A|a)fd\|/'):
		fetch(nom['title'],'{{afd|')

def vfd():
	for nom in zh.search(r'insource:/\{\{(V|v)fd\|/'):
		fetch(nom['title'],'{{vfd|')

def main():
	d()
	afd()
	vfd()
	delt()

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
		main()
		time.sleep(60)