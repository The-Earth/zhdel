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

def fetch(title):
    sta = status(title)
    print('Checking',title,':',sta)
    if sta == 'skip':
        print('Skipped %s' % title)
        pass
    if sta == 'update' or sta == 'new':
        page = zh.Pages[title]
        rev = next(page.revisions())
        by = '由[[w:zh:User:%s|%s]]于%s年%s月%s日 %s:%s:%s(UTC)做出的[[w:zh:Special:permalink/%s|版本%s]]，编辑摘要：%s' % (rev['user'],rev['user'],rev['timestamp'].tm_year,rev['timestamp'].tm_mon,rev['timestamp'].tm_mday,rev['timestamp'].tm_hour,rev['timestamp'].tm_min,rev['timestamp'].tm_sec,rev['revid'],rev['revid'],rev['comment'])
        new = dp.Pages[title]
        talk = dp.Pages['Talk:'+title]
        txt = page.text()
        if sta == 'update':
            try:
                new.save(txt,'Bot: Page updated.')
                talk.save(by,'Attribution information')
            except EditError:
                revoke()    #revoke auto-confirmed
                new.save(txt,'Bot: Page updated.')    #retry
                talk.save(by,'Attribution information')
        elif sta == 'new':
            try:
                new.save(txt,'Bot: New page collected.')
                talk.save(by,'Attribution information')
                with open(logdir,'a') as log:
                    log.write(title+'\n')
            except EditError:
                revoke()    #revoke auto-confirmed
                new.save(txt,'Bot: New page collected.')    #retry
                talk.save(by,'Attribution information')
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

def status(title):
    if title in skip:
        return 'skip'
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

def main():
    for nom in zh.search(r'insource:/\{\{\s*((db|d|sd|csd|speedy|delete|速刪|速删|快刪|快删|有爭議|有争议|[vaictumr]fd|delrev|存廢覆核|存废复核)\s*(\||}})|(db|vfd)-)/'): #Reg from AF197
        fetch(nom['title'])

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
        main()
        time.sleep(60)
