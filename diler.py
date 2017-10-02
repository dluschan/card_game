from cards import createCards
from random import randint
from comparator import Comparator

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

        class Pass(Ready):
            pass

        def __init__(self, id, conn):
            self.rise_client = None
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
        self.comparator = Comparator()

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
        if len(list(filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients))) < 2:
            return

        for client in filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients):
            client.status = Diler.Client.NotReady()
            
        k = 0 if rise_client is None else rise_client
        
        while not all([client.ready() for client in self.clients]):
            if not self.clients[k].ready():
                self.server.send(self.clients[k].conn, 'ask')
                ans = self.server.recv(self.clients[k].conn)
                self.server.broadcast('info: игрок ' + str(self.clients[k].id) + ' ответил ' + ans)
                if ans == 'pass':
                    self.clients[k].status = Diler.Client.Pass()
                elif ans == 'call':
                    self.clients[k].status = Diler.Client.Called()
                elif ans == 'rise':
                    for c in filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients):
                        c.status = Diler.Client.NotReady()
                    self.clients[k].status = Diler.Client.Rised()
                    self.rise_client = k
                else:
                    self.clients[k].status = Diler.Client.Pass()
                    print('error: непонятный ответ от клиента')
            k = (k + 1) % len(self.clients)

    def flop(self):
        self.roundRun()
        for i in range(3):
            self.table.append(self.getCard())
        print('flop', ' '.join(map(str, self.table[0: 3])))
        return ' '.join(map(str, self.table))

    def turn(self):
        self.roundRun()
        self.table.append(self.getCard())
        print('turn', str(self.table[-1]))
        return str(self.table[-1])

    def river(self):
        self.roundRun()
        self.table.append(self.getCard())
        print('river', str(self.table[-1]))
        return str(self.table[-1])

    def opening(self):
        self.roundRun()
        clients = {}
        for client in filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients):
            clients[client.id] = client.cards
        win = self.comparator.compare(clients, self.table)
        if len(win) == 1:
            res = 'победитель: ' + str(win[0])
        else:
            res = 'победители: ' + ', '.join(map(str, win))
        return res
