# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# ^ src 
# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html#connecting
# /////////// GUIDES ///////////////////////////

# TODO: Add timestamp on intels

from sqlalchemy import *
from sqlalchemy.pool import Pool
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import *

# //////////////////////

engine = create_engine('sqlite:///winnie.sqlite', echo=False)
Base = declarative_base()
Session = sessionmaker( bind=engine )
session = Session()

def Create():
    Base.metadata.create_all(engine)

# //////////////////////

@listens_for(Pool, 'init')
def auto_add(target, args, kwargs):
    Session.add(target)

# //////////////////////

class User(Base):
    __tablename__ = 'users'

    id    = Column(Integer, primary_key=True)
    nick  = Column(String(convert_unicode=True))
    mask  = Column(String(convert_unicode=True))

    def __repr__(s): return '<User %s>' % (s.nick,)

    @classmethod
    def find_by(cls, nick):
        try:
            return session.query(User).filter(User.nick == nick).one()
        except NoResultFound, e:
            u = User(nick=nick,mask=nick)
            session.add(u)
            return u

    @classmethod
    def learned(cls, nick, target, text, save=True):
        u = User.find_by(nick)
        i = Intel(user=u, target=target, text=text)
        session.add(i)

        if save:
            session.commit()

class Intel(Base):
    __tablename__ = 'intel'

    id      = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text    = Column(String(convert_unicode=True))
    target  = Column(String(convert_unicode=True))

    user    = relationship("User", backref=backref('intels', order_by=id))

    def __repr__(s): return '<Intel %s>' % (s.id,)

def Import( n ):
    import re
    reg = re.compile(r'([^ ]+)\s<(\w+):[^ ]+>\s(.*)')
    p = lambda i: filter(None, reg.split(i))

    return [p(l.rstrip("\n")) for l in open( n ).readlines() ]

if __name__ == '__main__':
    Create()

    # i = 0
    # for e in Import("/home/joshua/projects/winnie/sample/boats.log"):
    #     i += 1
    #     if i % 100 == 0:
    #         session.commit()
    #         print i
    #     try:
    #         # print "%s :: %s" % (e[1],e[2])
    #         User.learned(e[1].encode('utf8'), '#boats', e[2].encode('utf8'), False)
    #     except UnicodeDecodeError:
    #         print "SKIPPEEEEED"

    # session.commit()
