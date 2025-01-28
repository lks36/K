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

if __name__ == '__main__':
    app.run(debug=True)