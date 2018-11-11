

class Card():

    #On creation define variables.
    def __init__(self, card_id, user_id, team_id)
    
        #Lists for allies and enemies, to be populated before starting the fight
        #and to be checked before each attack.
        self.allies = list<int>
        self.enemies = list<int>
        
        #Populate card stats.
        self.user_id = 
        self.card_id =
        self.team_id =
        self.element = 
        self.max_health = 
        self.current_health = 
        self.initiative = 
        self.defense = 
        self.attack = 

    #Attack Logic here.
    async def Attack(self,fight_list)

        #Pick a random skill from the available ones.
        skill_to_use = Random("List of attacks owned by this card")

        #From the attack you read the possible targets and effects, then apply logic here.
        #In this step it should check if any of the targets HP <= 0 and if so, remove from the fight_list        
        execute skill_to_use




    #Methods to manipulate the allies and enemies lists.
    def add_allies(self,allies_list)
        allies = allies_list

    def add_enemies(self,enemies_list)
        enemies = enemies_list

    def remove_ally(self,card_id)
        allies.remove(card_id)

    def remove_enemy(self,card_id)
        enemies.remove(card_id)



        
