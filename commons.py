import requests
from .db.database import Database
from sqlite3 import Connection

class Commons:

    _OSRS_API = "http://services.runescape.com/m=itemdb_oldschool/api"
    _OSRS_WIKI_API = "https://prices.runescape.wiki/api/v1/osrs/"

    _DB = Database()
    Database.init_schema(_DB.get_db())
    Database.reindex_osrs_wiki(_DB.get_db())
