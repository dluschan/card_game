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

def compare(cards):
    for c in combinations:
        if c.check(cards):
            return c()

combinations = [StraightFlush, Quads, FullHouse, Flush, Straight, Set, TwoPairs, Pair, High]

Suits = [Diamonds, Clubs, Hearts, Spades]
cards = [Card(2, Diamonds), Card(5, Diamonds), Card(5, Diamonds), Card(5, Diamonds), Card(2, Diamonds)]
#cards = [Card(i, Diamonds) for i in range(2, 7)]

print(compare(cards))
print(' '.join(map(str, cards)))
