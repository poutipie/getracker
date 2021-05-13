import sys, pdb;

class Commons:

    _OSRS_API = "http://services.runescape.com/m=itemdb_oldschool/api"
    _OSRS_WIKI_API = "https://prices.runescape.wiki/api/v1/osrs/"

    def pdb() -> pdb.Pdb:
        return pdb.Pdb(stdout=sys.__stdout__)
