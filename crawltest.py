import configparser
from crawler.crawler import Crawler

config = configparser.ConfigParser()
config.read('config.ini')

pi = config['PRAWInfo']
crawler = Crawler(pi['cid'], pi['sec'], pi['user'], pi['pwd'], pi['uage'])
topBf = crawler.spawnTop()
roster = crawler.generateBoss(topBf)

with open('roster.ini', 'w') as f:
    for iid, ititle, iscore, url, topcomment in roster:
        f.write(url+'\n')
        f.flush()