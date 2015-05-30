import unittest
from evaluator import Evaluator
from game import Card


class TestEvaluator(unittest.TestCase):
    def test_straight_value_ok(self):
        c1 = Card('A', 's')
        c2 = Card('K', 'c')
        c3 = Card('9', 's')
        c4 = Card('7', 'c')
        c5 = Card('Q', 's')
        c6 = Card('J', 'c')
        c7 = Card('10', 's')
        e = Evaluator()
        self.assertEqual(e.straight_value(
            [c1, c2, c3, c4, c5, c6, c7]
        ), e.multiplier['STRAIGHT'] + 14)
        
        c1 = Card('8', 's')
        c2 = Card('K', 'c')
        c3 = Card('9', 's')
        c4 = Card('7', 'c')
        c5 = Card('Q', 's')
        c6 = Card('J', 'c')
        c7 = Card('10', 's')
        e = Evaluator()
        self.assertEqual(e.straight_value(
            [c1, c2, c3, c4, c5, c6, c7]
        ), e.multiplier['STRAIGHT'] + 13)

        c1 = Card('8', 's')
        c2 = Card('4', 'c')
        c3 = Card('A', 's')
        c4 = Card('7', 'c')
        c5 = Card('5', 's')
        c6 = Card('J', 'c')
        c7 = Card('6', 's')
        e = Evaluator()
        self.assertEqual(e.straight_value(
            [c1, c2, c3, c4, c5, c6, c7]
        ), e.multiplier['STRAIGHT'] + 8)

        c1 = Card('8', 's')
        c2 = Card('9', 'c')
        c3 = Card('7', 's')
        c4 = Card('6', 'c')
        c5 = Card('5', 's')
        c6 = Card('5', 'c')
        c7 = Card('3', 's')
        e = Evaluator()
        self.assertEqual(e.straight_value(
            [c1, c2, c3, c4, c5, c6, c7]
        ), e.multiplier['STRAIGHT'] + 9)
