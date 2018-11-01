import discord, identities, cogs
from discord.ext.commands import Bot

# Client Initialisation
discordInfo = identities.DiscordConfig()
PRAWConfig = identities.PRAWConfig()
bot = Bot('$')
cogs.setup(bot)

# Run Client
bot.run(discordInfo.discToken)