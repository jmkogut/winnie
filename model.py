# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# ^ src 
# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#connecting
# /////////// GUIDES ///////////////////////////

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import *

# //////////////////////

engine = create_engine('sqlite:///winnie.sqlite', echo=True)
Base = declarative_base()
Session = scoped_session(sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=True
))
Base.metadata.create_all(engine)

# //////////////////////

@event.listens_for(mapper, 'init')
def auto_add(target, args, kwargs):
    Session.add(target)

# //////////////////////

class User(Base):
    __tablename__ = 'users'

    id    = Column(Integer, primary_key=True)
    nick  = Column(String)
    mask  = Column(String)
    intel = relationship("Intel", order_by="Intel.id", backref="user")

    def __repr__(s): return '<User %s>' % (s.nick,)

    @classmethod
    def find_by(cls, nick):
        try:
            return Session.query(User).filter(User.nick == nick).one()
        except NoResultFound, e:
            u = User(nick=nick,mask=nick)
            Session.add(u)
            Session.commit(u)
            return u

    @classmethod
    def learned(cls, nick, text):
        u = User.find_by(nick)
        i = Intel(user=u, text=text)
        Session.add(i)
        Session.commit()

class Intel(Base):
    __tablename__ = 'intel'

    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text    = Column(String)

    user    = relationship("User", backref=backref('intels', order_by=id))

    def __repr__(s): return '<Intel %s>' % (s.id,)
