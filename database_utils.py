from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import base, Article, Reference


class db_session:


    def __init__(self):
        engine = create_engine('sqlite:///brain.db')
        base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()


    def insert_article(self, art):
        exists = self.session.query(Article).filter_by(url=art['url']).first()
        article = Article(url=art['url'], title=art['title'], date=art['date'])
        if not exists:
            self.session.add(article)
            print("added: " + art['title'] + " to Database")
        else:
            self.session.merge(article)
            print("merged: " + art['title'] + " in Database")
        self.session.commit()


    def insert_reference(self, ref):
        reference = Reference(url=ref['url'], ref=ref['ref'])
        self.session.add(reference)

    def commit(self):
        self.session.commit()
