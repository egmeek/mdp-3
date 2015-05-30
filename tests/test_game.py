import unittest
from game import Player, Card, Hand, Deck
from poker import Table, Game


class SequencePlayer(Player):
    def __init__(self, name, br, hand):
        super(SequencePlayer, self).__init__(name=name, bankroll=br, hand=hand)
        self.it = 0

    def move(self, table):
        m, amt = self.moves(self.it)
        self.it += 1
        return m, amt


class SequencePlayerA(SequencePlayer):
    def moves(self, it):
        seq = {
            0: (6, 0),
            1: (6, 0),
        }
        return seq[it]


class SequencePlayerB(SequencePlayer):
    def moves(self, it):
        seq = {
            0: (6, 0),
            1: (6, 0),
        }
        return seq[it]


class SequencePlayerC(SequencePlayer):
    def moves(self, it):
        seq = {
            0: (6, 0),
            1: (6, 0),
        }
        return seq[it]


class TestGame(unittest.TestCase):
    def test_2_player_quick_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        p1 = SequencePlayerA('A', 1500, h1)
        p2 = SequencePlayerB('B', 1500, h2)
        p3 = SequencePlayerC('C', 1500, h3)

        t = Table([p1, p2, p3], bigblind=1, deck=d)
        t.dealer = 0
        g = Game(t)

        g.play()
