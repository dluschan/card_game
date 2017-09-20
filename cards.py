class Suit:
    pass

class Diamonds(Suit):
    def __str__(self):
        return '♢'

class Clubs(Suit):
    def __str__(self):
        return '♧'

class Hearts(Suit):
    def __str__(self):
        return '♡'

class Spades(Suit):
    def __str__(self):
        return '♤'

class Value:
    value_map = {0: 'A', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '10', 10: 'J', 11: 'Q', 12: 'K'}
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return Value.value_map[self.value]

class Card:
    def __init__(self, value, suit):
        self.suit = suit()
        self.value = Value(value)

    def __str__(self):
        return ('\033[31m' if type(self.suit) in [Diamonds, Hearts] else '') + str(self.value) + str(self.suit) + ('\033[0m' if type(self.suit) in [Diamonds, Hearts] else '')

Suits = [Diamonds, Clubs, Hearts, Spades]

def createCards():
    cards = []
    for s in Suits:
        for v in range(13):
            cards.append(Card(v, s))
    return cards
