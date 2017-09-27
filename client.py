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

    def round(self):
        mail = self.recv()
        while 'ask' in mail:
            while True:
                ans = input('сделайте ваш ход (pass(p)/call(c)/rise(r)): ')
                if ans == 'p':
                    self.send('pass')
                    break
                elif ans == 'c':
                    self.send('call')
                    break
                elif ans == 'r':
                    self.send('rise')
                    break
                else:
                    print('я вас не понимаю')
            mail = self.recv()
        print(mail)

    def game(self):
        for i in range(3):
            self.round()

    def main(self):
        if input('Подключиться к серверу (yes(y)/no(n))?: ').lower() == 'y':
            self.id = self.recv()
            print("Регистрация на сервере успешно выполнена.")
            self.wait()
            self.game()
        else:
            print('By!')
            exit(0)

player = Player()
