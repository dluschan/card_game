import cards
import network

class Player:
    def __init__(self):
        self.cards = []
        self.coins = 1000
        self.id = None
        self.server = None
        self.s = None

    def send(self, msg):
        if self.s is None:
            self.s = network.Client()
        self.s.send(msg)

    def recv(self):
        return self.s.recv()

player = Player()
ans = ''
while ans != 'q':
    print('r - registration')
    print('w - wait')
    print('s - show')
    print('q - quit')
    ans = input('Введите команду(r/w/s/q): ')
    if ans == 'r':
        player.send('Hello')
        player.id = player.recv()
        print("Регистрация на сервере успешно выполнена", player.id)
    elif ans == 'w':
        print('Ожидание карт')
        player.cards.append(player.recv())
        print('Получена карта', player.cards[-1])
    elif ans == 'q':
        print('By!')
        exit(0)
    elif ans == 's':
        for c in player.cards:
            print(str(c))
    else:
        print('Команда не распознана')
