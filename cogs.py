import crawler, db, fightclub

def setup(bot):
    crawler.setup(bot)
    db.setup(bot)
    fightclub.setup(bot)