import discord, asyncio, random
from discord.ext import commands
from db.util import DatabaseInterface
from crawler.crawler import Crawler

class Fightclub:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database
    
    def get_nick(self, user):
        nick = user.nick
        if not nick:
            nick = user.name
        return nick
    
    def unregistered_message(self, nick):
        return f"Hello, {nick}\nYou are not yet part of the game. Use $register to sign up. You will get 5 free random cards and 1 free card per day. Use $gacha to pull cards."

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """I can talk about Fight Club."""
        welcome = "Fight Club. A game based on /r/bossfight."
        user_id = ctx.message.author.id
        nick = self.get_nick(ctx.message.author)
        user = self.db.users.get(user_id)
        if not user:
            await ctx.bot.send_message(ctx.message.channel, self.unregistered_message(nick))
            return
        status = f"Welcome back, {nick}\nYour score is [{user.wins} wins : {user.losses} losses] You have {user.pulls} pulls remaining."
        msg = "```{}\n{}```".format(welcome, status)
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
            self.db.commit()
        await ctx.bot.send_message(ctx.message.channel, msg)
    
    @commands.command(pass_context=True)
    async def custom(self, ctx, param, value):
        """Usage: custom color FFDE16 | custom badge http://badge-url.jpg"""
        user_id = ctx.message.author.id
        user = self.db.users.get(user_id)
        if not user:
            return
        #todo: verify input
        if param == 'color':
            user.color = int(value, 16)
            self.db.commit()
        elif param == 'badge':
            user.badge = value
            self.db.commit()
    
    def embed_card(self, user, card, roster):
        #unfinished
        #should be roster.score
        embed = discord.Embed(title=f'Power Level: {card.score}', colour=discord.Colour(value=user.color))
        if user.badge:
            embed.set_author(name=f'{card.name}', icon_url=user.badge)
        else:
            embed.set_author(name=f'{card.name}')
        embed.set_image(url=card.image)
        #unfinished
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        embed.add_field(name='Attack Name', value='Attack Value', inline=True)
        #
        return embed
    
    def random_card(self):
        total_cards = self.db.cards.count()
        rand = int(total_cards * random.random())
        return self.db.cards.getrow(rand)

    @commands.command(pass_context=True)
    async def gacha(self, ctx):
        user_id = ctx.message.author.id
        user = self.db.users.get(user_id)
        if not user:
            nick = self.get_nick(ctx.message.author)
            await ctx.bot.send_message(ctx.message.channel, self.unregistered_message(nick))
            return
        card = self.random_card()
        #todo: add card to user's roster
        embed = self.embed_card(user, card, None)
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
