import crawler, db, fightclub, util

def setup(bot):
    crawler.setup(bot)
    db.setup(bot)
    fightclub.setup(bot)
    #util.setup(bot)