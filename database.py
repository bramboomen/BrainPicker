from sqlalchemy import Column, ForeignKey, Integer, String
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
    article = relationship(Article)


engine = create_engine('sqlite:///brain.db')
base.metadata.create_all(engine)