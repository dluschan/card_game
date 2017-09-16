import socket
import diler
import cards
import network

class Game:
    def __init__(self):
        self.d = diler.Diler()
        self.clients = [] #[(conn, addr)]
        self.server = network.Server()

    def accept(self):
        self.clients.append(self.server.accept())
        print('Установлена связь с клиентом', self.clients[-1][1][1])
        self.send((self.clients[-1][0]), str(self.clients[-1][1][1]))

    def send(self, conn, msg):
        self.server.send(conn, msg)

    def recv(self, conn):
        return self.server.recv(conn)

    def dispense(self):
        for client in self.clients:
            self.send(client[0], str(self.d.request(client[1][1])))

game = Game()
ans = ''
while ans != 'q':
    print('a - установить соединение с новым клиентом')
    print('s - отправить всем клиентам по одной карте')
    print('q - quit')
    ans = input('Введите команду(a/w/s/q): ')
    if ans == 'a':
        game.accept()
    elif ans == 's':
        game.dispense()
    elif ans == 'q':
        print('By!')
        exit(0)
    else:
        print('Команда не распознана')
