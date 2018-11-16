import discord
import asyncio
import random
from discord.ext import commands
from operator import itemgetter, attrgetter
from fightclub import card
from db.util import DatabaseInterface
from fightclub.util import get_nick

class FightManager:

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.database

    #The lobby list will be a list of Cards, the Cards themselves will host the list of current users.
    #Empty when no lobby is active.
    
    ### lobby_list = list(card)
    
    #Command to start a lobby or join an existing fight.
    #Inputs will be Team_ID and Card_ID.
    #Team_ID will be a user generated string, everyone using the same string will be on the same team.
    @commands.command(pass_context=True)
    async def lobby(self, ctx, team_id, *args):

        cards_list = args
        for item in cards_list:
            print(item)

        user_id = ctx.message.author.id
        nick = get_nick(ctx.message.author)
        user = self.db.users.get(user_id)

        #Info to grab from the user is the discord ID to check card ownership
        #If everything its ok it will return a list of Card with all the card info in it.
        
        ### self.lobby_list.append(Insert_Actual_Check_Funtion_Here("Discord ID", "Team_ID", "List of Cards to check"))

        #If error return message telling to check the Cards and retry again
        #This should be done inside the previous ownership check
        
    #Once the timer runs out, the fight will begin.
    #Since each card has all the info in them, the manager will just order them by initiative and tell them to attack.

    #Get all the cards IDs and tell the db to return them ordered by Initiative.
    #Then pass the lobby_list to a fight_list.

    ### fight_list = sorted(lobby_list, key=attrgetter("initiative"), reverse=False)

    #==============INSERT ACTUAL ROUND LOGIC BELOW THIS POINT==============
        
    #Populate card's allies and enemies list

    ###for card in fight_list:
    ###    card.set_allies("Filtered fight_list with only cards with the same team_id.")
    ###    card.set_enemies("Filtered fight_list with all the other cards.")
    
    #The idea is, since each Card is its own Class, to just call the .attack() function
    #while going down the fight_list.
    
    ###for card in fight_list:
    ###    card.attack(fight_list)
    
    #The effects of the attacks will be applied when the cards attack, that means that if a card dies, its removed from the list
    #so it won't be target nor actor from that point forwards.
    #Each Card will also have a list of "Friendly" and "Enemy" IDs to know what to target.

    #When all the rounds are done decide the winner based on w/e factors you want.
    #Give prices.