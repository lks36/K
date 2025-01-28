from flask import Flask, render_template, request, session
import sqlite3


def verifier_login()->bool:
    """
    Verifie le login de l'utilisateur (request.form['email'], request.form['password'])
    """
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        # Problème : Injection SQL possible (?)
        sqlreq = f"SELECT * FROM users WHERE email = '{request.form['email']}'"
        res = cur.execute(sqlreq)
        #Attention : Récuperer le tuple de fetchone dans une variable
        tuple = res.fetchone()
        email = tuple[2]
        password = tuple[3]
        print(f"tuple : {tuple}")
        if email == None:
            # Cette adresse n'existe pas
            return False
        else:
            if password == request.form['password']:
                return True
            else:
                return False
    except Exception as erreur:
        print(erreur)
        return "<p> Erreur lors de la connexion à la base de données <p>"
    finally:
        con.close()