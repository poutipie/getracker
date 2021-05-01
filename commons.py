import requests

class Commons:

    _OSRS_API = "http://services.runescape.com/m=itemdb_oldschool/api"
    _OSRS_WIKI_API = "https://prices.runescape.wiki/api/v1/osrs/"

    _SESSION = requests.Session()
    _SESSION.headers = {
        'User-Agent': 'GETrackApp/0.1',
        'From': 'pietari.poutiainen@gmail.com'
    }

    @staticmethod
    def session():
        return Commons._SESSION
