import requests
from bs4 import BeautifulSoup
import json
import time


class RankingCapture:
    def __init__(self, ranking_url="/ranking_jugadores.asp?Cod_Cat=", category="TN",
                 root_url="http://www.fatm.com.es/"):
        self._root_url = root_url
        self._category = category
        self._ranking_url = root_url + ranking_url + category
        self._players = []
        self._ranking_html = None
        self._games = []

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        self._players = value

    @property
    def games(self):
        return self._games

    @games.setter
    def games(self, value):
        self._games = value

    def load_ranking(self):
        ranking_raw_html = requests.get(self._ranking_url)
        self._ranking_html = BeautifulSoup(ranking_raw_html.content, 'html.parser')

    def process_players(self):
        lines_number = 1
        for html_line in self._ranking_html.find_all('tr'):
            if lines_number > 1:
                player = {}
                field_count = 1
                for html_field in html_line.find_all('td'):
                    if field_count == 2:
                        player['link'] = html_field.a.get('href')
                        player['nombre'] = " ".join(html_field.get_text().split())
                    elif field_count == 3:
                        player['club'] = " ".join(html_field.get_text().split())
                    elif field_count == 4:
                        player['grupo'] = " ".join(html_field.get_text().split())
                    elif field_count == 5:
                        player['partidos_jugados'] = " ".join(html_field.get_text().split())
                    elif field_count == 6:
                        player['partidos_ganados'] = " ".join(html_field.get_text().split())
                    elif field_count == 7:
                        player['partidos_perdidos'] = " ".join(html_field.get_text().split())
                    elif field_count == 8:
                        player['puntos'] = " ".join(html_field.get_text().split())
                    field_count = field_count + 1
                self.players.append(player)
            lines_number = lines_number + 1

    def process_games(self):
        for player in self.players:
            table_count = 1
            games_html = BeautifulSoup(requests.get(self._root_url + player['link']).content, 'html.parser')
            player_games = []
            for games_line in games_html.find_all('tr'):
                if table_count > 0:
                    game = {}
                    game_number = 1
                    for field in games_line.find_all('td'):
                        if game_number == 1:
                            game['jugador1'] = " ".join(field.get_text().split())
                        elif game_number == 2:
                            game['puntuacion_jugador1'] = " ".join(field.get_text().split())
                        elif game_number == 3:
                            game['jugador2'] = " ".join(field.get_text().split())
                        elif game_number == 4:
                            game['puntuacion_jugador2'] = " ".join(field.get_text().split())
                        elif game_number == 5:
                            game['jornada'] = " ".join(field.get_text().split())
                        elif game_number == 6:
                            date_string = " ".join(field.get_text().split())
                            # Fix for 00 day in date from fatm
                            if len(date_string) == 9:
                                date_string = '1' + date_string
                            game['fecha'] = date_string
                        game_number = game_number + 1
                    player_games.append(game)
                    self.games.append(game)
                table_count = table_count + 1
            player['partidos'] = player_games

    def save_players(self):
        with open('players_' + self._category + '_' + str(int(time.time())) + '.json', 'w') as file_out:
            json.dump(self.players, file_out, ensure_ascii=False)

    def save_games(self):
        with open('games_' + self._category + '_' + str(int(time.time())) + '.json', 'w') as file_out:
            json.dump(self.games, file_out, ensure_ascii=False)

    def load_players(self, players_file):
        with open(players_file, "r") as read_file:
            self.players = json.load(read_file)

    def load_games(self, games_file):
        with open(games_file, "r") as read_file:
            self.games = json.load(read_file)


if __name__ == "__main__":
    ranking_tn = RankingCapture()
    ranking_tn.load_ranking()
    ranking_tn.process_players()
    ranking_tn.process_games()
    ranking_tn.save_players()
    ranking_tn.save_games()

    # ranking_tn.load_games('games_TN_1580834889.json')
    # ranking_tn.load_players('players_TN_1580834658.json')


