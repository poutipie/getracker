import sqlite3
import sys
import os
from datetime import datetime, timedelta
from typing import Optional

from .schema.item import Item, ItemIndexTime
from .schema.volume import Volume, VolumeIndexTime
from .schema.price import Price, PriceIndexTime
from ..wiki_endpoint import WikiEndpoint

class Database():

    _DB_DIR = os.path.dirname(os.path.abspath(__file__))
    _DATA_DIR = os.path.join(_DB_DIR, 'data')
    _SCHEMA_DIR = os.path.join(_DB_DIR, 'schema')

    _DB_FILE = os.path.join(_DATA_DIR, 'database.db')
    _SCHEMA_FILE =  os.path.join(_SCHEMA_DIR, "schema.sql")

    @staticmethod
    def connect() -> sqlite3.Connection:

        db = sqlite3.Connection = None
        db = sqlite3.connect(Database._DB_FILE)
        return db
    
    @staticmethod
    def disconnect(db: sqlite3.Connection) -> None:

        db.close()
        db = None

    @staticmethod
    def init_schema(db: sqlite3.Connection):

        cursor: sqlite3.Cursor = db.cursor()

        schema_txt = ""
        with open(Database._SCHEMA_FILE, "r") as schema_f:
            schema_txt = schema_f.read()
        cursor.executescript(schema_txt)
        db.commit()

    @staticmethod
    def osrs_prices_reindex_needed(db: sqlite3.Connection) -> bool:
        cur = db.cursor()
        cur.execute("SELECT * FROM PriceIndexTime")
        _idx_t = cur.fetchall()

        t_since = None if not _idx_t else Database.time_since(_idx_t[0][1])
        item_interval = timedelta(minutes=2)

        return not t_since or len(_idx_t) > 1 or t_since >= item_interval

    @staticmethod
    def reindex_osrs_prices(db: sqlite3.Connection):

        cur = db.cursor()
        cur.execute("DELETE FROM Price WHERE TRUE")
        cur.execute("DELETE FROM PriceIndexTime WHERE TRUE")

        prices_json = WikiEndpoint.fetch_latest_prices()

        for price_data in prices_json.items():
            Price.insert(price_data, db)
        
        PriceIndexTime.insert(db)
        db.commit()


    @staticmethod
    def osrs_items_reindex_needed(db: sqlite3.Connection) -> bool:

        cur = db.cursor()
        cur.execute("SELECT * FROM ItemIndexTime")
        _idx_t = cur.fetchall()

        t_since = None if not _idx_t else Database.time_since(_idx_t[0][1])
        item_interval = timedelta(hours=3)

        return not t_since or len(_idx_t) > 1 or t_since >= item_interval

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
        _idx_t = cur.fetchall()

        t_since = None if not _idx_t else Database.time_since(_idx_t[0][1])
        vol_interval = timedelta(hours=6)
        return not _idx_t or len(_idx_t) > 1 or t_since >= vol_interval

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


    @staticmethod
    def time_since(utc_then_timestamp: Optional[str]):

        if utc_then_timestamp is None:
            return None

        f = '%Y-%m-%d %H:%M:%S'
        utc_then = datetime.strptime(utc_then_timestamp, f)
        utc_now = datetime.utcnow()
        return (utc_now - utc_then)
