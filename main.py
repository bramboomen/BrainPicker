#! python3

from indexer import Indexer


def index(start_year, start_month, start_day, local, save):
    Indexer(start_year, start_month, start_day, local, save)
