from flask import Flask, render_template, request, session, flash, redirect
import time
import sqlite3
from kfonctions import *
import pytest
import tempfile
import os


app = Flask(__name__)
app.secret_key = 'test_key'

@pytest.fixture #bdd temporaire
def test_db():
    ostest, db_path = tempfile.mkstemp()
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.execute('''CREATE TABLE classic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host TEXT,
    name TEXT,
    status TEXT NOT NULL,
    maxplayers INT,
    creation TIMESTAMP
    )''')

    cur.execute('''CREATE TABLE leaderboard (
    id INT PRIMARY KEY,
    score TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
    )''')

    con.commit()
    yield db_path
    os.close(ostest)
    try:
        os.remove(db_path)
    except OSError:
        pass


@pytest.fixture
def app_context():
    with app.test_request_context():
        yield
    
@pytest.fixture
def clean_session(app_context):
    session.clear()
    yield

def test_get_classic_games(test_db, monkeypatch):
    
    connect_original = sqlite3.connect #Correction problème récursion

    def mock_connect(db_path):
        return connect_original(test_db)
    monkeypatch.setattr(sqlite3, "connect", mock_connect) #modifie sqlite3.connect en "mock_connect"

    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute("INSERT INTO classic (host, name, status, maxplayers, creation) VALUES ('testPseudo', 'Partie 99', 'en attente', 4, 123456789)")
    con.commit()
    con.close()

    result = get_classic_games()
    assert result == [(1, 'testPseudo', 'Partie 99', 'en attente', 4, 123456789)]



    #Test avec aucune partie dans la base

    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute("DELETE FROM classic")
    con.commit()
    con.close()
    assert get_classic_games() == []

def test_verifie_connexion(clean_session):

    #Session vide : 
    assert verifie_connexion() == False

    #username et email définis
    session['username'] = 'testPseudo'
    session['email'] = 'test@gmail.com'
    assert verifie_connexion() == True

    #email est None
    session['username'] = 'test_user'
    session['email'] = None
    assert verifie_connexion() == False

def test_creer_partie_classique(test_db, monkeypatch):

        connect_original = sqlite3.connect #Correction problème récursion

        def mock_connect(db_path):
            return connect_original(test_db)
        monkeypatch.setattr(sqlite3, "connect", mock_connect) #modifie sqlite3.connect en "mock_connect"

        monkeypatch.setattr(time, 'time', lambda: 123456789)

        result = creer_partie_classique("Partie 88", "TestPseudo", 5)
        assert result == True

        con = sqlite3.connect(test_db)
        cur = con.cursor()
        cur.execute("SELECT * FROM classic")
        data = cur.fetchone()
        assert data == (1, "TestPseudo", "Partie 88", "en attente", 5, 123456789)
        con.close()



def test_get_leaderboard(test_db, monkeypatch):
    with app.test_request_context():
        connect_original = sqlite3.connect #Correction problème récursion

        def mock_connect(db_path):
            return connect_original(test_db)
        monkeypatch.setattr(sqlite3, "connect", mock_connect) #modifie sqlite3.connect en "mock_connect"

        
        con = sqlite3.connect(test_db)
        cur = con.cursor()

        creation("TestPseudo1", "TestPseudo1@ksite.com", "TestPseudoMDP")
        creation("TestPseudo2", "TestPseudo2@ksite.com", "TestPseudoMDP")
        creation("TestPseudo3", "TestPseudo3@ksite.com", "TestPseudoMDP")
        cur.execute("INSERT INTO leaderboard (id, score) VALUES (1, 5)")
        cur.execute("INSERT INTO leaderboard (id, score) VALUES (3, 2)")
        cur.execute("INSERT INTO leaderboard (id, score) VALUES (2, 4)")

        con.commit()
        con.close()


        result = get_leaderboard()
        assert result == [('2', "TestPseudo3"),  ('4', 'TestPseudo2'), ('5', "TestPseudo1")]

        con = sqlite3.connect(test_db)
        cur = con.cursor()
        cur.execute("DELETE FROM leaderboard")
        cur.execute("DELETE FROM users")
        con.commit()
        con.close()
        assert get_leaderboard() == []

def test_verifier_login(test_db, monkeypatch):
    with app.test_request_context():
        connect_original = sqlite3.connect

        def mock_connect(db_path):
            return connect_original(test_db)
        monkeypatch.setattr(sqlite3, "connect", mock_connect)

        con = sqlite3.connect(test_db)
        cur = con.cursor()
        creation("TestPseudo1", "TestPseudo1@ksite.com", "TestPseudoMDP")
        con.commit()
        con.close()
    
    #Données correcte
    with app.test_request_context(method='POST', data={'email': 'TestPseudo1@ksite.com', 'password': 'TestPseudoMDP'}):
        result = verifier_login()
        assert result == True
        assert session['username'] == 'TestPseudo1'
    
    #Mail incorrecte
    with app.test_request_context(method='POST', data={'email': 'fausseAdresse1@ksite.com', 'password': 'TestPseudoMDP'}):
        result = verifier_login()
        assert result == False
    
    #MDP incorrecte
    with app.test_request_context(method='POST', data={'email': 'TestPseudo1@ksite.com', 'password': 'FauxMDP'}):
        result = verifier_login()
        assert result == False


def test_creation(test_db, app_context, monkeypatch):

    connect_original = sqlite3.connect
    def mock_connect(db_path):
        return connect_original(test_db)
    monkeypatch.setattr(sqlite3, "connect", mock_connect)
    
    def mock_render_template(template, **error):
        return f"{template} {error}"
    monkeypatch.setattr('kfonctions.render_template', mock_render_template)
    
    def mock_redirect(connexion):
        return connexion
    monkeypatch.setattr('kfonctions.redirect', mock_redirect)
    

    with app.test_request_context():
        result = creation("TestPseudo1", "TestPseudo1@ksite.com", "TestPseudoMDP")
        assert result == "./connexion"
    
    # Tout bon, test de l'objectif
    con = sqlite3.connect(test_db)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username = 'TestPseudo1'")
    data = cur.fetchone()
    assert data == (1, 'TestPseudo1', 'TestPseudo1@ksite.com', 'TestPseudoMDP')
    con.close()
    
    # email déjà utilisé
    with app.test_request_context():
        result = creation('TestPseudo2', 'TestPseudo1@ksite.com', 'TestMDP')
        assert result == "create.html {'error': 'Exception_Deja'}"
    
    # username déjà pris
    with app.test_request_context():
        result = creation('TestPseudo1', 'TestPseudo2@example.com', 'TestMDP')
        assert result == "create.html {'error': 'Exception_Deja'}"

