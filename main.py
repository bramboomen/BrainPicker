#! python3

from indexer import Indexer
from scraper import scrape
import datetime as dt
from database_utils import DBSession
from database_optimalisation import optimize_my_database as optimize
from database_operations import run_operations as operate
from database import LastRun
from ner import NERserver

dbs = DBSession().session
ner_server = NERserver()


# date = dbs.query(LastRun.date).order_by(LastRun.id.desc()).first()[0]
date = dt.date(year=2009, month=1, day=1)
print("Indexing...", end="", flush=True)
index = Indexer(date, local=True)
index.bp_index()
print(" finished!")

ner_server.start()
print("Scraping...", end="", flush=True)
scrape(date, what_to_do="references people", local=True)
ner_server.stop()
print(" finished!")

print("Optimizing...", end="", flush=True)
optimize()
operate()
print(" finished!")

dbs.add(LastRun(date=dt.date.today()))
dbs.commit()

print("Done")
