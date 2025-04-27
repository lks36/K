import time
import random
class Player:

    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
        self.messages = []
        self.avatar = "default"


class Partie:

    def __init__(self, id:int, id_thematique:int, max_joueurs:int):
        self.id = id
        self.thematiqueID = id_thematique
        self.status = "en attente"
        self.nb_joueurs = 0
        self.max = max_joueurs
        self.players = []
        self.equipes = {
            "team1": [],
            "team2": []
        }
        self.messages = []
        self.last_message_id = 0


        self.round = 1



        #Ordre de passsage
        self.talking_time = 10
        self.talking = 0
        self.order_index = 0
        self.order = [0, 3, 1, 4, 2, 5]
        self.skip = False
        self.start = time.time()
        self.change_time = self.start
        self.current_timer = 0


    def player_in(self, player:Player):
        for p in self.players:
            if p.id == player.id:
                return True
        return False


    def add(self, player:Player, team:int=None):
        """ 
        
        Cette methode ajoute une instance d'un joueur dans la partie

        Args:
            player (Player): instance du joueur de la classe Player
            team (int): numero de l'equipe 1 ou 2

        Renvoie:
            true si le joueur a bien été ajouté a la partie
            false sinon
        """

        try:
            if self.player_in(player):
                return False
            
            if team is None:
                if len(self.equipes["team1"]) == len(self.equipes["team2"]) and len(self.equipes["team1"])  < 3:
                    self.equipes["team1"].append(player)
                    self.players.append(player)
                    self.nb_joueurs += 1
                    return True
                elif len(self.equipes["team1"]) == len(self.equipes["team2"]) and len(self.equipes["team1"])  >= 3:
                    return False
                elif len(self.equipes["team1"]) > len(self.equipes["team2"]):
                    self.equipes["team2"].append(player)
                    self.players.append(player)
                    self.nb_joueurs += 1
                    return True
                return False
            else:
                if len(self.equipes[f"team{team}"]) < 3:
                    self.equipes[f"team{team}"].append(player)
                    self.players.append(player)
                    self.nb_joueurs += 1
                    return True
        except Exception as e:
            print("Erreur dans Partie.add() : ", e)
            return False

    def get_player(self, player_id:int):
        try:
            for player in self.players:
                if player.id == player_id:
                    return player
            return None
        except Exception as e:
            print("Erreur dans Partie.get_player() : ", e)

    def new_message_id(self):
        self.last_message_id += 1
        return self.last_message_id

    def next_talking(self):
        try:
            print("Index : ", self.order_index)
            if self.order_index < self.nb_joueurs:
                player = self.players[self.order_index]
                self.order_index += 1
                return player
            else:
                print("new round")
                self.round += 1
                self.order_index = 1
                return self.players[0]
        except Exception as e:
            print("Erreur dans next_talking : ", e)
            return None

    def choose_player(self):
        self.current_timer = time.time() - self.change_time
        if(self.talking is None):
            player = self.next_talking()
            self.talking = player.id
            return self.talking
        if(self.current_timer > self.talking_time or self.skip):
            self.skip = False
            #il faut changer de joueur
            player = self.next_talking()
            self.change_time = time.time()
            if(player):
                self.talking = player.id
            else:
                return self.talking
        return self.talking

    def sort_scores(self):
        if self.messages == []:
            return
        for i in range(0, len(self.messages)):
            for j in range(0, len(self.messages)):
                if self.messages[i].score > self.messages[j].score:
                    self.messages[i], self.messages[j] = self.messages[j], self.messages[i]
        


class Message:

    def __init__(self, id:int, author:Player, content:str, date:int):
        self.id = id
        self.author = author
        self.content = content
        self.date = date
        self.score = 0
        self.likes = 0
        self.attaquants = []

    
    def calcul_score(self):
        gain = self.likes*50 - len(self.attaquants)*50
        if gain > 0:
            self.score = gain
        else:
            self.score = 0