import mwclient
import time
import json
import re
from mwclient.errors import EditError
from sseclient import SSEClient as EventSource


pattern = re.compile(r'\{\{\s*((db|d|sd|csd|speedy|delete|速刪|速删|快刪|快删|有爭議|有争议|[vaictumr]fd|delrev|存廢覆核|存废复核)\s*(\||}})|(db|vfd)-)')
stime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
print(stime,'Bot started.')

zh = mwclient.Site('zh.wikipedia.org')
dp = mwclient.Site('zhdel.miraheze.org')
logdir = ''
skip=('')

dp.login('','') #Username and password
print('Login successfully!')

def fetch(title, token):
    sta = status(title)
    print('Checking',title,':',sta)
    if sta == 'skip':
        print('Skipped %s' % title)
        return None
    
    if sta == 'update' or sta == 'new':
        if count_revisions(title) > 100:
            dp.api(action='import', token=token, interwikisource='zhwikipedia', interwikipage=title)    # import the latest revision
        else:
            dp.api(action='import', token=token, interwikisource='zhwikipedia', interwikipage=title, fullhistory=1) # import all revisions

        if sta == 'new':
            with open(logdir,'a') as log:
                log.write(title+'\n')

    elif sta == 'deleted':
        pass
    elif sta == 'nobot':
        pass
    elif sta == 'well':
        pass

def status(title):
    if title in skip:
        return 'skip'
    wpp = zh.Pages[title]
    wpt = wpp.text()
    dpp = dp.Pages[title]
    dpt = dpp.text()
    loglist = list(open(logdir))
    if not wpp.exists:
        return 'deleted'
    if not title+'\n' in loglist:
        return 'new'
    if wpt != dpt:
        return 'update'
    if '!nobot!' in dpt:
        return 'nobot'
    else:
        return 'well'
        

def count_revisions(title):
    wpp = zh.Pages[title]
    sum = 0
    revs = wpp.revisions()
    for i in revs:
        sum += 1
    return sum


def main():
    event_url = 'https://stream.wikimedia.org/v2/stream/recentchange'
    for event in EventSource(event_url):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
            except ValueError:
                pass
            else:
                site = change['meta']['domain']
                if not site == 'zh.wikipedia.org':
                    continue
                title = change['title']
                if not pattern.search(zh.Pages[title].text()) == None:
                    token = dp.api(action='query', meta='tokens')['query']['tokens']['csrftoken']
                    fetch(title, token)
                
while True:
    main()
