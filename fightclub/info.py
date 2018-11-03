import discord
from discord.ext import commands
from db.util import users

@commands.command(pass_context=True)
async def info(ctx):
    """I can talk about Fight Club."""
    welcome = "Fight Club. A game based on /r/bossfight."
    user_id = ctx.message.author.id
    nick = ctx.message.author.nick
    if not nick:
        nick = ctx.message.author.name
    user = users.get(user_id)
    status = ""
    if user:
        status = "Welcome back, {}\nYour score is [{} wins : {} losses] You have {} pulls remaining."\
        .format(nick, user.wins, user.losses, user.pulls)
    else:
        status = "Welcome, {}\nYou are not yet part of the game. Use $register to sign up. You will get 5 free random cards and 1 free card per day. Use $gacha to pull cards."\
        .format(nick)
    msg = "```{}{}```".format(welcome, status)
    await ctx.bot.send_message(ctx.message.channel, msg)