from cards import createCards
from random import randint

class Diler:
    def __init__(self):
        self.deck = createCards()
        self.table = []
        self.clients = {}

    def request(self, id):
        if id in self.clients:
            self.clients[id].append(self.getCard())
        else:
            self.clients[id] = [self.getCard()]
        return self.clients[id][-1]

    def getCard(self):
        return self.deck.pop(randint(0, len(self.deck)-1))

    def getState(self):
        return self.clients

    def roundRun(self):
        pass

    def flop(self):
        print("выдача общих карт")
        self.roundRun()
        for i in range(3):
            self.table.append(self.getCard())
        print(' '.join(map(str, self.table)))
        return ' '.join(map(str, self.table))

    def turn(self):
        self.roundRun()
        self.table.append(self.getCard())
        return ' '.join(map(str, self.table))

    def river(self):
        self.roundRun()
        self.table.append(self.getCard())
        return ' '.join(map(str, self.table))

    def opening(self):
        self.roundRun()
        return ''
