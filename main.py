from flask import Flask, render_template, request, session, redirect, jsonify, flash
from flask_socketio import SocketIO, join_room, leave_room, send
import time
import os
import sqlite3
from kfonctions import *
import profil
from partie import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = "./static/avatars"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

global lastid
lastid = 10000
TestRoom = Partie(10000, 0, 6)
rooms = {}
rooms[10000] = TestRoom 

liste_themes = ["Les pièces de théâtre sont-elles meilleures que les romans ?", "L’art peut-il être séparé de l’artiste ?", "L’art doit-il être financé par des fonds publics ?", "Faut-il augmenter le salaire minimum ?"]

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
    if session.get("id"):
        return render_template("./index.html", leaderboard=lb, iter_liste=range(len(lb)), avatar=get_user_avatar(session["id"]))  
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
    return redirect("/")

@app.route("/howtoplay")
def howtoplay():
    return render_template("./regles.html")

@app.route("/profil")
def profil():
    if session.get("username") and session.get("id"):
        return render_template("./profil.html", data=get_list_data(session['username']), avatar=get_user_avatar(session["id"]))
    else:
        return redirect("/connexion")
@app.route("/startplaying")
def startplaying():
    return render_template("./startplaying.html")

@app.route("/createclassic", methods=['GET', 'POST'])
def createclassic():
    """"""
    """"""
    try:
        if not verifie_connexion():
            return redirect("./connexion")
        if request.method == 'POST':
            username = session['username']
            gamename = request.form['name']
            maxplayer = int(request.form['maxplayer'])
            global lastid
            new_game = Partie(lastid+1, random.randint(0, len(liste_themes)), maxplayer)
            lastid+=1
            rooms[new_game.id] = new_game
            return redirect("./classic_games")
        else:
            return render_template("./createclassic.html")
    except Exception as e:
        print(e)
        return redirect("/")

@app.route("/classic_games", methods=['GET', 'POST'])
def classic_games():
    liste_parties = get_classic_games()
    return render_template("./classic_games.html", gamelist=rooms.values(), themes=liste_themes)

@app.route("/classic_queue", methods=['GET', 'POST'])
def classic_queue():
    """
    Afficher la page permettant de lancer une partie
    """
    if not verifie_connexion():
            return redirect("./connexion")
    room = session.get("room")
    if room:
        return redirect(f"/game/{room}")
    liste_parties = get_classic_games()
    return render_template("./classic_queue.html", gamelist=liste_parties, iter_liste=range(len(liste_parties)))


@app.route("/check_game")
def check_game():
    """
    Envoie les données d'une partie dès qu'elle est trouvée au js de la page classicqueue
    """

    return jsonify({"found": True, "status": "En attente", "gameid":10000, "ready":True})
    #Il aurait fallu refaire le systeme de matchmaking en l'adaptant aux objets de la classe Partie
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

    rooms[gameid] = Partie(gameid, random.randint(0, len(liste_themes)-1), 6)

    print(f"Found : {found}\nGameid:{gameid}\n Status : {status}\n Max : {maxjoueurs}")

    return jsonify({"found": found, "status": status, "gameid":gameid, "ready":ready})


@app.route("/create", methods=['GET', 'POST'])
def create():
    """
    Endpoint permettant de créer un compte
    """
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
    """
    Endpoint permettant d'afficher la partie en cours
    """
    session["room"] = gameid
    try:
        return render_template("./ingame.html", room=gameid, partie=rooms[gameid], equipe1=rooms[gameid].equipes["team1"], equipe2=rooms[gameid].equipes["team2"], themes=liste_themes, sessionid=session.get("id"))
    except:
        session["room"] = None
        return "Partie non trouvée"

@app.route("/game/<int:gameid>/game_review")
def game_review(gameid):
    """
    Afficher le résultat d'une partie sur une nouvelle page (les meilleurs messages et leur score)
    """
    try:
        if(rooms[gameid].status != "Terminée"):
            return redirect(f"/game/{gameid}")
        return render_template("./game_review.html", gameid=gameid, game_object=rooms[gameid], messages=rooms[gameid].messages)
    except:
        return "Partie non trouvée"
    

@app.route("/edit_profile", methods=['GET', 'POST'])
def edit_profile():
    """
    Gérer la modification de profil, envoi et réception d'un formulaire avec un fichier image
    """
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
                set_user_avatar(session["id"], session["id"])
                return redirect("/profil")
        return render_template("./edit_profile.html", userid=session['id'],  avatar=get_user_avatar(session["id"]))
    else:
        flash("Erreur")
        return redirect("/")



@socketio.on('connect')
def handle_connect():
    """
    Cette fonction permet de gérer l'ajout d'un utilisateur dans une partie 
    """
    room = session.get("room")
    id = session.get("id")
    name = session.get("username")
    if not room or not name:
        return
    user = Player(id, name)
    partie = rooms[room]
    #Verifier si le nombre de JOUEURS max est atteint (place en joueur ou spectateur)
    if(partie.nb_joueurs == partie.max):
        pass
    else:
        partie.add(user)

    join_room(room)
    print(f"{name} a rejoint la room {room}")

@socketio.on('like')
def handle_like(payload):
    """
    Cette fonction permet de gérer les likes côté objet
    """
    room = session.get("room")
    message_id = payload["message_id"]
    id = session.get("id")
    name = session.get("username")
    if not room or not name:
        return
    partie = rooms[room]
    for msg in partie.messages:
        if msg.id == message_id:
            msg.likes += 1

@socketio.on('message')
def handler_message(payload):
    """
    Cette fonction permet de gérer l'envoi d'un message et de construire le graphe.
    """

    #Récupérer les données de la partie
    rep = payload["rep"]
    room = session.get("room")
    pid = session.get("id")
    name = session.get("username")

    partie = rooms[room]
    joueur = partie.get_player(pid)
    joueur.avatar = get_user_avatar(pid)

    if room not in rooms.keys():
        return
    
    message = {
        "event":"message",
        "player_id" : pid,
        "sender" : name,
        "message" : payload["message"],
        "rep": rep
    }
    #Construire un objet message qu'on ajoute à l'objet de la Partie
    message_object = Message(partie.new_message_id(), joueur, message["message"], time.time())
    partie.messages.append(message_object)

    #Ajouter quelques informations à envoyer au JS
    message["date"] = message_object.date
    message["id"] = message_object.id
    message["avatar"] = joueur.avatar
    if joueur in partie.equipes["team1"]:
        message["equipe"] = 1
    else:
        message["equipe"] = 2
    

    #Envoyer le message à tous les autres joueurs
    send(message, to=room)

    #Ajouter au graphe si besoin
    if rep is not None:
        #Si on a séléctionné un message à répondre
        #ajouter l'objet message à la liste des attaquants du message rep
        for msg in partie.messages:
            if msg.id == rep:
                msg.attaquants.append(message_object)

@socketio.on('update')
def updateGameInfo(payload):
    """
    Mettre a jour les données de la partie 
    """
    room = session.get("room")
    game = rooms[room]
    if room not in rooms.keys():
        return

    #changer le choix du joueur    
    id = game.choose_player()
    #Recupérer l'utilisateur avec son id dans la partie
    player = "None"
    for p in game.players:
        if p.id == id:
            player = p.nom
    if player == "None":
        return 
    else:
        game.talking_time = 80
        game.round = game.round
        game.status = "En cours"
        
    if(game.round > 3):
        #Fin de la partie, calcul des scores et ajout des points
        infos = {
        "event": "end",
        "gameid": game.id}
        print("fin de la partie : ", game.id)
        for message in game.messages:
            message.calcul_score()
        game.sort_scores()
        send(infos, to=room)
        if game.status != "Terminée":
            for message in game.messages:
            #Calcul du gain (à revoir)
                gain = message.score
                if gain > 0:
                    add_score(message.author, gain)
        game.status = "Terminée"
        return infos

    #Mise a jour des equipes
    equipe1 = [p.nom for p in game.equipes["team1"]]
    equipe2 = [p.nom for p in game.equipes["team2"]]
    #Mise a jour de toutes les infos
    infos = {
        "event": "update",
        "status" : game.status,
        "talking" : player,
        "id" : id,
        "equipe1": equipe1,
        "equipe2": equipe2,
        "timer" : (int)(round(game.talking_time - game.current_timer + 1, 0)),
        "round" : game.round
    }
    send(infos, to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)   