import cards
import network

class Player:
    def __init__(self):
        self.cards = []
        self.coins = 1000
        self.id = None
        self.server = None
        self.s = None
        self.main()

    def send(self, msg):
        if self.s is None:
            self.s = network.Client()
        self.s.send(msg)

    def recv(self):
        if self.s is None:
            self.s = network.Client()
        return self.s.recv()

    def wait(self):
        print('Ожидание карт')
        for i in range(2):
            self.cards.append(self.recv())
            print('Получена карта', self.cards[-1])

    def game(self):
        print(self.recv())
        print(self.recv())
        print(self.recv())

    def main(self):
        if input('Подключиться к серверу? (y or n)').lower() == 'y':
            self.send('Hello')
            self.id = self.recv()
            print("Регистрация на сервере успешно выполнена.")
            self.wait()
            self.game()
        else:
            print('By!')
            exit(0)

player = Player()
