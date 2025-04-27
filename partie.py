

class Partie:

    def __init__(self, id:int, id_thematique:int, nb_joueurs:int):
        self.id = id
        self.thematiqueID = id_thematique
        self.status = "en attente"
        self.nb_joueurs = nb_joueurs
        self.equipes = {
            "team1": [],
            "team2": []
        }
        self.msg_hist = []



class Player:

    def __init__(self):
        pass