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
        return self.rank + self.suit

    def rank_num(self):
        return ranks_numerical[self.rank]


