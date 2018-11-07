import discord, asyncio, random, math
from datetime import date
from discord.ext import commands
from db.util import DatabaseInterface
from .name_generator import generate_attack_names
from formulae import level_formula

class Fightclub:
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database
        self.challenges = dict()

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
        if param == 'color':
            user.color = int(value, 16)
            self.db.commit()
        elif param == 'badge':
            user.badge = value
            self.db.commit()
    
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
