# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# ^ src 
# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#connecting
# /////////// GUIDES ///////////////////////////

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import *

engine = create_engine('sqlite:///winnie.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def Init():
    Base.metadata.create_all(engine)

def Save(item, ses=False):
    if ses == False:
        ses = Session()

    ses.add(item)
    ses.commit()
    return ses

# //////////////////////

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nick = Column(String)
    mask = Column(String)

    def __repr__(s):
        return '<User %s>' % (s.nick,)

def find_nick(nick, s=False):
    if s == False: s = Session()
    try:
        return s.query(User.nick).filter(User.nick == nick).first()
    except NoResultFound, e:
        return False

