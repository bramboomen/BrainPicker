#! python3

from crawler import *
from indexer import *
import sys


bp = "https://www.brainpickings.org/2017/03/01/mary-ruefle-madness-rack-and-honey-prayer/"


def crawl_test():
    local = True
    save = False
    crawl(local, save)


def index_test():
    indexer = Indexer(2017, 3, 21, local=False, save=True)
    indexer.bp_index()


crawl_test()
# index_test()
