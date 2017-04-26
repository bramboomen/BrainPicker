from database_utils import DBSession
from database import *
import wikipedia as wiki


db = DBSession()
dbs = db.session


def optimize_my_database():
    # print("Optimize one-offs")
    # delete_one_offs()
    # print("Finished one-offs")
    # print("Optimize too-longs")
    # remove_five_or_more_name()
    # print("Finished too-longs")
    # print("Optimize duplication")
    # fix_name_duplication()
    # print("Finished duplication")
    # print("Optimize not-letters")
    # fix_not_letters_in_name()
    # print("Finished not-letters")
    print("Verify")
    verify_all_with_wikipedia()
    print("Finished Verification")


def remove_five_or_more_name():
    # Find all people with four or more name-parts and delete them
    # These are most likely mistakes
    people = dbs.query(Person).filter(Person.name.like("% % % % %")).all()
    for person in people:
        dbs.delete(person)
    dbs.commit()


def fix_not_letters_in_name():
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
    people = dbs.query(Person).filter(Person.name.notlike("% %")).limit(500)
    for person in people:
        references = dbs.query(PeopleRel.count).filter(PeopleRel.person == person.name).all()
        count = sum(i[0] for i in references)
        if count < 5:
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


def verify_all_with_wikipedia():
    people = dbs.query(Person).all()
    length = people.__len__()
    print(str(length))
    progress = 0

    for person in people:
        progress += 1
        print(str(progress))
        if progress % int(length/100) == 0:
            print(str(int(progress / length * 100)) + "%")
        name, count = verify_with_wikipedia(person.name)
        if name and count < 1000:
            person.verified = True

    dbs.commit()


def verify_with_wikipedia(name):
    # Search wikipedia, return true if first result is the same as the name
    search = wiki.search(name, results=500)
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


optimize_my_database()
