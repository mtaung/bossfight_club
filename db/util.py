from sqlalchemy import create_engine, literal
from sqlalchemy.orm import sessionmaker
from . import tables

Session = sessionmaker()
main_session = None

def dbopen(url):
    engine = create_engine(url)
    Session.configure(bind=engine)
    global main_session
    main_session = Session()

def dbreset(url):
    """Drops all tables and remakes them. Doesn't fuck around."""
    engine = create_engine(url)
    tables.Base.metadata.bind = engine
    tables.Base.metadata.drop_all()
    tables.Base.metadata.create_all()

class BasicInterface:
    def __init__(self, table, session):
        self.Table = table
        self.session = session

    def get(self, id):
        return self.session.query(self.Table).filter(self.Table.id == id).first()
    
    def add(self, **kwargs):
        if kwargs:
            dbo = self.Table(kwargs)
            self.session.add(dbo)

class CardInterface(BasicInterface):
    def sid_exists(self, sid):
        q = self.session.query(self.Table).filter(self.Table.sid == sid)
        return self.session.query(literal(True)).filter(q.exists()).scalar()

class RosterInterface(BasicInterface):
    def user_inventory(self, user_id):
        return self.session.query(self.Table).filter(self.Table.user_id == user_id)

users = BasicInterface(tables.User, main_session)
cards = CardInterface(tables.Card, main_session)
rosters = RosterInterface(tables.Roster, main_session)
