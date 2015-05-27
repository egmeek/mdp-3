import unittest
from game import Hand, InvalidHand, Card


class TestHands(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(InvalidHand):
            c1 = Card(rank='3', suit='c')
            c2 = Card(rank='3', suit='c')
            h = Hand(c1, c2)
        c1 = Card(rank='2', suit='c')
        c2 = Card(rank='3', suit='c')
        h = Hand(c1, c2)
        self.assertEqual(h.cards()[0].rank, '2')
        self.assertEqual(h.cards()[0].suit, 'c')
        self.assertEqual(h.cards()[1].rank, '3')
        self.assertEqual(h.cards()[0].suit, 'c')

    def test_cards(self):
        c1 = Card(rank='2', suit='c')
        c2 = Card(rank='3', suit='c')
        h = Hand(c1, c2)
        self.assertEqual(h.cards()[0].rank, '2')
        self.assertEqual(h.cards()[0].suit, 'c')
        self.assertEqual(h.cards()[1].rank, '3')
        self.assertEqual(h.cards()[0].suit, 'c')
