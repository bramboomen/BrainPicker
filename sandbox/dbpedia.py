from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pyparsing import Suppress, QuotedString, SkipTo
from sqlalchemy import Column, Integer, String


engine = create_engine('sqlite:///names.db')
base = declarative_base()
base.metadata.bind = engine
db_session = sessionmaker(bind=engine)
session = db_session()


class Name(base):
    __tablename__ = 'name'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    surname = Column(String(250), nullable=True)
    givenname = Column(String(250), nullable=True)


base.metadata.create_all(engine)


def create_names_db():
    p = Suppress(SkipTo('"')) + QuotedString('"') + Suppress(SkipTo("."))

    with open("persondata_en.ttl") as pd:
        for line in pd:
            surname, givenname = None, None
            if "/name" in line:
                name = p.parseString(line)[0]
                line = pd.__next__()
                if "/surname" in line:
                    surname = p.parseString(line)[0]
                    line = pd.__next__()
                    if "/givenName" in line:
                        givenname = p.parseString(line)[0]
                n = Name(name=name, surname=surname, givenname=givenname)
                session.add(n)
                session.commit()
