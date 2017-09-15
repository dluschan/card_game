import socket
import diler
import cards

class Server:
    def __init__(self):
        self.clients = {}
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('127.0.0.1', 1234))
        self.s.listen(5)

    def send(self, msg):
        conn, addr = self.s.accept()
        conn.send(msg.encode('utf-8'))

    def recv(self, size = 1024):
        conn, addr = self.s.accept()
        return conn.recv(size).decode('utf-8')

    def waitClient(self):
        if self.recv() == 'Hi!':
            client_id = len(self.clients)
            self.clients.append(client_id)
            print('Появился клиент', client_id)
            self.send(str(client_id))
            for i in range(2):
                self.send(str(d.getCard()))
            print('done')

    def sendCard(self):
        pass

d = diler.Diler()
server = Server()
while len(server.clients()) < 2:
    server.waitClient()
    server.sendCard()
