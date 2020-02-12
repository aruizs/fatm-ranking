from .ranking_capture import RankingCapture
from .players import Players
from enum import Enum


class Category(Enum):
    TN = 1
    SDA = 2
    DHA = 3


class Ranking:
    def __init__(self, category):
        self._ranking = None
        self._players = None
        self._ranking_urls = []
        self._category = category
        self._root_urls = []
        if category == Category.DHA:
            self._ranking_urls = ["/ranking_jugadores.asp?Cod_Cat="]
            self._root_urls = ["http://www.fatm.com.es/", "http://www.fatm.com.es/2019-2020_1_ronda/"]
        elif category == Category.SDA:
            self._ranking_urls = ["/ranking_jugadores.asp?Cod_Cat="]
            self._root_urls = ["http://www.fatm.com.es/", "http://www.fatm.com.es/2019-2020_1_ronda/"]
        elif category == Category.TN:
            self._ranking_urls = ["/ranking_jugadores.asp?Cod_Cat="]
            self._root_urls = ["http://www.fatm.com.es/"]

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        self._players = value

    @property
    def ranking(self):
        return self._players

    @ranking.setter
    def ranking(self, value):
        self._ranking = value

    def load(self):
        self._ranking = RankingCapture(self._ranking_urls, self._category.name, self._root_urls)
        self._ranking.load_ranking()
        self._ranking.process_players()
        self._ranking.process_games()

        self._players = Players(self._ranking.players, self._ranking.games)
        self._players.sort_games_by_date()
        self._players.remove_duplicate_games()
        self._players.is_repeated_players()
        self._players.scoring()
        self._players.join_duplicated_players()