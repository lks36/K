from flask import Flask, render_template, request, session, flash, redirect
import time
import sqlite3
from matchmaking import *



def verifie_connexion():
    try:
        if session is None:
            return False
        if session['username'] == None:
            return False
        if session['email'] == None:
            return False
        return True
    except:
        return False

def creer_partie_classique(nom:str, host:str, maxplayer:int)->bool:
    """Créer une partie classique dans la base de données

    Returns :
        bool: true if the game was successfully created
    """
    print(host, nom, maxplayer)
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        ts = int(round(time.time(), 0))
        cur.execute(f"INSERT INTO classic ('host', 'name', 'status', 'maxplayers', 'creation') VALUES ('{host}', '{nom}', 'en attente', {maxplayer}, {ts})")
        con.commit()
        return True
    except Exception as erreur:
        print("Erreur dans creer_partie_classique : ", erreur)
        return False


def get_leaderboard()->list[tuple]:
    """Récupérer le leaderboard

    Returns :
        list[tuple]: results from the SQL request in the leaderboard table

    """
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        # Problème : Injection SQL possible (?)
        sqlreq = f"SELECT score, username FROM leaderboard JOIN users ON users.id = leaderboard.id ORDER BY score DESC"
        res = cur.execute(sqlreq)
        reslist = res.fetchall()
        con.close()
        print("test", reslist)
        return reslist

    except Exception as erreur:
        print("Erreur dans get_leaderboard() :", erreur)
        return []

def get_list_data(username)->dict:
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        print(username)
        sqlreq = f"SELECT * FROM users WHERE username='{username}'"
        res = cur.execute(sqlreq)
        reslist = res.fetchone()
        dictionnaire = dict()
        dictionnaire["username"] =username
        dictionnaire["nb_parties"] = reslist[4]
        dictionnaire["nb_victoires_classique"] = reslist[5]
        dictionnaire["nb_victoires_tournois"] = reslist[6]
        dictionnaire["taux_victoires"] = reslist[7]
        dictionnaire["rang"] = reslist[8]
        dictionnaire["score_total"] = reslist[9]
        dictionnaire["niveau"] = reslist[10]
        con.close()
        print(dictionnaire)
        return dictionnaire

    except Exception as erreur:
        print("Erreur dans get_list_data() :", erreur)
        return []


def verifier_login()->bool:
    """Verifie le login de l'utilisateur (request.form['email'], request.form['password'])
    
    Returns : 
        bool: true if the email and the password are correct
    
    """
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        # Problème : Injection SQL possible (?)
        sqlreq = f"SELECT * FROM users WHERE email = '{request.form['email']}'"
        res = cur.execute(sqlreq)
        #Attention : Récuperer le tuple de fetchone dans une variable
        res_tuple = res.fetchone()
        email = res_tuple[2]
        password = res_tuple[3]
        print(f"tuple : {res_tuple}")
        if email == None:
            # Cette adresse n'existe pas
            return False
        else:
            if password == request.form['password']:
                session['username'] = res_tuple[1]
                return True
            else:
                return False
    except Exception as erreur:
        print("Erreur dans verifier_login() :", erreur)
        return False
    finally:
        con.close()

def creation(username,email,password):
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        # Problème : Injection SQL possible (?)
        sqlreq = "SELECT * FROM users WHERE email = ? OR username = ?"
        cur.execute(sqlreq, (email, username))
        existing_user = cur.fetchone()

        if existing_user:
            # si une user avec le meme pseudo ou email
            return render_template("create.html", error="Exception_Deja")

        # On ajouter le nouvel user a la database
        sqlreq = "INSERT INTO users (username, email, password, nb_parties, nb_victoires_classique, nb_victoires_tournois, taux_victoire, rang, score_total, niveau) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur.execute(sqlreq, (username, email, password, 0, 0, 0, 0, 0, 0, 0))
        con.commit()

        #recuprer l'id de l'utilisateur nouvellement créé
        cur.execute(f"SELECT id FROM users WHERE email = '{email}'")
        id = cur.fetchone()[0]

        # initialiser le score de l'utilisateur dans leaderboard
        cur.execute(f"INSERT INTO leaderboard VALUES ({id}, 0)")
        con.commit()

        flash("Compte crée avec succès !","success")
        return redirect("./connexion")
    
    except Exception as erreur:
        print("Erreur dans creation() :", erreur)
        return render_template("create.html", error=erreur)
    finally:
        con.close()