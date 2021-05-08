from typing import NamedTuple
from sqlite3 import Connection

class Volume(NamedTuple):
    id: int
    volume: int
    item_id: int

    @staticmethod
    def insert(item_id: int, volume: int, db: Connection):

        cursor = db.cursor()

        sql = (
            "INSERT INTO Volume "
            " (volume, item_id) "
            " VALUES(?, ?)"
        )

        cursor.execute(sql, (volume, item_id))

class VolumeIndexTime(NamedTuple):

    id: int
    indexed_at: str


    @staticmethod
    def insert(db: Connection):

        cursor = db.cursor()
        sql = (
            " INSERT INTO VolumeIndexTime "
            " (indexed_at) "
            " VALUES(CURRENT_TIMESTAMP) "
        )

        cursor.execute(sql)