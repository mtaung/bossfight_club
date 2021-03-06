from sqlalchemy import create_engine, literal
from sqlalchemy.orm import sessionmaker
from . import tables

class BasicInterface:
    def __init__(self, table, session):
        self.Table = table
        self.session = session

    def get(self, id):
        return self.session.query(self.Table).filter(self.Table.id == id).first()
    
    def add(self, **kwargs):
        if kwargs:
            dbo = self.Table(**kwargs)
            self.session.add(dbo)
            return dbo
        return None
    
    def count(self):
        return self.session.query(self.Table).count()
    
    def getrow(self, row):
        return self.session.query(self.Table).offset(row).first()

class CardInterface(BasicInterface):
    def sid_exists(self, sid):
        q = self.session.query(self.Table).filter(self.Table.sid == sid)
        return self.session.query(literal(True)).filter(q.exists()).scalar()

class RosterInterface(BasicInterface):
    def user_inventory(self, user_id):
        return self.session.query(self.Table).filter(self.Table.user_id == user_id)

class DatabaseInterface:
    def __init__(self, url):
        engine = create_engine(url)
        Session = sessionmaker(bind=engine)
        self.main_session = Session()
        self.users = BasicInterface(tables.User, self.main_session)
        self.cards = CardInterface(tables.Card, self.main_session)
        self.rosters = RosterInterface(tables.Roster, self.main_session)
    
    def commit(self):
        self.main_session.commit()
