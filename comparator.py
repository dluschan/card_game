from random import choice
from cards import *

class Flush:
    def __str__(self):
        return "Flush"

    def check(cards):
        suits = {c.suit for c in cards}
        return len(suits) == 1

class Pair:
    def __str__(self):
        return "Pair"

    def check(cards):
        nom = {}
        for v in map(lambda x: x.value.value, cards):
            nom[v] = nom.get(v, 0) + 1
        return len(nom) == 4

class TwoPairs:
    def __str__(self):
        return "TwoPairs"

    def check(cards):
        nom = {}
        for v in map(lambda x: x.value.value, cards):
            nom[v] = nom.get(v, 0) + 1
        return len(nom) == 3 and max(nom.values()) == 2 and min(nom.values()) == 1

class Set:
    def __str__(self):
        return "Set"

    def check(cards):
        nom = {}
        for v in map(lambda x: x.value.value, cards):
            nom[v] = nom.get(v, 0) + 1
        return len(nom) == 3 and max(nom.values()) == 3 and min(nom.values()) == 1

class FullHouse:
    def __str__(self):
        return "FullHouse"

    def check(cards):
        nom = {}
        for v in map(lambda x: x.value.value, cards):
            nom[v] = nom.get(v, 0) + 1
        return len(nom) == 2 and max(nom.values()) == 3

class Quads:
    def __str__(self):
        return "Quads"

    def check(cards):
        nom = {}
        for v in map(lambda x: x.value.value, cards):
            nom[v] = nom.get(v, 0) + 1
        return len(nom) == 2 and max(nom.values()) == 4

class Straight:
    def __str__(self):
        return "Straight"

    def check(cards):
        s = list(map(lambda x: x.value.value, cards))
        return not Pair.check(cards) and max(s) - min(s) == 4

class High:
    def check(cards):
        return True

class StraightFlush():
    def __str__(self):
        return "StraightFlush"

    def check(cards):
        return Straight.check(cards) and Flush.check(cards)

combinations = [StraightFlush, Quads, FullHouse, Flush, Straight, Set, TwoPairs, Pair, High]

class Comparator:
    def combine(self, cards):
        r = []
        for i in range(6):
            for j in range(i + 1, 7):
                 r.append(cards[:i] + cards[i + 1: j] + cards[j + 1:])
        return r

    def compare(self, clients, table):
        res = {}
        for client_id, cards in clients:
            res[max(map(max_combine, combine(cards + table)))].append(client_id)
        ans = []
        for key in sorted(res):
            ans.append(res[key])
        return ans

    def max_combine(cards):
        for c in combinations:
            if c.check(cards):
                return c()

Suits = [Diamonds, Clubs, Hearts, Spades]

cards = [
        Card(2, Diamonds),
        Card(5, Diamonds),
        Card(9, Diamonds),
        Card(11, Diamonds),
        Card(0, Diamonds),
        Card(2, Hearts),
        Card(5, Hearts),
        Card(5, Clubs),
        Card(5, Clubs),
        Card(2, Clubs)
]

#cards = [Card(i, Diamonds) for i in range(2, 7)]

print(*cards)
