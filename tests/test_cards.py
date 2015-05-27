import unittest
from game import Card, InvalidCard


class TestCards(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(InvalidCard):
            Card(rank='x', suit='h')
            Card(rank=13, suit='c')
            Card(rank='A', suit='x')
            Card(rank='K', suit=1)
        c = Card(rank='J', suit='s')
        self.assertEqual('J', c.rank)
        self.assertEqual('s', c.suit)

    def test_val(self):
        c = Card(rank='A', suit='h')
        self.assertEqual('Ah', c.val())
        c = Card(rank='8', suit='c')
        self.assertEqual('8c', c.val())

    def test_rank_num(self):
        c1 = Card(rank='K', suit='h')
        self.assertEqual(13, c1.rank_num())
        c2 = Card(rank='Q', suit='h')
        self.assertEqual(12, c2.rank_num())
        c3 = Card(rank='8', suit='h')
        self.assertEqual(8, c3.rank_num())
        self.assertGreater(c1.rank_num(), c2.rank_num())
        self.assertGreater(c2.rank_num(), c3.rank_num())
