import random


ranks = ('A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2')
suits = ('h', 's', 'c', 'd')

ranks_numerical = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    '10': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}


class InvalidCard(Exception):
    pass


class Card(object):
    '''Simple card object'''
    def __init__(self, rank, suit):
        if rank not in ranks or suit not in suits:
            raise InvalidCard()
        self.rank = rank
        self.suit = suit

    def val(self):
        '''Returns a string representation of the Card object'''
        return self.rank + self.suit

    def rank_num(self):
        '''Returns a numerical representation of the Card rank'''
        return ranks_numerical[self.rank]


class InvalidHand(Exception):
    pass


class Hand(object):
    '''Hand class containing 2 cards'''
    def __init__(self, card1, card2):
        '''Initializes the Hand class with two given card objects'''
        if card1.rank == card2.rank and card1.suit == card2.suit:
            raise InvalidHand()
        self.card1 = card1
        self.card2 = card2

    def cards(self):
        '''Returns a tuple containing the two card objects'''
        return self.card1, self.card2


class Deck(object):
    '''Deck object that manages 52 cards'''
    def __init__(self, decks=1):
        self.cards = []
        for i in xrange(decks):
            for j in xrange(len(ranks)):
                for k in xrange(len(suits)):
                    self.cards.append(Card(rank=ranks[j], suit=suits[k]))

    def shuffle(self):
        '''Shuffles the cards that are currently in the deck'''
        random.shuffle(self.cards)

    def pop_card(self):
        '''Returns the card from the end of the deck'''
        return self.cards.pop()

    def pop_hand(self):
        '''Returns two cards from the end of the deck'''
        c1 = self.cards.pop()
        c2 = self.cards.pop()
        return c1, c2
