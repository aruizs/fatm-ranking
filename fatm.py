from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from app.ranking import Ranking, Category
from pathlib import Path

application = Flask(__name__)

bootstrap = Bootstrap(application)
moment = Moment(application)

dha_ranking = Ranking(Category.DHA)
dha_ranking.load()

sda_ranking = Ranking(Category.SDA)
sda_ranking.load()

tn_ranking = Ranking(Category.TN)
tn_ranking.load()


@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@application.route('/')
def index():
    return render_template('homepage.html', people_tn=tn_ranking.players.players[0:10],
                           people_sda=sda_ranking.players.players[0:10],
                           people_dha=dha_ranking.players.players[0:10])


@application.route('/liga_andalucia/ranking')
def liga_andalucia_ranking():
    return render_template('ranking.html', people=tn_ranking.players.players)


@application.route('/super/ranking')
def super_ranking():
    return render_template('ranking.html', people=sda_ranking.players.players)


@application.route('/dhonor/ranking')
def dhonor_ranking():
    return render_template('ranking.html', people=dha_ranking.players.players)


@application.route('/update_ranking')
def update():
    for filename in Path(".").glob("*.json"):
        filename.unlink()
    dha_ranking.load()
    sda_ranking.load()
    tn_ranking.load()
    return render_template('homepage.html', people_tn=tn_ranking.players.players[0:10],
                           people_sda=sda_ranking.players.players[0:10],
                           people_dha=dha_ranking.players.players[0:10])


@application.route("/liga_andalucia/<uid_player>")
def liga_andalucia_profile(uid_player):
    uid_player = next((player for player in tn_ranking.players.players if player["uid"] == int(uid_player)), None)

    return render_template("matches.html", name=uid_player['nombre'], matches=uid_player['played_matches'])


@application.route("/super/<uid_player>")
def super_profile(uid_player):
    uid_player = next((player for player in sda_ranking.players.players if player["uid"] == int(uid_player)), None)

    return render_template("matches.html", name=uid_player['nombre'], matches=uid_player['played_matches'])


@application.route("/dhonor/<uid_player>")
def dhonor_profile(uid_player):
    uid_player = next((player for player in dha_ranking.players.players if player["uid"] == int(uid_player)), None)

    return render_template("matches.html", name=uid_player['nombre'], matches=uid_player['played_matches'])