import discord

async def registration_check(ctx, db):
    user_id = ctx.message.author.id
    user = db.users.get(user_id)
    if not user:
        msg = f"You are not a registered member of Fight Club. Use $info for more information."
        await ctx.bot.send_message(ctx.message.channel, msg)
        raise commands.CheckFailure()
    return user

def get_nick(user):
    nick = user.nick
    if not nick:
        nick = user.name
    return nick

def embed_card(user, card, roster):
    embed = discord.Embed(title=f'Level: {roster.level} ({roster.score} xp)', colour=discord.Colour(value=user.color))
    if user.badge:
        embed.set_author(name=f'{card.name}', icon_url=user.badge)
    else:
        embed.set_author(name=f'{card.name}')
    embed.set_image(url=card.image)
    embed.add_field(name=roster.attack_0, value=f'🗡️ {roster.power_0}', inline=True)
    embed.add_field(name=roster.attack_1, value=f'🗡️ {roster.power_1}', inline=True)
    embed.add_field(name=roster.attack_2, value=f'🗡️ {roster.power_2}', inline=True)
    embed.add_field(name=roster.attack_3, value=f'🗡️ {roster.power_3}', inline=True)
    return embed

def level_formula(exp):
    #500 exp ~ level 1
    #1'700 ~ level 5
    #8'000 ~ level 10
    #20'000 ~ level 12
    return math.floor((math.log(exp, 400) - 1) * 20) + 1

def level_up(entry):
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

def give_exp(entry, exp, db):
    entry.score += exp
    new_level = level_formula(entry.score)
    while entry.level < new_level:
        level_up(entry)
    db.commit()