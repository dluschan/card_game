from cards import createCards
from random import randint

class Diler:
    class Client:
        class Status:
            pass

        class NotReady(Status):
            def ready(self):
                return False

        class Ready(Status):
            def ready(self):
                return True

        class Check(Ready):
            pass

        class AllIn(Ready):
            pass

        class Called(Ready):
            pass

        class Rised(Ready):
            pass

        def __init__(self, id, conn):
            self.conn = conn
            self.id = id
            self.cards = []
            self.status = Diler.Client.NotReady()

        def __eq__(self, other):
            return self.id == other.id

        def addCard(self, card):
            self.cards.append(card)

        def ready(self):
            return self.status.ready()

    def __init__(self, server):
        self.server = server
        self.deck = createCards()
        self.table = []
        self.clients = []

    def getClient(self, client):
        missing = Diler.Client(client[1][1], client[0])
        if missing in self.clients:
            return self.clients[self.clients.index(missing)]
        self.clients.append(missing)
        return self.clients[-1]

    def request(self, client):
        card = self.getCard()
        self.getClient(client).addCard(card)
        return card

    def getCard(self):
        return self.deck.pop(randint(0, len(self.deck) - 1))

    def getState(self):
        return self.clients

    def roundRun(self):
        k = 0
        while not all([client.ready() for client in self.clients]):
            if not self.clients[k].ready():
                self.server.send(self.clients[k].conn, 'ваш ход')
            k = (k + 1) % len(self.clients)

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
