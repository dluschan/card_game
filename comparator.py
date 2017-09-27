from random import choice

class Comparator:
    def compare(self, clients, table):
        return [choice(list(clients.keys()))]
