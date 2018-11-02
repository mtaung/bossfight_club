import discord, asyncio
from discord.ext import commands
from db.db import Database
from crawler.crawler import Crawler

class Fightclub:
    def __init__(self):
        self.database = Database()

    async def auction(self, num):
        self.cards = self.database.randomBoss(f'{num}')
        
    @commands.command(pass_context=True)
    async def gacha(self, ctx):
        pull = self.database.randomBoss('1')
        pull = pull[0] #Query returns list, need to go a level deeper

        embed = discord.Embed(title=f'{pull[1]}', description=f'Power Level: {pull[2]}')
        imageurl = pull[3]
        embed.set_image(url=imageurl)
        
        embed.set_footer(text=f'{pull[4]}')
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
