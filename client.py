import cards
import sender

class Client:
    def __init__(self):
        self.cards = []
        self.coins = 1000
        self.id = None
        self.server = None
        self.s = None

    def send(self, msg):
        if self.s is None:
            self.s = sender.Sender()
        self.s.send(msg)

    def recv(self):
        return self.s.recv()

player = Client()
ans = ''
while ans != 'q':
    print('r - registration')
    print('w - wait')
    print('s - show')
    print('q - quit')
    ans = input('Введите команду(r/w/s/q): ')
    if ans == 'r':
        player.send('Hi!')
        player.id = player.recv()
        print("Регистрация на сервере успешно выполнена", player.id)
    elif ans == 'w':
        print('Запрос карт')
        player.send('Request')
        while (len(player.cards)) < 2:
            player.cards.append(player.recv())
    elif ans == 'q':
        print('By!')
        exit(0)
    elif ans == 's':
        for c in player.cards:
            print(str(c))
    else:
        print('Команда не распознана')
