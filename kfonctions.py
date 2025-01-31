from flask import Flask, render_template, request, session
import sqlite3


def get_leaderboard()->list[tuple]:
    """Récupérer le leaderboard

    Returns :
        list[tuple]: results from the SQL request in the leaderboard table

    """
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        # Problème : Injection SQL possible (?)
        sqlreq = f"SELECT score, username FROM leaderboard JOIN users ON users.id = leaderboard.id ORDER BY score ASC"
        res = cur.execute(sqlreq)
        reslist = res.fetchall()
        con.close()
        print("test", reslist)
        return reslist

    except Exception as erreur:
        print("Erreur dans get_leaderboard() :", erreur)
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
                return True
            else:
                return False
    except Exception as erreur:
        print("Erreur dans verifier_login() :", erreur)
        return False
    finally:
        con.close()
