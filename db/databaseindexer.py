from threading import Event, Thread, Timer

import sqlite3
from .database import Database

class DatabaseIndexerThread(Thread):

    def __init__(self, event):
        Thread.__init__(self)
        self.event = event
        self.init_db()
        self.reindex_osrs_wiki()

    def run(self):
        print("DatabaseIndexerThread:: Start!")
        while not self.event.wait(timeout=15.0):
            self.reindex_osrs_wiki()
        print("DatabaseIndexerThread:: Done!")
    
    def init_db(self):
        db = Database.connect()
        Database.init_schema(db)
        Database.disconnect(db)


    def reindex_osrs_wiki(self):

        db = Database.connect()

        if Database.osrs_items_reindex_needed(db):
            print("DatabaseIndexerThread:: Re-indexing Items..")
            Database.reindex_osrs_items(db)
            print("DatabaseIndexerThread:: Items Re-indexed")

        if Database.osrs_volumes_reindex_needed(db):
            print("DatabaseIndexerThread:: Re-indexing Volumes..")
            Database.reindex_osrs_volumes(db) 
            print("DatabaseIndexerThread:: Volumes Re-indexed")

        if Database.osrs_prices_reindex_needed(db):
            print("DatabaseIndexerThread:: Re-indexing prices")
            Database.reindex_osrs_prices(db)
            print("DatabaseIndexerThread:: Prices Re-indexed")

        Database.disconnect(db)

class DatabaseIndexer():

    def __init__(self):

        self.indexer = None
        self.indexer_event = None

        self.indexer_event = Event()
        self.indexer = DatabaseIndexerThread(self.indexer_event)
        self.indexer.start()

    def __del__(self):
        
        if self.indexer_event is not None:
            self.indexer_event.set()

        if self.indexer is not None:
            self.indexer.join()