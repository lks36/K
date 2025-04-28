from flask import Flask, render_template, request, session, flash, redirect
import time
import sqlite3
import random
import partie

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
