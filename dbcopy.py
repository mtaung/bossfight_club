from db import tables
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db.util import DatabaseInterface

db_old = create_engine('sqlite:///fightclub_old.db')
Base = declarative_base(db_old)

class Boss(Base):
    __tablename__ = 'cards'
    __table_args__ = {'autoload':True}
    sid = Column(String(6), primary_key=True)

Session = sessionmaker(bind=db_old)
session = Session()

db_new = DatabaseInterface('sqlite:///fightclub.db')

query = session.query(Boss).all()
for row in query:
    db_new.cards.add(name=row.name, image=row.image, score=row.score, sid=row.sid)
db_new.commit()
