import os

with open('zhdel.py', 'r') as main:
    maintext = main.read()
with open('clean.py', 'r') as clean:
    cleantext = clean.read()
with open('query.py', 'r', encoding="utf-8") as query:
    qtext = query.read()

print('Welcome!')
usr = input('zhdel Bot user name:')
pwd = input('zhdel Bot password:')
logdir = input('Log directory[Full directory recommended]: ')
ctr = input('Bot control page[Example: User talk:bot]: ')
qusr = input('ZHWP user[For query on ZHWP]: ')
qpwd = input('ZHWP password[For query on ZHWP]: ')

maintext = maintext.replace("dp.login('','')","dp.login('"+usr+"','"+pwd+"')")
cleantext = cleantext.replace("dp.login('','')","dp.login('"+usr+"','"+pwd+"')")
maintext = maintext.replace("logdir = ''", "logdir = '"+logdir+"'")
cleantext = cleantext.replace("logdir = ''", "logdir = '"+logdir+"'")
maintext = maintext.replace("dp.Pages['']", "dp.Pages["+ctr+"]")
cleantext = cleantext.replace("dp.Pages['']", "dp.Pages["+ctr+"]")
qtext = qtext.replace("zh.login('','')", "zh.login('"+qusr+"','"+qpwd+"')")
with open(logdir, 'w'):
    pass

with open('zhdel.py', 'w') as main:
    main.write(maintext)
with open('clean.py', 'w') as main:
    main.write(maintext)
with open('zhdel.py', 'w') as main:
    main.write(maintext)

print('Job done. You can run the scripts now.\n')
print('################ CAUTION ##################')
print('Never upload this file to any public area!')
print('Doing so will lead to leaking of your account and password.')

os.system('pause')
