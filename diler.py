from cards import createCards
from random import randint
from comparator import Comparator
from time import sleep

class Diler:
    class Client:
        def __init__(self, id, conn):
            self.conn = conn
            self.id = id
            self.cards = []
            self.bet = 0
            self.money = 1000
            self.in_game = True
            self.big_blind = False

        def __eq__(self, other):
            return self.id == other.id

        def addCard(self, card):
            assert(len(self.cards) < 2)
            self.cards.append(card)

        def skip(self, max_bet):
            return self.money == 0 or self.bet >= max_bet or not self.in_game or not self.big_blind

    def __init__(self, server):
        self.server = server
        self.deck = createCards()
        self.table = []
        self.clients = []
        self.comparator = Comparator()
        self.rise_client = None
        self.bet = 0
        self.bank = [0]
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

    def dispense(self):
        for client in self.clients:
            self.send(client.conn, str(self.request(client.id)))

    def roundRun(self):
        k = 0 if self.rise_client is None else self.rise_client
        while not all([client.skip() for client in self.clients]) and len(list(filter(lambda client: client.in_game, self.clients))) > 1:
            if not self.clients[k].skip():
                sleep(0.01)
                request = ['fold', 'rise']
                if self.bet == 0 or self.clients[k].big_blind and self.clients[k].bet == self.bet:
                    request.append('check')
                else:
                    request.append('call')
                self.send(self.clients[k].conn, '|'.join(request))
                ans = self.server.recv(self.clients[k].conn)
                self.broadcast('info: игрок ' + str(self.clients[k].id) + ' ответил ' + ans)
                if ans.count('check') > 0:
                    self.
                elif ans.count('fold') > 0:
                    self.clients[k].in_game = False
                elif ans.count('call') > 0:
                    self.clients[k].bet = self.bet
                elif ans.count('rise') > 0:
                    self.clients[k].bet = int(ans.split()[1])
                    assert(self.bet < self.clients[k].bet)
                    self.bet = self.clients[k].bet
                    self.rise_client = k
                    self.bank += self.bet
                else:
                    assert(False)
            k = (k + 1) % len(self.clients)
        for client in self.clients:
            client.bet = 0

    def pre_flop(self):
        for i in range(2):
            self.dispense()
        self.bank += self.big_blind // 2
        self.bank += self.big_blind
        self.clients[0].bed = self.big_blind // 2
        self.clients[1].bed = self.big_blind
        self.clients[1].big_blind = True
        self.bet = self.big_blind
        return "Игрок " + str(self.clients[0].id) + " поставил " + str(self.big_blind // 2) + ", игрок " + str(self.clients[1].id) + " поставил " + str(self.big_blind)

    def flop(self):
        self.bet = 0
        self.roundRun()
        for i in range(3):
            self.table.append(self.getCard())
        print('flop', ' '.join(map(str, self.table[0: 3])))
        return ' '.join(map(str, self.table))

    def turn(self):
        self.bet = 0
        self.roundRun()
        self.table.append(self.getCard())
        print('turn', str(self.table[-1]))
        return str(self.table[-1])

    def river(self):
        self.bet = 0
        self.roundRun()
        self.table.append(self.getCard())
        print('river', str(self.table[-1]))
        return str(self.table[-1])

    def opening(self):
        self.bet = 0
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
        self.broadcast(self.pre_flop())
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
