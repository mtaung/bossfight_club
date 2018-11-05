import discord, asyncio, random
from discord.ext import commands
from db.util import DatabaseInterface
from .name_generator import generate_attack_names

class Fightclub:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database
    
    def get_nick(self, user):
        nick = user.nick
        if not nick:
            nick = user.name
        return nick
    
    async def registration_check(self, ctx):
        user_id = ctx.message.author.id
        user = self.db.users.get(user_id)
        if not user:
            msg = f"You are not a registered member of Fight Club. Use $info for more information."
            await ctx.bot.send_message(ctx.message.channel, msg)
            raise commands.CheckFailure()
        return user

    @commands.command(pass_context=True)
    async def info(self, ctx):
        """I can talk about Fight Club."""
        welcome = "Fight Club. A game based on /r/bossfight."
        user_id = ctx.message.author.id
        nick = self.get_nick(ctx.message.author)
        user = self.db.users.get(user_id)
        if user:
            status = f"Welcome back, {nick}\nYour score is [{user.wins} wins : {user.losses} losses] You have {user.pulls} pulls remaining."
        else:
            status = f"Hello, {nick}\nYou are not yet part of the game. Use $register to sign up. You will get 5 random cards and 1 card per day. Use $gacha to pull cards."
        msg = "```{}\n{}```".format(welcome, status)
        await ctx.bot.send_message(ctx.message.channel, msg)
    
    @commands.command(pass_context=True)
    async def register(self, ctx):
        """Join the Fight Club."""
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
        user = await self.registration_check(ctx)
        if not user:
            return
        #TODO: verify input
        if param == 'color':
            user.color = int(value, 16)
            self.db.commit()
        elif param == 'badge':
            user.badge = value
            self.db.commit()
    
    def embed_card(self, user, card, roster):
        embed = discord.Embed(title=f'Power Level: {roster.score}', colour=discord.Colour(value=user.color))
        if user.badge:
            embed.set_author(name=f'{card.name}', icon_url=user.badge)
        else:
            embed.set_author(name=f'{card.name}')
        embed.set_image(url=card.image)
        #unfinished
        embed.add_field(name=roster.attack_0, value='Attack Value', inline=True)
        embed.add_field(name=roster.attack_1, value='Attack Value', inline=True)
        embed.add_field(name=roster.attack_2, value='Attack Value', inline=True)
        embed.add_field(name=roster.attack_3, value='Attack Value', inline=True)
        #
        return embed
    
    def random_card(self):
        total_cards = self.db.cards.count()
        rand = int(total_cards * random.random())
        return self.db.cards.getrow(rand)

    @commands.command(pass_context=True)
    async def gacha(self, ctx):
        """Receive a random card."""
        user = await self.registration_check(ctx)
        if not user.pulls:
            msg = "You have no more pulls left."
            await ctx.bot.send_message(ctx.message.channel, msg)
            return
        card = self.random_card()
        attacks = generate_attack_names(card.name)
        roster_entry = self.db.rosters.add(user_id=user.id, card_id=card.id, score=card.score,\
        attack_0=attacks[0], attack_1=attacks[1], attack_2=attacks[2], attack_3=attacks[3])
        embed = self.embed_card(user, card, roster_entry)
        user.pulls -= 1
        self.db.commit()
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
    
    def format_roster_entry(self, entry):
        card = self.db.cards.get(entry.card_id)
        col1 = str(card.id)
        col1 += ' '*(5 - len(col1))
        col2 = str(card.name)
        if len(col2) > 50:
            col2 = col2[:47]
            col2 += '...'
        else:
            col2 += ' '*(50 - len(col2))
        return f"#{col1} {col2} p:{entry.score}"

    @commands.command(pass_context=True)
    async def roster(self, ctx):
        """List the cards you own."""
        user = await self.registration_check(ctx)
        nick = self.get_nick(ctx.message.author)
        entries = self.db.rosters.user_inventory(user.id)
        msg = f"```{nick}'s cards:"
        for e in entries:
            msg += '\n'
            msg += self.format_roster_entry(e)
        msg += f"```"
        await ctx.bot.send_message(ctx.message.channel, msg)
    
    @commands.command(pass_context=True)
    async def cheat(self, ctx):
        """Cheat yourself some pulls for testing."""
        user = await self.registration_check(ctx)
        user.pulls += 5
        self.db.commit()
