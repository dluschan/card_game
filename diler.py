from cards import createCards
from random import randint
from comparator import Comparator
from time import sleep

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

        class Bet(Ready):
            pass

        class AllIn(Bet):
            pass

        class Called(Bet):
            pass

        class Rised(Bet):
            pass

        class Pass(Ready):
            pass

        def __init__(self, id, conn):
            self.rise_client = None
            self.conn = conn
            self.id = id
            self.cards = []
            self.status = Diler.Client.NotReady()
            self.bet = 0
            self.money = 1000
            self.pass = False

        def __eq__(self, other):
            return self.id == other.id

        def addCard(self, card):
            self.cards.append(card)

        def ready(self, max_bet):
            return self.money == 0 or self.bet >= max_bet or self.pass

    def __init__(self, server):
        self.server = server
        self.deck = createCards()
        self.table = []
        self.clients = []
        self.comparator = Comparator()
        self.rise_client = None
        self.bet = 0
        self.bank = 0
        self.big_blind = 100

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
        for client in filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients):
            client.status = Diler.Client.NotReady()
            
        k = 0 if self.rise_client is None else self.rise_client
        
        while not all([client.ready() for client in self.clients]) or len(list(filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients))) < 2:
            if not self.clients[k].ready():
                sleep(0.01)
                if self.bet > 0:
                    self.server.send(self.clients[k].conn, 'ask1 ' + str(bet - self.clients[k].bet))
                else:
                    self.server.send(self.clients[k].conn, 'ask0')
                ans = self.server.recv(self.clients[k].conn)
                self.broadcast('info: игрок ' + str(self.clients[k].id) + ' ответил ' + ans)
                if ans == 'check':
                    self.clients[k].status = Diler.Client.Check()
                elif ans == 'pass':
                    self.clients[k].status = Diler.Client.Pass()
                elif ans == 'call':
                    self.clients[k].status = Diler.Client.Called()
                elif ans[:4] == 'rise' or ans[:3] == 'bet':
                    for c in filter(lambda x: type(x.status) != Diler.Client.Pass, self.clients):
                        c.status = Diler.Client.NotReady()
                    self.clients[k].status = Diler.Client.Rised()
                    self.rise_client = k
                    bet = int(ans[4:])
                    self.bank += bet
                    self.clients[k].bet = bet
                else:
                    self.clients[k].status = Diler.Client.Pass()
                    print('error: непонятный ответ от клиента')
            k = (k + 1) % len(self.clients)

    def blind(self):
        self.bank += self.big_blind // 2
        self.bank += self.big_blind
        self.clients[0].bed(self.big_blind // 2)
        self.clients[1].bed(self.big_blind)
        self.bet = True
        return "Игрок " + str(self.clients[0].id) + " поставил " + str(self.big_blind // 2) + ", игрок " + str(self.clients[1].id) + " поставил " + str(self.big_blind)

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

    def game(self):
        self.broadcast(self.blind())
        self.broadcast(self.flop())
        self.broadcast(self.turn())
        self.broadcast(self.river())
        self.broadcast(self.opening())
        self.next_turn()
        self.broadcast("Спасибо за игру!")

    def broadcast(self, msg):
        for client in self.clients:
            self.server.send(client.conn, msg)

    def next_turn(self):
        self.clients.append(self.clients.pop(0))
