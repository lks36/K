# Projet K

## Descriptif du projet 

### Notre projet consiste en une plateforme de débat en ligne, le format des débats est le suivant : <br>
Une partie classique opposera deux équipes de **N** membres, chaque membre **K** d'une équipe affrontera le membre **K** de l'équipe adverse, le score total de l'équipe est calculé a partir de le somme des points de chaque équipier : pour chaque affrontement, une question en rapport avec le sujet initial est choisi (aléatoirement) et les deux concurrents se voient attribuer un camps à défendre (aléatoirement aussi), pour gagner, il faut être capable de **défendre son sujet** et de faire preuve d'**éloquence** pour gagner le vote des spectateurs.

Un tournoi opposera 8 à 16 joueurs, toujours dans le format d'un affrontement en 1 contre 1, cette fois les joueurs ne font pas partie d'une équipe mais d'un arbre de tournoi, le gagnant de le finale remporte des points pour le **classement global**.

## Requis

1. Python 3.10 ou plus : [installation](https://www.python.org/downloads/)
2. Flask : [installation](#installation--usage)
3. sqlite3 : [installation (site de sqlite)](https://www.sqlite.org/s)

## Installation & usage
1. Installer Flask & Sqlite3 : [guide d'installation](https://flask.palletsprojects.com/en/stable/installation/)
    ```
    > pip install Flask
    > pip install sqlite3
    ```

2. Lancer le programme **main.py**
    ```
    > python3 main.py
    ```

3. Ouvrir ``localhost:5000`` dans un navigateur

4. En cas de problème :
    - Vérifier l'installation de Flask
    - Vérifier keyfile.txt
    - Initialiser la base de données [(comment faire ?)](#initialiser-la-base-de-données-si-besoin)
    

## Initialiser la base de données (si besoin)

1. Avoir installé [sqlite3](https://www.sqlite.org/)

2. Se placer dans le répertoire database et executer :<br>
**Pour Bash**
    ```
    > sqlite3 database.db < init_user_table
    ```
    **Pour Windows**
    ```
    > sqlite3 database.db
    ``````
    Executer directement cette commande dans le programme sqlite
    ```sql
    CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    score TEXT NOT NULL);
    ```
## Membres du projet
- BENMERZOUQ Charif-Mehdi (scrum master)
- XIA Eric
- AYODELE Toyin
- MACCARONE-SAURET Antoine
- HALILOU Yanis
- LI Kun
