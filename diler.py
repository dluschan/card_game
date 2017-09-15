from cards import createCards
from random import randint

class Diler:
    def __init__(self):
        self.deck = createCards()
        self.clients = {}

    def request(self, id):
        if id in self.clients:
            self.clients[id].append(self.getCard())
        else:
            self.clients[id] = [self.getCard()]
        return self.clients[id]

    def getCard(self):
        return self.deck.pop(randint(0, len(self.deck)-1))

    def getState(self):
        return self.clients
