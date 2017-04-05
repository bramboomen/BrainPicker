#! python3

from indexer import Indexer
from crawler import crawl

# index = Indexer(2010, 11, 10, local=False, save=True)
# index.bp_index()
crawl(0, -1, False, True)