import configparser, discord, os, sys
from discord.ext.commands import Bot
from crawler.crawler import Crawler
from db.db import Database

# Module Initialization
config = configparser.ConfigParser()
config.read('config.ini')

pi = config['PRAWInfo']
crawler = Crawler(pi['cid'], pi['sec'], pi['user'], pi['pwd'], pi['uage'])
topBf = crawler.queryTop()
roster = crawler.generateBoss(topBf)

dbfile = 'bossfight.db'
if '--reset' in sys.argv:
    if os.path.exists(dbfile):
        os.remove(dbfile)
    database = Database(dbfile)
    database.initTables()
    for iid, ititle, iscore, url, topcomment in roster:
        database.registerBoss((iid, ititle, iscore, url, topcomment))
else:
    database = Database(dbfile)

# Client Initialisation
bot = Bot('$')
start_modules = ['fightclub']
for name in start_modules:
    bot.load_extension('fightclub')

# Run Client
bot.run(config['discordInfo']['discToken'])