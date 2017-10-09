import diler
import cards
import network
import socket
import os
import time

class Game:
    def __init__(self):
        self.d = diler.Diler(self)
        self.logins = {}
        self.money = 10000
        self.clients = [] #[(conn, addr)]
        self.server = network.Server()
        try:
            self.f = open('file.txt', 'a')
        except IOError as e:
            print('Файла с логинами не существует!')
            print('Создаю новый файл')
            self.f = open('file.txt', 'w+')
        self.main()

    def main(self):
        ans = ''
        while ans != 'q':
            print('a - установить соединение с новым клиентом')
            print('s - начать игру')
            print('q - quit')
            ans = input('Введите команду(a/w/s/q): ')
            if ans == 'a':
                try:
                    self.accept()
                except socket.timeout:
                    print('Клиент не отвечает')
                    continue
            elif ans == 's':
                self.start()
            elif ans == 'q':
                print('By!')
                self.f = open('file.txt', 'w')
                for log, mon in self.logins.items():
                    self.f.write(log + '.' + str(mon) + '\n')
                self.f.close()
                exit(0)
            else:
                print('Команда не распознана')

    def fromFiletoDict(self, File):
        for line in open(File.name):
            if os.stat("file").st_size == 0:
                break
            self.logins[line[:line.index('.')]] = line[line.index('.')+1:]

    def accept(self):
        self.money = 10000
        self.clients.append(self.server.accept())
        print('Установлена связь с клиентом', self.clients[-1][1][1])
        self.send((self.clients[-1][0]), 'Введите ваш логин:')
        s = self.recv(self.clients[-1][0])
        print('Clients Login = ' + s)
        try: #проверяем сущесвтование файла
            self.f = open('file.txt')
            self.fromFiletoDict(self.f)
            if not(s in self.logins.keys()):
                self.send(self.clients[-1][0], 'Добро пожаловать, новый игрок')
                self.logins[s] = self.money #10000 - изначальное кол-во денег
            else:
                self.money = int(self.logins[s])
                self.send(self.clients[-1][0], 'Добро пожаловать ' + s)
        except FileNotFoundError as e:
            if not(s in self.logins):
                self.send(self.clients[-1][0], 'Добро пожаловать, новый игрок')
                self.logins[s] = self.money #10000 - изначальное кол-во денег
        time.sleep(0.01)
        self.send(self.clients[-1][0], str(self.money))
        self.recv(self.clients[-1][0])
        self.send((self.clients[-1][0]), str(self.clients[-1][1][1]))

    def send(self, conn, msg):
        self.server.send(conn, msg)

    def recv(self, conn):
        return self.server.recv(conn)

    def start(self):
        for i in range(2):
            self.dispense()
        self.d.game()

    def dispense(self):
        for client in self.clients:
            self.send(client[0], str(self.d.request(client)))

game = Game()
