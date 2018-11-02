import configparser, discord
from discord.ext.commands import Bot
from crawler.crawler import Crawler
from db.db import Database

# Module Initialization
config = configparser.ConfigParser()
config.read('config.ini')

pi = config['PRAWInfo']
crawler = Crawler(pi['cid'], pi['sec'], pi['user'], pi['pwd'], pi['uage'])
topBf = crawler.spawnTop()
roster = crawler.generateBoss(topBf)

database = Database()
database.initTables()

for iid, ititle, iscore, url, topcomment in roster:
    database.registerBoss((iid, ititle, iscore, url, topcomment))

# Client Initialisation
bot = Bot('$')
start_modules = ['fightclub']
for name in start_modules:
    bot.load_extension('fightclub')

# Run Client
bot.run(config['discordInfo']['discToken'])