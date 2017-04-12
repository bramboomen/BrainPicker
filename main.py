#! python3

from indexer import Indexer
from crawler import crawl

# index = Indexer(2010, 11, 10, local=False, save=True)
# index.bp_index()
wtd = "please crawl: people, organisations and locations"
crawl(58, -1, True, False, wtd)
