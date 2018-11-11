import time
import discord
import asyncio
import random
import card
from discord.ext import commands


class FightManager:

#The lobby list will be a list of Cards, the Cards themselves will host the list of current users.
#Empty when no lobby is active.
lobby_list = list<Card>

    #Command to start a lobby or join an existing fight.
    #Inputs will be Team_ID and Card_ID.
    #Team_ID will be a user generated string, everyone using the same string will be on the same team.

    async def lobby(self,ctx)

        #Info to grab from the user is the discord ID to check card ownership
        #If everything its ok it will return a list of Card with all the card info in it.
        lobby_list.add(Insert_Actual_Check_Funtion_Here("Discord ID", "Team_ID", "List of Cards to check"))

        #If error return message telling to check the Cards and retry again
        #This should be done inside the previous ownership check
        
    #Once the timer runs out, the fight will begin.
    #Since each card has all the info in them, the manager will just order them by initiative and tell them to attack.

    #Get all the cards IDs and tell the db to return them ordered by Initiative.
    #Then pass the lobby_list to a fight_list.

    fight_list = Get_IDs_And_Return_Ordered_By_Initiative(lobby_list)

    #==============INSERT ACTUAL ROUND LOGIC BELOW THIS POINT==============
        
    #The idea is, since each Card is its own Class, to just call the .attack() function
    #while going down the fight_list.
    
    for card in fight_list:
        card.attack(fight_list)
    
    #The effects of the attacks will be applied when the cards attack, that means that if a card dies, its removed from the list
    #so it won't be target nor actor from that point forwards.
    #Each Card will also have a list of "Friendly" and "Enemy" IDs to know what to target.

    #When all the rounds are done decide the winner based on w/e factors you want.
    #Give prices.