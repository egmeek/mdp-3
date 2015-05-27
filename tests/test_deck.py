import unittest
from game import Deck, ranks, suits


class TestDeck(unittest.TestCase):
    def test_init(self):
        d1 = Deck()
        self.assertEqual(len(d1.cards), 52)
        self.assertEqual(d1.cards[0].rank, ranks[0])
        self.assertEqual(d1.cards[0].suit, suits[0])
        self.assertEqual(d1.cards[-1].rank, ranks[-1])
        self.assertEqual(d1.cards[-1].suit, suits[-1])

    def test_shuffle(self):
        d1 = Deck()
        old = []
        for i in xrange(20):
            old.append(d1.cards[i].rank)
        d1.shuffle()
        same = True
        for i in xrange(20):
            if old[i] != d1.cards[i].rank:
                same = False
                break
        self.assertEqual(same, False)

    def test_pop_card(self):
        d1 = Deck()
        c1 = d1.pop_card()
        self.assertEqual(c1.rank, ranks[-1])
        self.assertEqual(c1.suit, suits[-1])

    def test_pop_hand(self):
        d1 = Deck()
        c1 = d1.pop_card()
        c2 = d1.pop_card()
        c3 = d1.pop_card()
        c4 = d1.pop_card()
        c5 = d1.pop_card()
        self.assertEqual(c1.rank, ranks[-1])
        self.assertEqual(c1.suit, suits[-1])
        self.assertEqual(c2.rank, ranks[-1])
        self.assertEqual(c2.suit, suits[-2])
        self.assertEqual(c3.rank, ranks[-1])
        self.assertEqual(c3.suit, suits[-3])
        self.assertEqual(c4.rank, ranks[-1])
        self.assertEqual(c4.suit, suits[-4])
        self.assertEqual(c5.rank, ranks[-2])
        self.assertEqual(c5.suit, suits[-1])
