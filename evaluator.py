class Evaluator(object):

    multiplier = {
        'STRAIGHT': 1000,



    }

    def __init__(self):
        pass

    def sort(hands, family_cards):
        '''Sorts the hands acording to standard hold'em rules.
        hands - [(player1, hand1), ... (playern, handn)]
        family_cards - the 5 family cards

        Returns a sorted list of players in descending order.
        '''
        pass

    def straight_value(self, cards):
        cards = sorted(cards, key=lambda x: x.rank_num(), reverse=True)
        for i in xrange(3):
            straight = True
            for j in xrange(4):
                print j
                if cards[j+i].rank_num() - 1 != cards[j+1+i].rank_num():
                    straight = False
                    break
            if straight:
                return self.multiplier['STRAIGHT'] + cards[j+i-3].rank_num()
        return 0



