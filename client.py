import cards
import sender

class Client:
    def __init__(self):
        self.cards = []
        self.coins = 1000
        self.id = None
        self.server = None
        self.s = sender.Sender()

    def send(self, msg):
        self.s.send(msg)

    def recv(self):
        return self.s.recv()

player = Client()
player.send('Hi!')
player.id = player.recv()
print(player.id)

for i in range(2):
    player.cards.append(player.recv())
for c in player.cards:
    print(str(c))
