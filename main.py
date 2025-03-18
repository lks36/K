from flask import Flask, render_template, request, session, redirect, jsonify, flash
from flask_socketio import SocketIO, join_room, leave_room, send
import time
import os
import sqlite3
from kfonctions import *
import profil

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = "./static/avatars"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

rooms = {307:{"members":0, "messages":[]}, 302:{"members":0, "messages":[]}}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1000

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

keyfile = open("./keyfile.txt")
key = keyfile.read()
keyfile.close()
app.secret_key = key

@app.route("/")
def index():
    lb = get_leaderboard()
    print(session)
    if session and session["id"]:
        return render_template("./index.html", leaderboard=lb, iter_liste=range(len(lb)), avatar=str(session["id"]))  
    else:
        return render_template("./index.html", leaderboard=lb, iter_liste=range(len(lb)), avatar="default")

@app.route("/connexion", methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if verifier_login(email, password):
            # A faire : Créer une session
            session['email'] = email
            session['id'] = get_id_by_email(session["email"])
            session['username'] = get_list_data_id(session['id'])['username']
            return redirect("/")
        else:
            session['email'] = None
            session['id'] = None
            session['username'] = None
            return redirect("/create")
    else:
        return render_template("./connexion.html")
    
@app.route("/leaderboard")
def leaderboard():
    leaderboard_list = get_leaderboard()
    return render_template("./leaderboard.html", leaderboard=leaderboard_list, iter_liste=range(len(leaderboard_list)))

@app.route("/disconnect")
def disconnect():
    session.clear()
    return render_template("./disconnect.html")

@app.route("/howtoplay")
def howtoplay():
    return render_template("./regles.html")

@app.route("/profil")
def profil():
    if session and session["email"]:
        return render_template("./profil.html", data=get_list_data(session['username']), avatar=get_user_avatar(session["id"]))
    else:
        return redirect("/connexion")
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
    room = session.get("room")
    if room:
        return redirect(f"/game/{room}")
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

    rooms[gameid] = {"members":0, "messages":[]}

    print(f"Found : {found}\nGameid:{gameid}\n Status : {status}\n Max : {maxjoueurs}")

    return jsonify({"found": found, "status": status, "gameid":gameid, "ready":ready})


@app.route("/ajouter_queue", methods=['GET'])
def ajouter_queue():
    gameid = request.args.get("gameid")
    add_queue(session["id"], gameid)
    return jsonify({"added":True})

@app.route("/wait_game", methods=['GET']) 
def wait_game():
    #Récuperer le gameid passé en paramètre de la requête
    gameid = request.args.get("gameid")
    #Tenter de lancer la partie
    res=attendre_partie(gameid)
    #Renvoyer True si la partie a bien été lancée, False sinon
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

@app.route("/game/<int:gameid>")
def show_game(gameid):
    session["room"] = gameid
    return render_template("./ingame.html", room=gameid)


@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    if session and session['id']:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash("No file part")
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file.')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = f"{session['id']}.jpg"
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return redirect("/profil")
        return render_template("./edit_profile.html", userid=session['id'])
    else:
        flash("Erreur")
        return redirect("/")



@socketio.on('connect')
def handle_connect():
    room = session.get("room")
    name = session.get("username")
    if not room or not name:
        return
    join_room(room)
    print(f"{name} a rejoint la room {room}")

@socketio.on('message')
def handler_message(payload):
    room = session.get("room")
    name = session.get("username")
    if room not in rooms.keys():
        return
    
    message = {
        "sender" : name,
        "message" : payload["message"]
    }
    send(message, to=room)
    rooms[room]["messages"].append(message)



if __name__ == '__main__':
    socketio.run(app, debug=True)