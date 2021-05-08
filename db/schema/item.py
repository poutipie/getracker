from typing import NamedTuple
from sqlite3 import Connection

class Item(NamedTuple):
    id: int
    name: str
    examine: str
    value: int
    icon: str
    ge_limit: int
    members: int
    low_alch: int
    high_alch: int


    @staticmethod
    def migrate(item_json: dict):

        assert 'id'       in item_json, "Item::Migrate:: no 'id' attr."
        assert 'name'     in item_json, "Item::Migrate:: no 'name' attr."
        assert 'examine'  in item_json, "Item::Migrate:: no 'examine' attr."
        assert 'value'    in item_json, "Item::Migrate:: no 'value' attr."
        assert 'icon'     in item_json, "Item::Migrate:: no 'icon' attr."
        assert 'members'  in item_json, "Item::Migrate:: no 'members' attr."

        if 'limit' not in item_json:
            item_json['limit'] = 0
        if 'lowalch' not in item_json:
            item_json['lowalch'] = 0
        if 'highalch' not in item_json:
            item_json['highalch'] = 0

        item_json['members'] = int(item_json['members'])

        return Item(
            id =       item_json['id'],
            name =     item_json['name'],
            examine =  item_json['examine'],
            value=     item_json['value'],
            icon=      item_json['icon'],
            ge_limit=  item_json['limit'],
            members=   item_json['members'],
            low_alch=  item_json['lowalch'],
            high_alch= item_json['highalch']
        )

    @staticmethod
    def insert(item_json: dict, db: Connection):

        item: Item = Item.migrate(item_json)

        cursor = db.cursor()

        sql = (
            "INSERT INTO Item "
            " (id, name, examine, value, icon, ge_limit, members, low_alch, high_alch) "
            " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )

        cursor.execute(sql, item)

class ItemIndexTime(NamedTuple):

    id: int
    indexed_at: str


    @staticmethod
    def insert(db: Connection):

        cursor = db.cursor()

        sql = (
            " INSERT INTO ItemIndexTime "
            " (indexed_at) "
            " VALUES(CURRENT_TIMESTAMP) "
        )

        cursor.execute(sql)
