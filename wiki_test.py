import re
from database import Person
from database_utils import DBSession
from wiki_db import WikiDB

db = DBSession()
dbs = db.session
wiki = WikiDB()

# people = dbs.query(Person).filter(Person.verified == 1).all()
people = dbs.query(Person).all()
failed = []
succeeded = []
failed_again = []
for p in people:
    name = p.name.encode("latin-1", "replace")
    if wiki.text_from_page(name.decode("latin-1")) == "empty":
        failed.append({"name": p.name, "count": p.count})
    else:
        succeeded.append({"name": p.name, "count": p.count})

for p in failed:
    if p["name"] == "C.S. Lewis":
        bram = " "
    name = p["name"].encode("latin-1", "replace")
    name = name.decode("latin-1")
    name = re.sub(r'(\.(?! ))', r'\1 ', name)
    name = name.replace(" ", "_")
    stmnt = "select * from redirect \
             where rd_title = %r and rd_namespace = 0" % name
    result = wiki.query(stmnt)
    if not result:
        failed_again.append(p)
    else:
        succeeded.append(p)

sorted_failed = sorted(failed_again, key=lambda k: k['count'])
x = 0
for p in sorted_failed:
    if p["count"] >= 10:
        x += 1
        print(str(p["count"]) + " - " + p["name"])

print("Failed: " + str(failed.__len__()) + " out of: " + str(people.__len__()))
print("Failed again: " + str(failed_again.__len__()) + " out of: " + str(failed.__len__()))
print("Important Fails: " + str(x) + " out of: " + str(failed_again.__len__()))
print("Success: " + str(succeeded.__len__()) + " out of: " + str(people.__len__()))
