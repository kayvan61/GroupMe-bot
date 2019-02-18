from time import sleep
from random import choice
import bot 
import threading

class duel(threading.Thread):
    lobby_time = 300
    players = set()
    started = False
    item = ["A dildo",
            "A New PC",
            "A Vape",
            "13 cats",
            "2 half used juul pods",
            "A ultra rare Miku body pillow",
            "one 2d girl tiddie game console",
            "an N-word pass",
            "death",
            "A pair of timbs",
            "A pair of GucciXLouis Vitton slides",
            "A 'them airpods'",
            "one(1) Pratik staring at you weirdly from across the room at a social gathering of mutual friends",
            "<Empty String>"]
    
    def __init__(self, lt, starting_p):
        super(duel, self).__init__()
        self.lobby_time = lt
        self.players = set()
        self.players.add(starting_p)
        self.started = False
        self.remaining_time = lt

    def startDuel(self):
        self.started = True
        self.start()
    
    def isDone(self):
        return not self.started

    
    def getLobbyState(self):
        if(self.remaining_time > 0):
            bot.postMessage("remaining time:" , self.remaining_time,
                        "\njoined Players:", self.players)

    def run(self):
        print("running a duel for", self.remaining_time,"seconds")
        while self.remaining_time > 0:
            sleep(1)
            print(self.players)
            self.remaining_time -= 1
            print("doing a duel with", self.remaining_time, "sec left")
        bot.postMessage("congrats to " + str(choice(list(self.players))) + " for winning! "+
                            "\nfor your effort you win " + choice(duel.item))
        self.started = False
        self.join()

    def addPlayer(self, player):
        self.players.add(player)
