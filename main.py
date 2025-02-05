from flask import Flask, render_template, request, session
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
    return render_template("./disconnect.html")

@app.route("/howtoplay")
def howtoplay():
    return render_template("./regles.html")

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