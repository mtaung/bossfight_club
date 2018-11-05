import discord, asyncio, random, math
from discord.ext import commands
from db.util import DatabaseInterface
from .name_generator import generate_attack_names

def level_formula(exp):
    #500 exp ~ level 1
    #1'700 ~ level 5
    #8'000 ~ level 10
    #20'000 ~ level 12
    return math.floor((math.log(exp, 400) - 1) * 20) + 1

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
        embed = discord.Embed(title=f'Level: {roster.level} ({roster.score} xp)', colour=discord.Colour(value=user.color))
        if user.badge:
            embed.set_author(name=f'{card.name}', icon_url=user.badge)
        else:
            embed.set_author(name=f'{card.name}')
        embed.set_image(url=card.image)
        #unfinished
        embed.add_field(name=roster.attack_0, value=f'might: {roster.power_0}', inline=True)
        embed.add_field(name=roster.attack_1, value=f'might: {roster.power_1}', inline=True)
        embed.add_field(name=roster.attack_2, value=f'might: {roster.power_2}', inline=True)
        embed.add_field(name=roster.attack_3, value=f'might: {roster.power_3}', inline=True)
        #
        return embed
    
    def random_card(self):
        total_cards = self.db.cards.count()
        rand = int(total_cards * random.random())
        return self.db.cards.getrow(rand)
    
    def level_up(self, entry):
        entry.level += 1
        # 4 skill points per level up, randomly distributed
        points = 4
        r = range(points)
        alloc = [0, 0, 0, 0]
        for i in r:
            alloc[random.choice(r)] += 1
        entry.power_0 += alloc[0]
        entry.power_1 += alloc[1]
        entry.power_2 += alloc[2]
        entry.power_3 += alloc[3]
    
    def give_exp(self, entry, exp):
        entry.score += exp
        new_level = level_formula(entry.score)
        while entry.level < new_level:
            self.level_up(entry)
        self.db.commit()

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
        score = card.score if card.score > 400 else 400
        roster_entry = self.db.rosters.add(user_id=user.id, card_id=card.id, level=0, score=score,\
        attack_0=attacks[0], attack_1=attacks[1], attack_2=attacks[2], attack_3=attacks[3],\
        power_0=1, power_1=1, power_2=1, power_3=1)
        self.give_exp(roster_entry, 0)
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
        return f"#{col1} {col2} lvl:{entry.level}"

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
