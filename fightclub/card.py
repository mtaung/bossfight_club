import time
import discord
import asyncio
import random
from discord.ext import commands

class Card:

    #On creation define variables.
    def __init__(self, card_id, user_id, team_id):
    
        #Lists for allies and enemies, to be populated before starting the fight
        #and to be checked before each attack.
        self.allies = list(int)
        self.enemies = list(int)
        
        
        #Populate card stats.
        self.user_id = user_id
        self.card_id = card_id
        self.team_id = team_id
        self.element = "Placeholder"
        self.max_health = "Placeholder"
        self.current_health = "Placeholder"
        self.initiative = "Placeholder"
        self.defense = "Placeholder"
        self.attack = "Placeholder"

    #Attack Logic here.
    async def Attack(self,fight_list):

        #Pick a random skill from the available ones.
        skill_to_use = random.choice("List of attacks owned by this card")

        #From the attack you read the possible targets and effects, then apply logic here.
        #In this step it should check if any of the targets HP <= 0 and if so, remove from the fight_list        
        "execute skill_to_use"




    #Methods to manipulate the allies and enemies lists.
    def add_allies(self,allies_list):
        self.allies = allies_list

    def add_enemies(self,enemies_list):
        self.enemies = enemies_list

    def remove_ally(self,card_id):
        self.allies.remove(card_id)

    def remove_enemy(self,card_id):
        self.enemies.remove(card_id)



        
