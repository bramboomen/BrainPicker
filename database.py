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
    ref = Column(String(250), ForeignKey('article.url'))


class Person(base):
    __tablename__ = 'person'
    name = Column(String(250), primary_key=True)


class PeopleRel(base):
    __tablename__ = 'people_rel'
    id = Column(String(250), primary_key=True)
    article = Column(String(250), ForeignKey('article.url'))
    person = Column(String(250), ForeignKey('person.name'))
    count = Column(Integer)
    main_person = Column(Boolean)


class Organisation(base):
    __tablename__ = 'organisation'
    name = Column(String(250), primary_key=True)


class OrganisationRel(base):
    __tablename__ = 'organisation_rel'
    id = Column(String(250), primary_key=True)
    article = Column(String(250), ForeignKey('article.url'))
    organisation = Column(String(250), ForeignKey('organisation.name'))
    count = Column(Integer)


class Location(base):
    __tablename__ = 'location'
    name = Column(String(250), primary_key=True)


class LocationRel(base):
    __tablename__ = 'location_rel'
    id = Column(String(250), primary_key=True)
    article = Column(String(250), ForeignKey('article.url'))
    location = Column(String(250), ForeignKey('location.name'))
    count = Column(Integer)


engine = create_engine('sqlite:///brain.db')
base.metadata.create_all(engine)
