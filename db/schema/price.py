from typing import NamedTuple, Any
from sqlite3 import Connection

class Price(NamedTuple):
    id: int
    high: int
    high_time: int
    low: int
    low_time: int
    item_id: int


    @staticmethod
    def migrate(price_data: tuple) -> tuple:
        
        try:
            migration: tuple = (
                price_data[1]['high'],
                price_data[1]['highTime'],
                price_data[1]['low'],
                price_data[1]['lowTime'],
                int(price_data[0])
            )
            return migration
        except KeyError as ex:
            import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

    @staticmethod
    def insert(price_data: tuple, db: Connection):

        price_mig: tuple = Price.migrate(price_data)
        cursor = db.cursor()
        sql = (
            "INSERT INTO Price "
            " (high, high_time, low, low_time, item_id) "
            " VALUES(?, ?, ?, ?, ?)"
        )
        cursor.execute(sql, price_mig)

class PriceIndexTime(NamedTuple):

    id: int
    indexed_at: str


    @staticmethod
    def insert(db: Connection):

        cursor = db.cursor()

        sql = (
            " INSERT INTO PriceIndexTime "
            " (indexed_at) "
            " VALUES(CURRENT_TIMESTAMP) "
        )

        cursor.execute(sql)

