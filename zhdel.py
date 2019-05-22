import mwclient
from mwclient.errors import EditError
import time

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
        pass
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
    token = dp.api(action='query', meta='tokens')['query']['tokens']['csrftoken']
    for nom in zh.search(r'insource:/\{\{\s*((db|d|sd|csd|speedy|delete|速刪|速删|快刪|快删|有爭議|有争议|[vaictumr]fd|delrev|存廢覆核|存废复核)\s*(\||}})|(db|vfd)-)/'): #Reg from AF197
        fetch(nom['title'], token)

while True:
    main()
    time.sleep(60)
