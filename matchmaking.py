from flask import Flask, render_template, request, session, flash, redirect
import time
import sqlite3
import random


def get_game_info(gameid):
    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    sqlreq = f"SELECT * FROM classic WHERE id={gameid}"
    res = cur.execute(sqlreq).fetchone()
    con.close()
    return {"status":res[3], "maxplayers":res[4]}

def get_classic_games()->list[tuple]:
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"SELECT * FROM classic"
        res = cur.execute(sqlreq)
        reslist = res.fetchall()
        con.close()
        return reslist

    except Exception as erreur:
        print("Erreur dans get_classic_games() :", erreur)
        return []

def choose_game():
    try:
        status = "None"
        gameid=-1
        gamelist = get_classic_games()
        while status != "en attente":
            game=random.choice(gamelist)
            gameid=game[0]
            status=game[3]
            maxjoueurs = game[4]

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"SELECT count(*) FROM user_in_game_classic WHERE id_partie"
        count = cur.execute(sqlreq).fetchone()[0]
        con.close()
        return {"gameid": gameid, "status":status, "nbjoueurs":count, "maxjoueurs":maxjoueurs}

    except Exception as erreur:
        print("Erreur dans choose_game() :", erreur)
        return {"gameid": 0, "status":"Erreur", "nbjoueurs":0}

def add_queue(userid, gameid):
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"INSERT into user_in_game_classic VALUES ({gameid}, {userid})"
        cur.execute(sqlreq)
        con.commit()
        con.close()
        return True
    except Exception as erreur:
        print("Erreur dans add_queue() :", erreur)
        return False

def lancer_partie(gameid):
    maxplayers = get_game_info(gameid)["maxplayers"]

    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    sqlreq = f"SELECT count(*) FROM user_in_game_classic WHERE id_partie"
    count = cur.execute(sqlreq).fetchone()[0]
    if count >= maxplayers:
        sqlreq = f"UPDATE classic SET status='ready' WHERE id={gameid}"
        cur.execute(sqlreq)
        con.close()
        return True
    con.close()
    return False