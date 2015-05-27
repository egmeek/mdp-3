import unittest
from game import Player


class TestPlayer(unittest.TestCase):
    def test_init(self):
        p1 = Player(name='Jimmy')
        self.assertEqual('Jimmy', p1.name)
        p2 = Player()
        self.assertEqual('John Doe', p2.name)
