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

        # Card Formatting
        embed = discord.Embed(title=f'Power Level: {pull[2]}', colour=discord.Colour.gold())
        embed.set_author(name=f'{pull[1]}', icon_url='https://pbs.twimg.com/media/DT3rkg0VAAAYAKR.jpg')
        embed.set_image(url=pull[3])
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.set_footer(text=f'{pull[4]}')
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
