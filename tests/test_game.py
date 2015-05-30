import unittest
from collections import deque
from game import Player, Card, Hand, Deck
from poker import Table, Game


class SequencePlayer(Player):
    def __init__(self, name, br, hand, seq):
        super(SequencePlayer, self).__init__(name=name, bankroll=br, hand=hand)
        self.seq = seq

    def move(self, table):
        return self.seq.popleft()


class TestGame(unittest.TestCase):
    def setUp(self):
        import os
        if 'DEBUG' in os.environ:
            del os.environ['DEBUG']

    def test_2_player_quick_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()

        seq = deque([(6, 0), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)

        t = Table([p1, p2], bigblind=2, deck=d)
        t.dealer = 1

        g = Game(t)
        g.play()

        self.assertEqual(t.state, 0)
        self.assertEqual(p1.bankroll, 1499)
        self.assertEqual(p2.bankroll, 1501)

    def test_3_player_quick_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([(6, 0), (6, 0), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)
        p3 = SequencePlayer('C', 1500, h3, seq)

        t = Table([p1, p2, p3], bigblind=2, deck=d)
        t.dealer = 0
        g = Game(t)

        g.play()

        self.assertEqual(t.state, 0)
        self.assertEqual(p1.bankroll, 1500)
        self.assertEqual(p2.bankroll, 1499)
        self.assertEqual(p3.bankroll, 1501)

    def test_3_player_quick_bets_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([(2, 100), (3, 200), (4, 300), (6, 0), (6, 0), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)
        p3 = SequencePlayer('C', 1500, h3, seq)

        t = Table([p1, p2, p3], bigblind=100, deck=d)
        t.dealer = 0
        g = Game(t)

        g.play()

        self.assertEqual(t.state, 0)
        self.assertEqual(p1.bankroll, 1400)
        self.assertEqual(p2.bankroll, 1250)
        self.assertEqual(p3.bankroll, 1850)

    def test_3_player_long_preflop_bets_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([
            (2, 100), (2, 50), (3, 100), (2, 100), (4, 200),
            (2, 100), (2, 100), (6, 0), (6, 0), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)
        p3 = SequencePlayer('C', 1500, h3, seq)

        t = Table([p1, p2, p3], bigblind=100, deck=d)
        t.dealer = 2

        g = Game(t)
        g.play()

        self.assertEqual(t.state, 1)
        self.assertEqual(p1.bankroll, 1200)
        self.assertEqual(p2.bankroll, 1200)
        self.assertEqual(p3.bankroll, 2100)

    def test_2_player_long_turn_bets_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([(3, 200), (2, 150), (3, 100), (4, 200), (2, 100), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)

        t = Table([p1, p2], bigblind=100, deck=d)
        t.dealer = 0

        g = Game(t)
        g.play()

        self.assertEqual(t.state, 2)
        self.assertEqual(p1.bankroll, 1950)
        self.assertEqual(p2.bankroll, 1050)

    def test_2_player_long_river_bets_folds(self):
        d = Deck()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([
            (2, 100), (2, 50), (1, 0), (3, 100), (4, 200), (4, 300),
            (4, 400), (2, 300), (2, 200), (1, 0), (1, 0), (1, 0), (6, 0),
            (3, 100), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)
        p3 = SequencePlayer('B', 1500, h2, seq)

        t = Table([p1, p2, p3], bigblind=100, deck=d)
        t.dealer = 0

        g = Game(t)
        g.play()

        self.assertEqual(t.state, 3)
        self.assertEqual(p1.bankroll, 900)
        self.assertEqual(p2.bankroll, 900)
        self.assertEqual(p3.bankroll, 2700)

    def test_3_player_preflop_allin_folds(self):
        d = Deck()
        d.shuffle()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([(5, 1500), (5, 1450), (6, 0)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)
        p3 = SequencePlayer('C', 1500, h3, seq)

        t = Table([p1, p2, p3], bigblind=100, deck=d)
        t.dealer = 0

        g = Game(t)
        g.play()

        self.assertEqual(t.state, 4)
        self.assertEqual(p1.bankroll + p2.bankroll, 3100)

    def test_3_player_showdown1(self):
        d = Deck()
        d.shuffle()
        h1 = d.pop_hand()
        h2 = d.pop_hand()
        h3 = d.pop_hand()

        seq = deque([
            (2, 100), (2, 50), (1, 0), (3, 100), (4, 200), (4, 300),
            (4, 400), (2, 300), (2, 200), (1, 0), (1, 0), (1, 0), (6, 0),
            (3, 100), (2, 100)])

        p1 = SequencePlayer('A', 1500, h1, seq)
        p2 = SequencePlayer('B', 1500, h2, seq)
        p3 = SequencePlayer('C', 1500, h3, seq)

        t = Table([p1, p2, p3], bigblind=100, deck=d)
        t.dealer = 0

        g = Game(t)
        g.play()

        self.assertEqual(t.state, 4)
        self.assertEqual(p1.bankroll + p3.bankroll - 3000, 600)
        self.assertEqual(p2.bankroll, 900)
