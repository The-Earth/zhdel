import mwclient
from mwclient.errors import APIError
import time
import re

zh = mwclient.Site('zh.wikipedia.org')
dp = mwclient.Site('zhdel.miraheze.org')
logdir = ''
deltemp = re.compile(r'{{\s*((db|d|sd|csd|speedy|delete|速刪|速删|快刪|快删|有爭議|有争议|[vaictumr]fd|delrev|存廢覆核|存废复核|copyvio|侵权|侵權|now ?commons|ncd)\s*(\||}})|(db|vfd)-)') #Reg from AF197
skip=('')

dp.login('','') #Username and password
print('Login successfully!')

def status(title):
    if title in skip:
        return 'skip'
    wpp = zh.Pages[title]
    wpt = wpp.text().lower()
    dpp = dp.Pages[title]
    dpt = dpp.text()
    if not wpp.exists:
        return 'deleted'
    elif '!nobot!' in dpt:
        return 'nobot'
    elif wpp.exists and deltemp.search(wpt) == None:
        return 'kept'
    else:
        return 'well'

def deletePage(title):
    dp.Pages[title].delete('Page kept on zhwp.')
    dp.Pages['Talk:'+title].delete('Page kept on zhwp.')
    logdelete(title)
    print(title,'kept on zhwp and deleted on zhdel.')

def clean():
    titlist = list(open(logdir))

    for i in range(len(titlist)):
        title = titlist[i].rstrip()
        sta = status(title)
        if sta == 'skip':
            print('Skipped %s' % title)
            continue
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
                    deletePage(title)    #Retry
        
        elif sta == 'well':
            print(title,': well')

def logdelete(title):
    with open(logdir,'r') as log:
        logtext = log.read()
    logtext = logtext.replace(title+'\n','')
    with open(logdir,'w') as log:
        log.write(logtext)

def kill():
    talk = dp.Pages[''] #Bot control page
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
