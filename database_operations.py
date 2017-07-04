from database_utils import DBSession
from database import *
from utils import ProgressBar
from sqlalchemy import or_, and_


db = DBSession()
dbs = db.session


def run_operations():
    link_people()
    # check_popularity()


def check_popularity():
    people = dbs.query(Person).all()
    pb = ProgressBar(people.__len__())

    for person in people:
        pb.update_print(people.index(person))
        references = dbs.query(PeopleRel.count).filter(PeopleRel.person == person.name).all()
        count = sum(i[0] for i in references)
        person.count = int(count)
    dbs.commit()


def link_people():
    articles = dbs.query(Article.url).all()
    pb = ProgressBar(articles.__len__())
    for article in articles:
        pb.update_print(articles.index(article))
        people = dbs.query(PeopleRel.person).filter(PeopleRel.article == article[0]).all()
        people = [x[0] for x in people]
        people_rel = []
        for x in range(people.__len__()):
            for y in range(x+1, people.__len__()):
                people_rel.append([people[x],people[y]])
        for rel in people_rel:
            p1, p2 = rel[0], rel[1]
            a = dbs.query(PersonRel).filter(or_(and_(PersonRel.person1 == p1, PersonRel.person2 == p2),
                                                and_(PersonRel.person1 == p2, PersonRel.person2 == p1))).first()
            if a:
                a.count += 1
            else:
                dbs.add(PersonRel(person1=p1, person2=p2, count=1))
        dbs.commit()



run_operations()
