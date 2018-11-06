from sqlalchemy import Column, Integer, String, Date, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(20), primary_key=True)
    badge = Column(String(300))
    color = Column(Integer, default=0x000000)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    pulls = Column(Integer, default=0)
    last_pull_date = Column(Date)
    roster = relationship("Roster", back_populates="user")

class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, Sequence('card_id_sequence'), primary_key=True)
    name = Column(String(200))
    image = Column(String(300))
    score = Column(Integer)
    sid = Column(String(6), unique=True)
    roster_entries = relationship("Roster", back_populates="card")

class Roster(Base):
    __tablename__ = 'rosters'
    id = Column(Integer, Sequence('roster_id_sequence'), primary_key=True)
    user_id = Column(String(20), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="roster")
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    card = relationship("Card", back_populates="roster_entries")
    level = Column(Integer, default=0)
    score = Column(Integer, default=0)
    attack_0 = Column(String(30))
    attack_1 = Column(String(30))
    attack_2 = Column(String(30))
    attack_3 = Column(String(30))
    power_0 = Column(Integer, default=1)
    power_1 = Column(Integer, default=1)
    power_2 = Column(Integer, default=1)
    power_3 = Column(Integer, default=1)
