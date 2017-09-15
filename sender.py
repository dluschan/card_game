import socket
import sys

class Sender:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 1234))

    def send(self, data):
        self.s.send(data.encode('utf-8'))

    def recv(self, size = 1024):
        #"""Получение посылки заданного размера от сервера"""
        return self.s.recv(size).decode('utf-8')
