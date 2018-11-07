
class Summon:
    
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database

    def random_card(self):
        total_cards = self.db.cards.count()
        rand = int(total_cards * random.random())
        return self.db.cards.getrow(rand)
    
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