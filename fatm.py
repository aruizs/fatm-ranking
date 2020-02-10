from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from app.ranking_capture import RankingCapture
from app.players import Players

application = Flask(__name__)

bootstrap = Bootstrap(application)
moment = Moment(application)

ranking_dha = RankingCapture(ranking_urls=["/ranking_jugadores.asp?Cod_Cat="], category="DHA",
                             root_urls=["http://www.fatm.com.es/", "http://www.fatm.com.es/2019-2020_1_ronda/"])
ranking_dha.load_ranking()
ranking_dha.process_players()
ranking_dha.process_games()

players_dha = Players(ranking_dha.players, ranking_dha.games)
players_dha.sort_games_by_date()
players_dha.remove_duplicate_games()
players_dha.is_repeated_players()
players_dha.scoring()
players_dha.join_duplicated_players()

ranking_sda = RankingCapture(ranking_urls=["/ranking_jugadores.asp?Cod_Cat="], category="SDA",
                             root_urls=["http://www.fatm.com.es/", "http://www.fatm.com.es/2019-2020_1_ronda/"])
ranking_sda.load_ranking()
ranking_sda.process_players()
ranking_sda.process_games()

players_sda = Players(ranking_sda.players, ranking_sda.games)
players_sda.sort_games_by_date()
players_sda.remove_duplicate_games()
players_sda.is_repeated_players()
players_sda.scoring()
players_sda.join_duplicated_players()

ranking_tn = RankingCapture()
ranking_tn.load_ranking()
ranking_tn.process_players()
ranking_tn.process_games()

players_tn = Players(ranking_tn.players, ranking_tn.games)
players_tn.sort_games_by_date()
players_tn.remove_duplicate_games()
players_tn.is_repeated_players()
players_tn.scoring()
players_tn.join_duplicated_players()


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@application.route('/')
def index():
    return render_template('ranking.html', name="Ranking Global", people=players_tn.players)

@application.route('/super/ranking')
def super_ranking():
    return render_template('ranking.html', name="Ranking Global", people=players_sda.players)

@application.route('/dhonor/ranking')
def dhonor_ranking():
    return render_template('ranking.html', name="Ranking Global", people=players_dha.players)


@application.route('/update_ranking')
def update():
    ranking_tn = RankingCapture()
    ranking_tn.load_ranking()
    ranking_tn.process_players()
    ranking_tn.process_games()
    ranking_tn.save_players("players.json")
    ranking_tn.save_games("games.json")
    players_tn.sort_games_by_date()
    players_tn.remove_duplicate_games()
    players_tn.scoring()
    return render_template('ranking.html', name="Ranking Global", people=players_tn.players)

