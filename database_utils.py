from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib
from database import base, Article, Reference, Person, ArticlePeople


class DBSession:

    def __init__(self):
        engine = create_engine('sqlite:///brain.db')
        base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

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
        # Generate unique id for db
        sha_id = hashlib.sha1(bytes(ref['url'] + ref['ref'], 'utf-8'))
        ref['id'] = sha_id.hexdigest()
        exists = self.session.query(Reference).filter_by(id=ref['id']).first()
        if not exists:
            reference = Reference(id=ref['id'], url=ref['url'], ref=ref['ref'])
            self.session.add(reference)
            print("added reference from: " + ref['url'] + " to: " + ref['ref'])
        else:
            print("reference already exists in database")
        self.session.commit()

    def insert_person(self, person):
        exists = self.session.query(Reference).filter_by(name=person['name']).first()
        if not exists:
            person = Person(name=person['name'])
            self.session.add(person)
            print("added: " + person['name'] + " to database")
        else:
            print("person already exists in database")
        self.session.commit()

    def insert_article_person(self, ref):
        sha_id = hashlib.sha1(bytes(ref['url'] + ref['name'], 'utf-8'))
        ref['id'] = sha_id.hexdigest()
        exists = self.session.query(Reference).filter_by(id=ref['id']).first()
        if not exists:
            relation = ArticlePeople(id=ref['id'],
                                     article=ref['url'],
                                     person=ref['name'],
                                     count=ref['count'],
                                     main_person=ref['main'])
            self.session.add(relation)
            print("added relation from: " + ref['url'] + " to: " + ref['name'])
        else:
            print("relation already exists in database")
        self.session.commit()

    def commit(self):
        self.session.commit()
