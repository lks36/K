import time
import sqlite3
from matchmaking import *
clock = 0

def get_users_in(gameid):
    try:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"SELECT count(*) FROM user_in_game_classic WHERE id_partie='{gameid}'"
        count = cur.execute(sqlreq).fetchone()[0]
        con.close()
        return count
    except Exception as erreur:
        print("Erreur dans get_usersin() :", erreur)
        return 0


def parties_pretes():
    try:
        res = []
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        sqlreq = f"SELECT * FROM classic WHERE status='en attente'"
        parties_en_attente = cur.execute(sqlreq).fetchall()
        for partie in parties_en_attente:
            count = get_users_in(partie[0])
            print(f"La partie {partie[0]} compte {count} joueur(s)")
            if partie[4] <= count:
                print(f"Lancement de la partie {partie[0]} ...")
                res.append(partie)
        con.close()
        return res
    except Exception as erreur:
        print("Erreur dans lancer_partie() :", erreur)
        return []




while True:
    if clock%120 == 0:
        creer_partie_classique("Classic Game", "Ksite.com", "1")
    print(clock)
    time.sleep(4)
    clock += 4
    for partie in parties_pretes():
        print("Lancement de", partie[0])
        if lancer_partie(partie[0]):
            print("Parite lancée :", partie[0])
    
