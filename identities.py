import configparser 

config = configparser.ConfigParser()
config.read('config.ini')

class DiscordConfig:

    def __init__(self, configFile=config):
        self.discId = config['discordInfo']['discId']
        self.discToken = config['discordInfo']['discToken']
        self.discPermission = config['discordInfo']['discPermission']

class PRAWConfig:

    def __init__(self, configFile=config):
        self.cid = config['PRAWInfo']['cid']
        self.sec = config['PRAWInfo']['sec']
        self.user = config['PRAWInfo']['user']
        self.pwd = config['PRAWInfo']['pwd']
        self.uage = config['PRAWInfo']['uage']