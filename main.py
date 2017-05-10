#! python3

from indexer import Indexer
from scraper import scrape

# index = Indexer(2010, 11, 10, local=False, save=True)
# index.bp_index()
wtd = "please crawl: people, organisations and locations"
scrape(58, -1, True, False, wtd)
