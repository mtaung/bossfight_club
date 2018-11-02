import configparser, discord, cogs
from discord.ext.commands import Bot
from crawler.crawler import Crawler

# Module Initialization
config = configparser.ConfigParser()
config.read('config.ini')

pi = config['PRAWInfo']
crawler = Crawler(pi['cid'], pi['sec'], pi['user'], pi['pwd'], pi['uage']) #wot we do with this

# Client Initialisation
bot = Bot('$')
start_modules = ['fightclub']
for name in start_modules:
    bot.load_extension('fightclub')

# Run Client
bot.run(config['discordInfo']['discToken'])