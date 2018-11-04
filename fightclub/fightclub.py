import discord, asyncio
from discord.ext import commands
from db.db import Database
from db.util import DatabaseInterface
from crawler.crawler import Crawler

class Fightclub:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database
        self.database = Database()
    
    def get_nick(self, user):
        nick = user.nick
        if not nick:
            nick = user.name
        return nick

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """I can talk about Fight Club."""
        welcome = "Fight Club. A game based on /r/bossfight.\n"
        user_id = ctx.message.author.id
        nick = self.get_nick(ctx.message.author)
        user = self.db.users.get(user_id)
        status = ""
        if user:
            status = "Welcome back, {}\nYour score is [{} wins : {} losses] You have {} pulls remaining."\
            .format(nick, user.wins, user.losses, user.pulls)
        else:
            status = "Hello, {}\nYou are not yet part of the game. Use $register to sign up. You will get 5 free random cards and 1 free card per day. Use $gacha to pull cards."\
            .format(nick)
        msg = "```{}{}```".format(welcome, status)
        await ctx.bot.send_message(ctx.message.channel, msg)
    
    @commands.command(pass_context=True)
    async def register(self, ctx):
        user_id = ctx.message.author.id
        nick = self.get_nick(ctx.message.author)
        user = self.db.users.get(user_id)
        if user:
            msg = "You are already a member of Fight Club."
        else:
            msg = "Welcome, {}. You have been awarded 5 free card pulls. Use $gacha to get your cards!".format(nick)
            self.db.users.add(id = user_id, pulls = 5)
        await ctx.bot.send_message(ctx.message.channel, msg)

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
