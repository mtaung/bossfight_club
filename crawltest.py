import configparser, pickle
from crawler.crawler import Crawler
from db.db import Database

config = configparser.ConfigParser()
config.read('config.ini')

pi = config['PRAWInfo']
crawler = Crawler(pi['cid'], pi['sec'], pi['user'], pi['pwd'], pi['uage'])
topPS = crawler.queryPS(100000, 500)
topReddit = list(crawler.queryTop())

picklePS = open('PS.pickle', 'wb')
pickle.dump(topPS, picklePS)
pickleReddit = open('Reddit.pickle', 'wb')
pickle.dump(topReddit, pickleReddit)


finalPS = crawler.generateBoss(topPS)
finalReddit = crawler.generateBoss(topReddit)

dibble = Database()
dibble.initTables()

dupe_id = []
count = 0
for iid, ititle, iscore, iurl, topcomment in finalPS:
    dupe_id.append(iid)
    if dupe_id.count(iid) > 1:
        print(f'{iid} is a duplicate with count: {dupe_id.count(iid)}')
        continue
    else:
        dibble.registerBoss((iid, ititle, iscore, iurl, topcomment, 0))
        print(count+=1)

for iid, ititle, iscore, iurl, topcomment in finalReddit:
    dupe_id.append(iid)
    if dupe_id.count(iid) > 1:
        print(f'{iid} is a duplicate with count: {dupe_id.count(iid)}')
        continue
    else:
        dibble.registerBoss((iid, ititle, iscore, iurl, topcomment, 0))
        print(count+=1)

dibble.commit()

"""with open('roster.ini', 'w') as f:
    for iid, ititle, iscore, url, topcomment in roster:
        f.write(url+'\n')
        f.flush()"""