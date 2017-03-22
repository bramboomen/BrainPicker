from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
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
        exists = self.session.query(Reference).filter_by(id=ref['id']).first()
        reference = Reference(id=id, url=ref['url'], ref=ref['ref'])
        if not exists:
            self.session.add(reference)
            print("added link from: " + ref['url'] + " to: " + ref['ref'])
        else:
            print("link already exists in database")

    def commit(self):
        self.session.commit()
