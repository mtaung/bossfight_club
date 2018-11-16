from fightclub.fightmanager import FightManager
from fightclub.fightclub import Fightclub
from fightclub.summon import Summon

def setup(bot):
    bot.add_cog(Fightclub(bot))
    bot.add_cog(Summon(bot))
    bot.add_cog(FightManager(bot))