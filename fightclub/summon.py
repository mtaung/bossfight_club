from fightclub.util import registration_check, embed_card, get_nick, give_exp

class Summon:

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database

    def random_card(self):
        total_cards = self.db.cards.count()
        rand = int(total_cards * random.random())
        return self.db.cards.getrow(rand)
    
    @commands.command(pass_context=True)
    async def summon(self, ctx):
        """Receive a random card."""
        user = await registration_check(ctx, self.db)
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
        self.give_exp(roster_entry, 0, self.db)
        embed = embed_card(user, card, roster_entry)
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
        user = await registration_check(ctx, self.db)
        nick = get_nick(ctx.message.author)
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
        user = await registration_check(ctx, self.db)
        # verify that card id is valid
        entry = self.db.rosters.get(card)
        if not entry or entry.user_id != user.id:
            await ctx.bot.send_message(ctx.message.channel, f"Card #{card} not found in your roster.")
            return
        _card = entry.card
        embed = embed_card(user, _card, entry)
        await ctx.bot.send_message(ctx.message.channel, embed=embed)