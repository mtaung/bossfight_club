import discord, asyncio, random, math
from datetime import date
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
        self.challenges = dict()
    
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
            self.db.users.add(id = user_id, pulls = 5, last_pull_date = date.min)
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
        embed.add_field(name=roster.attack_0, value=f'might: {roster.power_0}', inline=True)
        embed.add_field(name=roster.attack_1, value=f'might: {roster.power_1}', inline=True)
        embed.add_field(name=roster.attack_2, value=f'might: {roster.power_2}', inline=True)
        embed.add_field(name=roster.attack_3, value=f'might: {roster.power_3}', inline=True)
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
        if user.last_pull_date >= date.today():
            # has no daily pull
            if not user.pulls:
                msg = "You have no more pulls left."
                await ctx.bot.send_message(ctx.message.channel, msg)
                return
            else:
                user.pulls -= 1
        else:
            user.last_pull_date = date.today()
        card = self.random_card()
        attacks = generate_attack_names(card.name)
        score = card.score if card.score > 400 else 400
        roster_entry = self.db.rosters.add(user=user, card=card, level=0, score=score,\
        attack_0=attacks[0], attack_1=attacks[1], attack_2=attacks[2], attack_3=attacks[3],\
        power_0=1, power_1=1, power_2=1, power_3=1)
        self.give_exp(roster_entry, 0)
        embed = self.embed_card(user, card, roster_entry)
        self.db.commit()
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
    
    def format_roster_entry(self, entry):
        card = entry.card
        col1 = str(entry.id)
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
        entries = user.roster
        msg = f"```{nick}'s cards:"
        for e in entries:
            msg += '\n'
            msg += self.format_roster_entry(e)
        msg += f"```"
        await ctx.bot.send_message(ctx.message.channel, msg)
    
    @commands.command(pass_context=True)
    async def show(self, ctx, card):
        """Displays a card from your roster."""
        user = await self.registration_check(ctx)
        # verify that card id is valid
        entry = self.db.rosters.get(card)
        if not entry or entry.user_id != user.id:
            await ctx.bot.send_message(ctx.message.channel, f"Card #{card} not found in your roster.")
            return
        _card = entry.card
        embed = self.embed_card(user, _card, entry)
        await ctx.bot.send_message(ctx.message.channel, embed=embed)
    
    def get_attack(self, entry, num):
        name = getattr(entry, f'attack_{num}')
        power = getattr(entry, f'power_{num}')
        return name, power

    def combat_round(self, entry1, name1, entry2, name2):
        e1 = self.get_attack(entry1, random.randint(0, 3))
        e2 = self.get_attack(entry2, random.randint(0, 3))
        r1 = random.randint(1, 6) + e1[1]
        r2 = random.randint(1, 6) + e2[1]
        if r1 == r2:
            # tie
            msg = f"{name1}'s {e1[0]} and {name2}'s {e2[0]} were evenly matched! [{r1} vs {r2}]"
            return 0, msg
        elif r1 > r2:
            msg = f"{name1}'s {e1[0]} overwhelmed {name2}'s {e2[0]}! [{r1} vs {r2}]"
            return -1, msg
        else:
            msg = f"{name2}'s {e2[0]} overwhelmed {name1}'s {e1[0]}! [{r2} vs {r1}]"
            return 1, msg
    
    @commands.command(pass_context=True)
    async def duel(self, ctx, opponent:discord.Member, card:int):
        """Duel someone else with a card from your roster."""
        user = await self.registration_check(ctx)
        nick = self.get_nick(ctx.message.author)
        opp_user = self.db.users.get(opponent.id)
        opp_nick = self.get_nick(opponent)
        # verify that opponent can be challenged
        if not opp_user:
            await ctx.bot.send_message(ctx.message.channel, f"{opp_nick} is not a member of Fight Club.")
            return
        if opp_user.id == user.id:
            await ctx.bot.send_message(ctx.message.channel, f"You can't duel yourself.")
            return
        # verify that card id is valid
        entry = self.db.rosters.get(card)
        if not entry or entry.user_id != user.id:
            await ctx.bot.send_message(ctx.message.channel, f"Card #{card} not found in your roster.")
            return
        # set up the duel
        _card = entry.card
        # check if the opponent has issued a challenge already
        # pop challenge if exists
        opp_id = self.challenges.pop((opp_user.id, user.id), None)
        if not opp_id:
            # they haven't, so we issue a challenge message
            self.challenges[(user.id, opp_user.id)] = entry.id
            await ctx.bot.send_message(ctx.message.channel, f"{nick} has challenged {opp_nick} to a duel with {_card.name}")
            return
        else:
            # they have, begin duel
            await ctx.bot.send_message(ctx.message.channel, f"{nick} accepts {opp_nick}'s challenge with his champion, {_card.name}")
            opp_entry = self.db.rosters.get(opp_id)
            opp_card = opp_entry.card
            # 3 rounds
            total = 0
            content = "Begin duel!"
            msg = await ctx.bot.send_message(ctx.message.channel, content)
            for i in range(3):
                r, text = self.combat_round(entry, _card.name, opp_entry, opp_card.name)
                total += r
                content += '\n' + text
                await asyncio.sleep(2)
                await ctx.bot.edit_message(msg, content)
            if total == 0:
                # tie
                content += '\n' + "Nobody wins."
                await ctx.bot.edit_message(msg, content)
            elif total < 0:
                user.wins += 1
                opp_user.losses += 1
                prev_level = entry.level
                exp_gain = opp_entry.level * 100
                content += '\n' + f"Congratulations, {nick}, {_card.name} is victorious and gains {exp_gain} exp!"
                await ctx.bot.edit_message(msg, content)
                self.give_exp(entry, exp_gain)
                if prev_level < entry.level:
                    await ctx.bot.send_message(ctx.message.channel, f"{_card.name} has leveled up!")
            elif total > 0:
                opp_user.wins += 1
                user.losses += 1
                prev_level = opp_entry.level
                exp_gain = entry.level * 100
                content += '\n' + f"Congratulations, {opp_nick}, {opp_card.name} is victorious and gains {exp_gain} exp!"
                await ctx.bot.edit_message(msg, content)
                self.give_exp(opp_entry, exp_gain)
                if prev_level < opp_entry.level:
                    await ctx.bot.send_message(ctx.message.channel, f"{_card.name} has leveled up!")
