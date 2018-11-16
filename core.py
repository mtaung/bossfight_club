import configparser, discord, os, sys
from discord.ext.commands import Bot
from crawler.crawler import Crawler
from db.util import DatabaseInterface

# Module Initialization
config = configparser.ConfigParser()
config.read('config.ini')

db = DatabaseInterface('sqlite:///fightclub.db')

# Client Initialisation
bot = Bot('€')
bot.database = db
start_modules = ['fightclub']
for name in start_modules:
    bot.load_extension('fightclub')

# Run Client
bot.run(config['discordInfo']['discToken'])