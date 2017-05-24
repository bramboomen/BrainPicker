from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import types

base = declarative_base()


class Article(base):
    __tablename__ = 'article'
    url = Column(String(250), primary_key=True)
    title = Column(String(250), nullable=False)
    date = Column(types.Date, nullable=True)


class Reference(base):
    __tablename__ = 'reference'
    id = Column(String(250), primary_key=True)
    url = Column(String(250), nullable=False)
    ref = Column(String(250), ForeignKey('article.url', ondelete="CASCADE", onupdate="CASCADE"))


class Person(base):
    __tablename__ = 'person'
    name = Column(String(250), primary_key=True)
    count = Column(Integer)
    verified = Column(Boolean)


class PeopleRel(base):
    __tablename__ = 'people_rel'
    id = Column(String(250), primary_key=True)
    article = Column(String(250), ForeignKey('article.url', ondelete="CASCADE", onupdate="CASCADE"))
    person = Column(String(250), ForeignKey('person.name', ondelete="CASCADE", onupdate="CASCADE"))
    count = Column(Integer)
    main_person = Column(Boolean)


class Organisation(base):
    __tablename__ = 'organisation'
    name = Column(String(250), primary_key=True)
    verified = Column(Boolean)


class OrganisationRel(base):
    __tablename__ = 'organisation_rel'
    id = Column(String(250), primary_key=True)
    article = Column(String(250), ForeignKey('article.url', ondelete="CASCADE", onupdate="CASCADE"))
    organisation = Column(String(250), ForeignKey('organisation.name', ondelete="CASCADE", onupdate="CASCADE"))
    count = Column(Integer)


class Location(base):
    __tablename__ = 'location'
    name = Column(String(250), primary_key=True)
    verified = Column(Boolean)


class LocationRel(base):
    __tablename__ = 'location_rel'
    id = Column(String(250), primary_key=True)
    article = Column(String(250), ForeignKey('article.url', ondelete="CASCADE", onupdate="CASCADE"))
    location = Column(String(250), ForeignKey('location.name', ondelete="CASCADE", onupdate="CASCADE"))
    count = Column(Integer)


class PersonRel(base):
    __tablename__ = 'person_rel'
    id = Column(Integer, autoincrement=True, primary_key=True)
    person1 = Column(String(250), ForeignKey('person.name', ondelete="CASCADE", onupdate="CASCADE"))
    person2 = Column(String(250), ForeignKey('person.name', ondelete="CASCADE", onupdate="CASCADE"))
    count = Column(Integer)

# engine = create_engine('postgresql://braindb@localhost/braindb')
engine = create_engine('sqlite:///brain.db')
base.metadata.create_all(engine)
