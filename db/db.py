import sqlite3
from crawler import crawler

class Database:

    def __init__(self, dbfile='bossfight.db'):
        """
        Database object that connects fo db file. 
        Parameters:
            dbfile = db file, make sure to place in root
        """
        self.connection = sqlite3.connect(dbfile)
        self.c = self.connection.cursor()

    def initTables(self):
        """
        Creates tables in a new db file.
        Note this is only for initialisation. 
        """
        self.c.execute('''CREATE TABLE bosses(sid, title, score, url, flavour)''')

    def registerBoss(self, boss):
        """
        Registers a boss to the db.
        Parameters:
            boss = a tuple of required boss info
        """
        self.c.execute("INSERT INTO bosses (sid, title, score, url, flavour) VALUES (?, ?, ?, ?, ?)", boss)                
        
    def commit(self):
        """
        Commits changes to db.
        """
        self.connection.commit()
        print('Changes committed to db')

    def randomBoss(self, num):
        """
        Pulls random {num} bosses from the db.
        Parameters:
            num = the number of bosses to pull
        """
        self.c.execute("SELECT * FROM bosses ORDER BY RANDOM() LIMIT ?", num)
        return self.c.fetchall()
