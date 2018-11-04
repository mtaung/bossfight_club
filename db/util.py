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
        main_session = Session()
        self.users = BasicInterface(tables.User, main_session)
        self.cards = CardInterface(tables.Card, main_session)
        self.rosters = RosterInterface(tables.Roster, main_session)
