from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(20), primary_key=True)
    wins = Column(Integer)
    losses = Column(Integer)

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, Sequence('card_id_sequence'), primary_key=True)
    name = Column(String(200))
    image = Column(String(300))
    score = Column(Integer)
    sid = Column(String(6), unique=True)

class Roster(Base):
    __tablename__ = 'rosters'
    id = Column(Integer, Sequence('roster_id_sequence'), primary_key=True)
    user_id = Column(String(20), ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    move_1 = Column(String(30))
    move_2 = Column(String(30))
    move_3 = Column(String(30))
    move_4 = Column(String(30))
    power_1 = Column(Integer)
    power_2 = Column(Integer)
    power_3 = Column(Integer)
    power_4 = Column(Integer)