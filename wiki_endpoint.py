import requests

class WikiEndpoint():

    _OSRS_WIKI_API = "https://prices.runescape.wiki/api/v1/osrs/"

    _SESSION = requests.Session()
    _SESSION.headers = {
        'User-Agent': 'GETrackApp/0.1',
        'From': 'pietari.poutiainen@gmail.com'
    }

    @staticmethod
    def session():
        return WikiEndpoint._SESSION
    

    @staticmethod
    def fetch_items():

        url: str = "{}/{}".format(WikiEndpoint._OSRS_WIKI_API, "mapping")
        return WikiEndpoint.session().get(url).json()

    @staticmethod
    def fetch_volumes():

        url: str = "{}/{}".format(WikiEndpoint._OSRS_WIKI_API, "volumes")
        return WikiEndpoint.session().get(url).json()['data']

    @staticmethod
    def fetch_high_low_data(id: int):
        
        latest_ep: str = "{}/{}".format(WikiEndpoint._OSRS_WIKI_API, "latest")
        url: str = "{}?id={}".format(latest_ep, id)

        return WikiEndpoint.session().get(url).json()['data'][str(id)]