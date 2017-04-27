from database_utils import DBSession
from database import *
from utils import ProgressBar


db = DBSession()
dbs = db.session


def run_operations():
    check_popularity()


def check_popularity():
    people = dbs.query(Person).all()
    pb = ProgressBar(people.__len__())

    for person in people:
        pb.update_print(people.index(person))
        references = dbs.query(PeopleRel.count).filter(PeopleRel.person == person.name).all()
        count = sum(i[0] for i in references)
        person.count = int(count)
    dbs.commit()


run_operations()
