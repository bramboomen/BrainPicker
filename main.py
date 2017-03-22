#! python3

from indexer import Indexer


index = Indexer(2010, 11, 10, local=False, save=True)
index.bp_index()
