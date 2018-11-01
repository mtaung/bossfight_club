import discord, identities, cogs
from discord.ext.commands import Bot

# Client Initialisation
discordInfo = identities.DiscordConfig()
PRAWConfig = identities.PRAWConfig()
client = discord.Client()
bot = Bot(command_prefix)
cogs.setup(bot)

# Run Client
client.run(discordInfo.discToken)