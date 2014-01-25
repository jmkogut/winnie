# http://www.pythoncentral.io/introductory-tutorial-python-sqlalchemy/
# ^ src

from sqlalchemy import *

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id',       Integer, primary_key=True),
    Column('username', String(512), nullable=False),
    Column('mask',     String(512), nullable=True)
)

if __name__ == '__main__':
    engine = create_engine('sqlite:///')
    metadata.create_all(engine)
    conn = engine.connect() 
