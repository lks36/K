from flask import Flask, render_template, request, session, flash, redirect
import time
import sqlite3





def get_user_avatar(userid:int)->str:
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"SELECT avatar FROM users WHERE id={userid}"
        res = cur.execute(sqlreq).fetchone()[0]
        con.close()
        return res
    except Exception as erreur:
        print("Erreur dans get_id_by_email():", erreur)
        return "default"