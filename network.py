import socket

class Connection:
    timeout = 5
    adress = '127.0.0.1'
    port = 1234
    players = 2
    coding = 'utf-8'

class Client:
    """Сетевая часть клиента.
    Занимается созданием и подключением сокета, а также отправкой и получением сообщений через него."""
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((Connection.adress, Connection.port))

    def send(self, msg):
        """Отправка сообщения на сервера"""
        self.s.send(msg.encode(Connection.coding))

    def recv(self, size = 1024):
        """Получение сообщения заданного размера от сервера"""
        return self.s.recv(size).decode(Connection.coding)

class Server:
    """Сетевая часть сервера.
    Занимается созданием сокета, установлением связи с клиентами, а также и получением и отправкой им сообщений."""
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(Connection.timeout)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((Connection.adress, Connection.port))
        self.socket.listen(Connection.players)

    def accept(self):
        "Установление связи с клиентом"
        return self.socket.accept()

    def send(self, conn, msg):
        "Отправка сообщения на клиент"
        conn.send(msg.encode(Connection.coding))

    def recv(self, conn, size = 1024):
        "Получение сообщения заданного размера от клиента"
        return conn.recv(size).decode(Connection.coding)
