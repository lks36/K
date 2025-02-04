from flask import Flask, render_template, request, session, redirect
import time
import sqlite3
from kfonctions import *
app = Flask(__name__)


keyfile = open("./keyfile.txt")
key = keyfile.read()
keyfile.close()
app.secret_key = key

@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/connexion", methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        if verifier_login():
            # A faire : Créer une session
            session['email'] = request.form['email']

            return render_template("./index.html")
        else:
            session['email'] = None
            return render_template("./index.html")
    else:
        return render_template("./connexion.html")
    
@app.route("/leaderboard")
def leaderboard():
    leaderboard_list = get_leaderboard()
    return render_template("./leaderboard.html", leaderboard=leaderboard_list, iter_liste=range(len(leaderboard_list)))

@app.route("/disconnect")
def disconnect():
    session['email'] = None
    session['username'] = None
    return render_template("./disconnect.html")

@app.route("/howtoplay")
def howtoplay():
    return render_template("./regles.html")

@app.route("/startplaying")
def startplaying():
    return render_template("./startplaying.html")

@app.route("/createclassic", methods=['GET', 'POST'])
def createclassic():
    try:
        if not verifie_connexion():
            return redirect("./connexion")
        if request.method == 'POST':
            username = session['username']
            gamename = request.form['name']
            maxplayer = int(request.form['maxplayer'])
            if creer_partie_classique(gamename, username, maxplayer):
                return redirect("./classic_games")
            else:
                return "<p> Erreur lors de la création de la partie : veuillez verifier les paramètres </p>"
        else:
            return render_template("./createclassic.html")
    except Exception as e:
        print(e)
        return redirect("/")

@app.route("/classic_games", methods=['GET', 'POST'])
def classic_games():
    liste_parties = get_classic_games()
    return render_template("./classic_games.html", gamelist=liste_parties, iter_liste=range(len(liste_parties)))

if __name__ == '__main__':
    app.run(debug=True)