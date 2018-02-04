import mwclient
import os

zh = mwclient.Site('zh.wikipedia.org')
dp = mwclient.Site('zhdel.miraheze.org')

zh.login('','')

title = input('Page:')
dpp = dp.Pages[title]

if dpp.exists:
    text = dpp.text()
    print(text)
    edit=int(input('是否搬运？'))
    if edit:
        zhp = zh.Pages['User:Tigerzeng/zhdel/' + title]
        zhp.save(text, '查询已删除内容')
        revid = next(zhp.revisions())['revid']
        zhp.save('{{User:Tigerzeng/zhdel/header|title='+title+'|id='+str(revid)+'}}', '查询已删内容')

else:
    print('页面未收录')

os.system('pause')
