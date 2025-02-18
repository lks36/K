from flask import Flask, render_template, request, session, redirect, jsonify, flash
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
    return render_template("./index.html", leaderboard=get_leaderboard())

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
    if len(leaderboard_list) < 10:
        liste=range(len(leaderboard_list))
    else:
        liste=range(10)
    return render_template("./leaderboard.html", leaderboard=leaderboard_list, iter_liste=liste)

@app.route("/disconnect")
def disconnect():
    session['email'] = None
    session['username'] = None
    return render_template("./disconnect.html")

@app.route("/howtoplay")
def howtoplay():
    return render_template("./regles.html")

@app.route("/profil")
def profil():
    return render_template("./profil.html", data=get_list_data(session['username']))

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

@app.route("/classic_queue", methods=['GET', 'POST'])
def classic_queue():
    if not verifie_connexion():
            return redirect("./connexion")
    liste_parties = get_classic_games()
    return render_template("./classic_queue.html", gamelist=liste_parties, iter_liste=range(len(liste_parties)))


@app.route("/check_game")
def check_game():
    """Envoie les données d'une partie dès qu'elle est trouvée au js de la page classicqueue"""

    #choisir une partie
    found = False
    ready = False
    game = choose_game()
    status = game["status"]
    gameid = game["gameid"]
    nbjoueurs = game["nbjoueurs"]
    maxjoueurs=game["maxjoueurs"]
    
    #effectuer le traitement
    if status == "en attente":
        found = True
    if status == "ready":
        ready = True

    print(f"Found : {found}\nGameid:{gameid}\n Status : {status}")

    return jsonify({"found": found, "status": status, "gameid":gameid, "ready":ready})


@app.route("/ajouter_queue", methods=['GET'])
def ajouter_queue():
    gameid = request.args.get("gameid")
    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute(f"SELECT id FROM users WHERE email = '{session['email']}'")
    id = cur.fetchone()[0]
    con.close()
    add_queue(id, gameid)
    return jsonify({"added":True})

@app.route("/launch_game", methods=['GET']) 
def launch_game():
    gameid = request.args.get("gameid")
    res=lancer_partie(gameid)
    return jsonify({"ready":res})

@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return render_template("create.html", error='Exception_Vide')
        else:
            return creation(username, email, password)
    else:
        return render_template("./create.html", error=None)

if __name__ == '__main__':
    app.run(debug=True)