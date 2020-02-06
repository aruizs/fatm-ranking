from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from app.ranking_capture import RankingCapture
from app.players import Players

application = Flask(__name__)

bootstrap = Bootstrap(application)
moment = Moment(application)

ranking_tn = RankingCapture()
ranking_tn.load_ranking()
ranking_tn.process_players()
ranking_tn.process_games()

players_tn = Players(ranking_tn.players, ranking_tn.games)
players_tn.sort_games_by_date()
players_tn.remove_duplicate_games()
players_tn.scoring()


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 500


@application.route('/')
def index():
    return render_template('ranking.html', name="Ranking Global", people=players_tn.players)
