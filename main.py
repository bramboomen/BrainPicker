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
index = Indexer(date, local=True)
index.bp_index()
ner_server.start()
scrape(date, what_to_do="references people", local=True)
ner_server.stop()
optimize()
operate()

dbs.add(LastRun(date=dt.date.today()))
dbs.commit()
