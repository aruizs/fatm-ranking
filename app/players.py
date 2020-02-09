from .ranking_capture import RankingCapture
import datetime as dt
import json
from .scoring import BasicScoring, EloScoring


class Players:
    def __init__(self, players, games):
        self._players = players
        self._games = games

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

    def sort_games_by_date(self):
        for game in self.games:
            game['fecha'] = dt.datetime.strptime(game['fecha'], '%d/%m/%Y')

        self.games = sorted(self.games, key=lambda x: x['fecha'], reverse=False)

    def remove_duplicate_games(self):
        not_repeated_games = []
        for game in self.games:
            if game not in not_repeated_games:
                not_repeated_games.append(game)
        self.games = not_repeated_games

    def is_repeated_players(self):
        not_repeated_players = []
        for player in self.players:
            if player not in not_repeated_players:
                not_repeated_players.append(player)

        done = set()
        for player in self.players:
            if player['nombre'] not in done:
                done.add(player['nombre'])
            else:
                print("Duplicated player based on name ", player['nombre'])
        return len(not_repeated_players) != len(self.players)

    def scoring(self):
        for game in self.games:
            winner_player = 1
            if int(game['puntuacion_jugador1']) < int(game['puntuacion_jugador2']):
                winner_player = 2

            player1 = next((player for player in self.players if player["nombre"] == game['jugador1']), None)
            player2 = next((player for player in self.players if player["nombre"] == game['jugador2']), None)

            scoring_algorithm = EloScoring()
            inc_score1, inc_score2 = scoring_algorithm.calculate(player1.get("score", 0), player2.get("score", 0),
                                                                 winner_player)

            player1["score"] = inc_score1
            player2["score"] = inc_score2

        self.players = sorted(self.players, key=lambda k: (k.get("score", 0),  -int(k.get("partidos_perdidos", "0"))),
                              reverse=True)

    def save(self):
        for player in self.players:
            del player['partidos']
            del player['grupo']

        with open('players_scoring.json', 'w') as file_out:
            json.dump(self.players, file_out, ensure_ascii=False)


if __name__ == "__main__":
    ranking_tn = RankingCapture()
    ranking_tn.load_games('games_TN_1580841079.json')
    ranking_tn.load_players('players_TN_1580841078.json')

    players_tn = Players(ranking_tn.players, ranking_tn.games)
    players_tn.sort_games_by_date()
    print(len(players_tn.games))
    players_tn.remove_duplicate_games()
    print(len(players_tn.games))
    print(players_tn.is_repeated_players())
    players_tn.scoring()
    players_tn.save()
