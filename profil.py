from flask import Flask, render_template, request, session, flash, redirect
import time
import sqlite3


def set_user_avatar(userid:int, avatar:str):
    """
    Définir l'avatar de l'utilisateur dans la base de données
    """
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"UPDATE users SET avatar = '{avatar}' WHERE id={userid}"
        cur.execute(sqlreq)
        con.commit()
        con.close()
    except Exception as erreur:
        print("Erreur dans set_user_avatar() : ", erreur)

def get_user_avatar(userid:int)->str:
    """
    Récupérer le nom de l'avatar correspondant à l'utilisateur dont l'id est passé en paramètre.

    Args:
        - userid: id utilisateur dans la base de données
    Retourne:
        - str: nom du fichier jpg correspondant à l'avatar
    """
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"SELECT avatar FROM users WHERE id={userid}"
        res = cur.execute(sqlreq).fetchone()[0]
        con.close()
        return res
    except Exception as erreur:
        print("Erreur dans get_user_avatar():", erreur)
        return "default"