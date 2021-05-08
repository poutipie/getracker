import sqlite3
import sys
import os
from datetime import datetime, timedelta
from typing import Optional

from .schema.item import Item, ItemIndexTime
from .schema.volume import Volume, VolumeIndexTime
from ..wiki_endpoint import WikiEndpoint

class Database():

    _DB_DIR = os.path.dirname(os.path.abspath(__file__))
    _DATA_DIR = os.path.join(_DB_DIR, 'data')
    _SCHEMA_DIR = os.path.join(_DB_DIR, 'schema')

    _DB_FILE = os.path.join(_DATA_DIR, 'database.db')
    _SCHEMA_FILE =  os.path.join(_SCHEMA_DIR, "schema.sql")

    def __init__(self):

        self._conn: sqlite3.Connection = None
        self._conn = sqlite3.connect(Database._DB_FILE)

    def __del__(self):

        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def get_db(self) -> sqlite3.Connection:

        return self._conn
    

    @staticmethod
    def init_schema(db: sqlite3.Connection):

        cursor: sqlite3.Cursor = db.cursor()

        schema_txt = ""
        with open(Database._SCHEMA_FILE, "r") as schema_f:
            schema_txt = schema_f.read()
        cursor.executescript(schema_txt)
        db.commit()


    @staticmethod
    def reindex_osrs_wiki(db: sqlite3.Connection):

        if Database.osrs_items_reindex_needed(db):
            Database.reindex_osrs_items(db)

        if Database.osrs_volumes_reindex_needed(db):
            Database.reindex_osrs_volumes(db) 

    @staticmethod
    def osrs_items_reindex_needed(db: sqlite3.Connection) -> bool:

        cur = db.cursor()
        cur.execute("SELECT * FROM ItemIndexTime")
        item_idx_t = cur.fetchall()

        t_since: Optional[timedelta] = None
        if item_idx_t:
            f = '%Y-%m-%d %H:%M:%S'
            utc_then = datetime.strptime(item_idx_t[0][1], f)
            utc_now = datetime.utcnow()
            t_since = (utc_now - utc_then)

        item_interval = timedelta(hours=3)

        return not t_since or len(item_idx_t) > 1 or t_since >= item_interval

    @staticmethod
    def reindex_osrs_items(db: sqlite3.Connection):
        
        cur = db.cursor()

        cur.execute("DELETE FROM Item WHERE True")
        cur.execute("DELETE FROM ItemIndexTime WHERE True")

        items_json = WikiEndpoint.fetch_items()
        for item in items_json:
            Item.insert(item, db)
        ItemIndexTime.insert(db)
        db.commit()

    @staticmethod
    def osrs_volumes_reindex_needed(db: sqlite3.Connection) -> bool:
        
        cur = db.cursor()
        cur.execute("SELECT * FROM VolumeIndexTime")
        vol_idx_t = cur.fetchall()

        t_since: Optional[timedelta] = None
        if vol_idx_t:
            f = '%Y-%m-%d %H:%M:%S'
            utc_then = datetime.strptime(vol_idx_t[0][1], f)
            utc_now = datetime.utcnow()
            t_since = (utc_now - utc_then)

        vol_interval = timedelta(hours=6)

        return not vol_idx_t or len(vol_idx_t) > 1 or t_since >= vol_interval

    @staticmethod
    def reindex_osrs_volumes(db: sqlite3.Connection):

        cur = db.cursor()

        cur.execute("DELETE FROM Volume WHERE True")
        cur.execute("DELETE FROM VolumeIndexTime WHERE True")

        volumes_json = WikiEndpoint.fetch_volumes()
        for item_id, volume in volumes_json.items():
            Volume.insert(int(item_id), volume, db)
        VolumeIndexTime.insert(db)
        db.commit()
