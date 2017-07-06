from database import Person
from database_utils import DBSession
from wiki_db import WikiDB

db = DBSession()
dbs = db.session
wiki = WikiDB()

people = dbs.query(Person).filter(Person.verified == 1).all()
failed = []
succeeded = []
for p in people:
    name = p.name.encode("latin-1", "replace")
    if wiki.text_from_page(name.decode("latin-1")) == "empty":
        failed.append(p.name)
    else:
        succeeded.append(p.name)
for p in failed:
    print(p)
print("Failed: " + str(failed.__len__()) + " out of: " + str(people.__len__()))
print("Success: " + str(succeeded.__len__()) + " out of: " + str(people.__len__()))
