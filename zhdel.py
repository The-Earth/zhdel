import json
import re
import time

import mwclient
import requests
from mwclient.errors import InvalidPageTitle
from requests_sse import EventSource, InvalidStatusCodeError, InvalidContentTypeError

import catbot

pattern = re.compile(
    r'{{\s*((db|d|sd|csd|speedy|delete|速刪|速删|快刪|快删|有爭議|有争议|[vaictumr]fd|delrev|存廢覆核|存废复核)\s*(\||}})|(db|vfd)-)')
stime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print(stime, 'Bot started.')
config = json.load(open('config.json', 'r', encoding='utf-8'))

zh = mwclient.Site('zh.wikipedia.org')
dp = mwclient.Site('zhdel.miraheze.org', clients_useragent='User:Tiger-bot operated by User:Tiger')
logdir = config['log']
skip = config['skip']
tgbot = catbot.Bot(config)

dp.login(config['zhdel_username'], config['zhdel_password'])
print('Login successfully!')


def fetch(title, token):
    sta = status(title)
    print('Checking', title, ':', sta)
    if sta == 'skip':
        print('Skipped %s' % title)
        return None

    if sta == 'update' or sta == 'new':
        if full_history_deter(title):
            dp.api(action='import', summary=sta, token=token, interwikisource='zhwikipedia',
                   interwikipage=title, fullhistory=1)  # import all revisions
        else:
            dp.api(action='import', summary=sta, token=token, interwikisource='zhwikipedia',
                   interwikipage=title)  # import the latest revisions

        if sta == 'new':
            with open(logdir, 'a') as log:
                log.write(title + '\n')
            tgbot.send_message(config['tg_chat_id'], text=config['tg_push_text'].format(title=title), parse_mode='HTML',
                               disable_web_page_preview=True)

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
    if not title + '\n' in loglist:
        return 'new'
    if wpt != dpt:
        return 'update'
    if '!nobot!' in dpt:
        return 'nobot'
    else:
        return 'well'


def full_history_deter(title):
    wpp = zh.Pages[title]
    sum_ = 0
    revs = wpp.revisions()
    for _ in revs:
        sum_ += 1
    copyvio = re.search(r'{{(\s*[Cc]opyvio|侵权|[Cc]!)\s*(\||}})', wpp.text())
    return sum_ < 100 and not copyvio


def main():
    event_url = 'https://stream.wikimedia.org/v2/stream/recentchange'
    ssekw = {'proxies': {'https': config['proxy']['proxy_url']}} if config['proxy']['enable'] else {}

    with EventSource(event_url, **ssekw) as source:
        try:
            for event in source:
                if event.type == 'message':
                    try:
                        change = json.loads(event.data.encode('utf-8').decode('utf-8'))
                    except ValueError:
                        continue
                    site = change['meta']['domain']
                    if site != 'zh.wikipedia.org' or change['type'] != 'edit':
                        continue
                    title = change['title']
                    try:
                        wpp = zh.Pages[title]
                    except InvalidPageTitle:
                        print(f'InvalidPageTitle: {title}')
                        continue
                    if wpp.namespace == 0 and not pattern.search(wpp.text()) is None:
                        token = dp.api(action='query', meta='tokens')['query']['tokens']['csrftoken']
                        fetch(title, token)
                time.sleep(0.1)
        except InvalidStatusCodeError:
            pass
        except InvalidContentTypeError:
            pass
        except requests.RequestException:
            pass
        except StopIteration:
            pass


if __name__ == '__main__':
    while True:
        main()
