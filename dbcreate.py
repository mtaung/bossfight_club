from db import tables
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///fightclub.db')
tables.Base.metadata.bind = engine
tables.Base.metadata.create_all()
