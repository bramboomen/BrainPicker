from database_utils import DBSession
from database import *
from sqlalchemy import func
from sqlalchemy.sql import collate
from sqlalchemy.orm import sessionmaker
import wikipedia as wiki
from utils import ProgressBar
from sandbox.dbpedia import Name
import os

db = DBSession()
dbs = db.session

engine = create_engine('sqlite:///names.db')
db_session = sessionmaker(bind=engine)
ndbs = db_session()


def optimize_my_database():
    print("Optimize one-offs")
    delete_one_offs()

    print("Optimize too-longs")
    delete_five_or_more()

    print("Optimize duplication")
    fix_name_duplication()
    fix_case_duplication()

    print("Optimize not-letters")
    fix_symbols()

    print("Fix link-errors")
    #link_errors()

    print("Verify")
    verify_all_with_dbpedia()


def link_errors():
    # Find all links that do not start with "https://www" and change them to the correct link
    wrong_links = ["http://www.brain", "www.brain", "https://brain", "http://brain", " https://www.brain"]
    for wrong_link in wrong_links:
        references = dbs.query(Reference).filter(Reference.ref.like(wrong_link + "%")).all()
        for reference in references:
            reference.ref = reference.ref.replace(wrong_link, "https://www.brain")
    dbs.commit()
    # Any wrong links left get deleted
    # wrong_references = dbs.query(Reference).filter(Reference.ref.notlike("https://www.brain")).all()
    # for wrong_reference in wrong_references:
    #     dbs.delete(wrong_reference)
    # dbs.commit()


def fix_symbols():
    # Find people with non-letters in the name
    not_letters = ["--", "?", "''", "`", "\\"]
    for not_letter in not_letters:
        people = dbs.query(Person).filter(Person.name.like("%" + not_letter + "%"))
        for person in people:
            name = person.name.replace(not_letter, "").strip()
            if dbs.query(Person).filter(Person.name == name).first():
                dbs.delete(person)
            else:
                person.name = name
        dbs.commit()


def delete_one_offs():
    # Find all people with singleton names who get referenced < 5 times
    # These are most likely not persons
    people = dbs.query(Person).filter(Person.name.notlike("% %")).all()
    pb = ProgressBar(people.__len__())

    for person in people:
        pb.update_print(people.index(person))
        references = dbs.query(PeopleRel.count).filter(PeopleRel.person == person.name).all()
        count = sum(i[0] for i in references)
        if count < 5:
            dbs.delete(person)
    dbs.commit()


def delete_five_or_more():
    # Find all people with four or more name-parts and delete them
    # These are most likely mistakes
    people = dbs.query(Person).filter(Person.name.like("% % % % %")).all()
    for person in people:
        dbs.delete(person)
    dbs.commit()


def fix_name_duplication():
    # Find names which got duplicated and fix them
    # Like: 'Albert Einstein Albert Einstein'
    people = dbs.query(Person).filter(Person.name.like("% % % %")).all()
    for person in people:
        split = person.name.split()
        if split.__len__() == 4:
            if split[0].lower() == split[2].lower() and split[1].lower() == split[3].lower():
                name = split[2] + " " + split[3]
                wrong_duplicate = dbs.query(PeopleRel).filter(PeopleRel.person == person.name).first()
                correct_duplicate = dbs.query(PeopleRel).filter(PeopleRel.person == name).first()
                if correct_duplicate:
                    if correct_duplicate.article == wrong_duplicate.article:
                        correct_duplicate.count += wrong_duplicate.count
                        dbs.delete(wrong_duplicate)
                    else:
                        wrong_duplicate.person = name
                    dbs.delete(person)
                else:
                    person.name = name
                dbs.commit()


def fix_case_duplication():
    # Find duplications based on case
    people = dbs\
        .query(Person.name, func.count(Person.name))\
        .group_by(collate(Person.name, 'NOCASE'))\
        .having(func.count(Person.name) > 1)\
        .all()
    for p in people:
        merge_person(p.name)


def merge_person(name):
    name = name.title()
    people = dbs.query(Person).filter(func.lower(Person.name) == func.lower(name)).all()
    count = 0
    verified = False
    for person in people:
        count = count + person.count if person.count else count
        if person.verified:
            verified = True
    person = people[0]
    del people[0]
    for p in people:
        dbs.delete(p)
    dbs.commit()
    person.name = name
    person.count = count
    person.verified = verified
    dbs.commit()


def verify_all_with_dbpedia():
    people = dbs.query(Person).filter(Person.verified == None).all()
    pb = ProgressBar(people.__len__())

    for person in people:
        pb.update_print(people.index(person))
        verified = verify_with_dbpedia(person.name)
        if verified:
            person.verified = True
        else:
            person.verified = False
    dbs.commit()


def verify_with_dbpedia(name):
    result = ndbs.query(Name).filter(Name.name.contains(name)).first()
    if result:
        return True
    else:
        return False


def verify_all_with_wikipedia():
    people = dbs.query(Person).all()
    pb = ProgressBar(people.__len__())
    threshold = 1000

    for person in people:
        pb.update_print(people.index(person))
        name, count = verify_with_wikipedia(person.name, threshold)
        if name and count < threshold:
            person.verified = True
    dbs.commit()


def verify_with_wikipedia(name, threshold):
    # Search wikipedia, return true if first result is the same as the name
    search = wiki.search(name, results=int(threshold/2))
    if search:
        if search[0].lower() == name.lower():
            return True, wiki_search_counter(name, search)
    return False, 0


def wiki_search_counter(name, search):
    counter = 0
    multiplier = name.split().__len__()
    for item in search:
        if all(word in item for word in name.split()):
            counter += 10/multiplier
        elif any(word in item for word in name.split()):
            counter += 1
    return counter

def delete_list():
    # Delete selected list of articles
    lijst = []

    # Dit kan nog ietsje mooier
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/delete_list.txt", "r") as delete_list:
        for line in delete_list:
            lijst.append(line.rstrip('\n'))
    for link in lijst:
        article = dbs.query(Article).filter(Article.url == link).first()
        refurl = dbs.query(Reference).filter(Reference.url == link).all()
        ref = dbs.query(Reference).filter(Reference.ref == link).all()
        people = dbs.query(PeopleRel).filter(PeopleRel.article == link).all()



        if article:
            dbs.delete(article)
            dbs.commit()
        if refurl:
            for reference in refurl:
                dbs.delete(reference)
            dbs.commit()
        if ref:
            for reference in ref:
                dbs.delete(reference)
            dbs.commit()
        if people:
            for person in people:
                dbs.delete(person)
            dbs.commit()





