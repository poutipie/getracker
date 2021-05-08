import sqlite3
import sys
import os
from datetime import datetime, timedelta
from typing import Optional

from .schema.item import Item, ItemIndexMeta
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

        cur = db.cursor()
        cur.execute("SELECT * FROM ItemIndexMeta")
        meta_data = cur.fetchall()

        time_diff: Optional[timedelta] = None
        if meta_data:
            f = '%Y-%m-%d %H:%M:%S'
            utc_then = datetime.strptime(meta_data[0][1], f)
            utc_now = datetime.utcnow()
            time_diff = (utc_now - utc_then)

        reindex_interval = timedelta(hours=3)
        if time_diff is None or time_diff >= reindex_interval:

            cur.execute("DELETE FROM Item WHERE True")
            cur.execute("DELETE FROM ItemIndexMeta WHERE True")

            items_json = WikiEndpoint.fetch_items()
            for item in items_json:
                Item.insert(item, db)
            ItemIndexMeta.insert(db)
            db.commit()
