import discord, asyncio
from discord.ext import commands
from db import Database
from crawler import Crawler

database= Database()

class Fightclub:
    async def auction(self, num):
        cards = database.randomBoss(f'{num}')
        

    @commands.command(pass_context=True)
    async def gacha(self, ctx):
        pull = database.randomBoss('1')
        pull = pull[0] #Query returns list, need to go a level deeper

        embed = discord.Embed(title=f'{pull[1]}', description=f'Power Level: {pull[2]}')
        imageurl = pull[3]
        embed.set_image(url=imageurl)
        
        embed.set_footer(text=f'{pull[4]}')
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
