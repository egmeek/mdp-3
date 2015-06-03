from unittest import TestCase
from game import Card, ranks, suits
from eval import Eval


class TestEval(TestCase):
    def test_check_straight_ok1(self):
        e = Eval()
        board = [
            Card('A', 's'),
            Card('K', 'c'),
            Card('Q', 'c'),
            Card('Q', 'd'),
            Card('J', 'c'),
            Card('T', 'c'),
        ]
        self.assertEquals(e.check_straight(board), True)
        self.assertEquals(e.relevant[0], Card('A', 's'))

    def test_check_straight_ok2(self):
        e = Eval()
        board = [
            Card('A', 's'),
            Card('K', 'c'),
            Card('Q', 'c'),
            Card('J', 'c'),
            Card('T', 'c'),
        ]
        self.assertEquals(e.check_straight(board), True)
        self.assertEquals(e.relevant[0], Card('A', 's'))

    def test_check_straight_ok3(self):
        e = Eval()
        board = [
            Card('A', 's'),
            Card('K', 'c'),
            Card('Q', 'h'),
            Card('Q', 's'),
            Card('Q', 'c'),
            Card('J', 'c'),
            Card('T', 'c'),
        ]
        self.assertEquals(e.check_straight(board), True)
        self.assertEquals(e.relevant[0], Card('A', 's'))

    def test_check_straight_bad(self):
        e = Eval()
        board = [
            Card('A', 's'),
            Card('K', 'c'),
            Card('J', 'c'),
            Card('J', 'h'),
            Card('T', 'c'),
        ]
        self.assertEquals(e.check_straight(board), False)
        self.assertEquals(e.relevant, [])

    def test_check_straight_bad2(self):
        e = Eval()
        board = [
            Card('A', 's'),
            Card('K', 'c'),
            Card('Q', 'c'),
            Card('J', 'h'),
            Card('9', 'c'),
        ]
        self.assertEquals(e.check_straight(board), False)
        self.assertEquals(e.relevant, [])

    def test_check_straight_bad3(self):
        e = Eval()
        board = [
            Card('K', 's'),
            Card('K', 'c'),
            Card('Q', 'c'),
            Card('J', 'h'),
            Card('T', 'c'),
        ]
        self.assertEquals(e.check_straight(board), False)
        self.assertEquals(e.relevant, [])

    def test_check_straight_many(self):
        e = Eval()
        for i in xrange(len(ranks) - 4):
            board = []
            for j in xrange(5):
                board.append(Card(ranks[i+j], 'h'))
            self.assertEqual(e.check_straight(board), True)
            self.assertEqual(e.relevant[0], Card(ranks[i], 'h'))

    def test_check_straight_many_bad(self):
        e = Eval()
        for i in xrange(len(ranks) - 4):
            board = []
            for j in xrange(5):
                if j is 4:
                    board.append(Card(ranks[i+j-1], 'h'))
                else:
                    board.append(Card(ranks[i+j], 'h'))
            self.assertEqual(e.check_straight(board), False)
            self.assertEqual(e.relevant, [])

    def test_check_straight_many_7(self):
        e = Eval()
        for i in xrange(len(ranks) - 4):
            board = []
            for j in xrange(5):
                board.append(Card(ranks[i+j], 'h'))
            board += [Card('A', 's'), Card('7', 'c')]
            self.assertEqual(e.check_straight(board), True)
            self.assertEqual(e.relevant[0], Card(ranks[i], 'h'))

    def test_check_straight_many_bad_7(self):
        e = Eval()
        for i in xrange(len(ranks) - 4):
            board = []
            for j in xrange(5):
                if j is 4:
                    board.append(Card(ranks[i+j], 'h'))
                else:
                    board.append(Card(ranks[i+j], 'h'))
            board += [Card('T', 's')]
            board = [Card('2', 'd')] + board
            board[3] = board[2]
            self.assertEqual(e.check_straight(board), False)
            self.assertEqual(e.relevant, [])

    def test_flush_bad(self):
        e = Eval()
        board = [
            Card('K', 's'),
            Card('K', 'c'),
            Card('Q', 'c'),
            Card('J', 'h'),
            Card('T', 'c'),
        ]
        self.assertEquals(e.check_flush(board), False)
        self.assertEquals(e.relevant, [])

    def test_flush_ok(self):
        e = Eval()
        board = [
            Card('6', 's'),
            Card('K', 's'),
            Card('Q', 's'),
            Card('J', 's'),
            Card('T', 's'),
        ]
        self.assertEquals(e.check_flush(board), True)
        self.assertEquals(e.relevant, board)

    def test_flush_ok(self):
        e = Eval()
        board = [
            Card('6', 's'),
            Card('K', 's'),
            Card('Q', 's'),
            Card('J', 's'),
            Card('T', 's'),
            Card('7', 's'),
        ]
        self.assertEquals(e.check_flush(board), True)
        self.assertEquals(e.relevant, board[:-1])

    def test_flush_ok2(self):
        e = Eval()
        board = [
            Card('6', 's'),
            Card('K', 's'),
            Card('Q', 's'),
            Card('J', 'h'),
            Card('T', 's'),
            Card('7', 's'),
        ]
        self.assertEquals(e.check_flush(board), True)
        board.remove(Card('J', 'h'))
        self.assertEquals(e.relevant, board)

    def test_flush_ok3(self):
        e = Eval()
        board = [
            Card('6', 's'),
            Card('K', 'd'),
            Card('Q', 's'),
            Card('J', 'h'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_flush(board), True)
        board.remove(Card('J', 'h'))
        board.remove(Card('K', 'd'))
        self.assertEquals(e.relevant, board)

    def test_flush_bad2(self):
        e = Eval()
        board = [
            Card('6', 'd'),
            Card('K', 'd'),
            Card('Q', 's'),
            Card('J', 'h'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_flush(board), False)
        board.remove(Card('J', 'h'))
        board.remove(Card('K', 'd'))
        self.assertEquals(e.relevant, [])

    def test_flush_ok4(self):
        e = Eval()
        board = [
            Card('6', 's'),
            Card('K', 's'),
            Card('Q', 's'),
            Card('J', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_flush(board), True)
        self.assertEquals(e.relevant, board[:5])

    def test_4kind_ok(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('6', 'h'),
            Card('6', 'd'),
            Card('6', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_pairs(board), True)
        self.assertEquals(e.relevant, board[:4])

    def test_4kind_ok(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('6', 'h'),
            Card('6', 'd'),
            Card('6', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_4(board), True)
        self.assertEquals(e.relevant, board[:4] + [Card('T', 's')])

    def test_4kind_ok2(self):
        e = Eval()
        board = [
            Card('Q', 's'),
            Card('6', 'c'),
            Card('6', 'h'),
            Card('T', 's'),
            Card('6', 's'),
            Card('6', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_4(board), True)
        board.remove(Card('T', 's'))
        board.remove(Card('2', 's'))
        self.assertEquals(e.relevant, board[1:] + [board[0]])

    def test_4kind_bad(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('6', 'h'),
            Card('6', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_4(board), False)
        self.assertEquals(e.relevant, [])

    def test_full_bad1(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('6', 'h'),
            Card('6', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_full(board), False)
        self.assertEquals(e.relevant, [])

    def test_full_bad2(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('2', 'h'),
            Card('6', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_full(board), False)
        self.assertEquals(e.relevant, [])

    def test_full_ok1(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('6', 'h'),
            Card('6', 's'),
            Card('T', 's'),
            Card('7', 's'),
            Card('2', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_full(board), True)
        board.remove(Card('T', 's'))
        board.remove(Card('7', 's'))
        self.assertEquals(e.relevant, board)

    def test_full_ok2(self):
        e = Eval()
        board = [
            Card('6', 'c'),
            Card('6', 'h'),
            Card('6', 's'),
            Card('T', 's'),
            Card('2', 'c'),
            Card('2', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_full(board), True)
        board.remove(Card('T', 's'))
        board.remove(Card('2', 's'))
        self.assertEquals(e.relevant, board)

    def test_full_ok3(self):
        e = Eval()
        board = [
            Card('A', 'c'),
            Card('9', 'h'),
            Card('9', 's'),
            Card('9', 's'),
            Card('6', 'c'),
            Card('6', 'd'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_full(board), True)
        board = [
            Card('9', 'h'),
            Card('9', 's'),
            Card('9', 's'),
            Card('6', 'c'),
            Card('6', 'd'),
        ]
        self.assertEquals(e.relevant, board)

    def test_full_ok3(self):
        e = Eval()
        board = [
            Card('A', 'c'),
            Card('4', 'h'),
            Card('4', 's'),
            Card('3', 's'),
            Card('3', 'c'),
            Card('3', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_full(board), True)
        board = [
            Card('3', 's'),
            Card('3', 'c'),
            Card('3', 'd'),
            Card('4', 'h'),
            Card('4', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_full_ok_many1(self):
        e = Eval()
        board = []
        for i in xrange(len(ranks) - 2):
            for j in xrange(i + 1, len(ranks)):
                board = []
                board2 = []
                for s in suits[:-1]:
                    board.append(Card(ranks[i], s))
                for s in suits[:-2]:
                    board.append(Card(ranks[j], s))
                self.assertEquals(e.check_full(board), True)
                self.assertEquals(e.relevant, board)

    def test_full_ok_many2(self):
        e = Eval()
        board = []
        for i in xrange(len(ranks) - 2):
            for j in xrange(i + 1, len(ranks)):
                board = []
                board2 = []
                for s in suits[:-2]:
                    board.append(Card(ranks[i], s))
                for s in suits[:-1]:
                    board.append(Card(ranks[j], s))
                self.assertEquals(e.check_full(board), True)
                self.assertEquals(e.relevant, board[2:] + board[:2])

    def test_kind_3_ok(self):
        e = Eval()
        board = [
            Card('A', 'c'),
            Card('9', 'h'),
            Card('8', 's'),
            Card('3', 's'),
            Card('3', 'c'),
            Card('3', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_3(board), True)
        board = [
            Card('3', 's'),
            Card('3', 'c'),
            Card('3', 'd'),
            Card('A', 'c'),
            Card('9', 'h'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_3_ok2(self):
        e = Eval()
        board = [
            Card('A', 'c'),
            Card('A', 'h'),
            Card('A', 's'),
            Card('6', 's'),
            Card('5', 'c'),
            Card('3', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_3(board), True)
        board = [
            Card('A', 'c'),
            Card('A', 'h'),
            Card('A', 's'),
            Card('6', 's'),
            Card('5', 'c'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_3_ok3(self):
        e = Eval()
        board = [
            Card('A', 'c'),
            Card('Q', 'h'),
            Card('T', 's'),
            Card('6', 's'),
            Card('5', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
        ]
        self.assertEquals(e.check_kind_3(board), True)
        board = [
            Card('5', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('A', 'c'),
            Card('Q', 'h'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_3_ok4(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('6', 's'),
            Card('5', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
        ]
        self.assertEquals(e.check_kind_3(board), True)
        board = [
            Card('5', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('T', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_3_bad1(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('6', 's'),
            Card('6', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
        ]
        self.assertEquals(e.check_kind_3(board), False)
        self.assertEquals(e.relevant, [])

    def test_kind_3_bad2(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('6', 's'),
            Card('6', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('3', 's'),
        ]
        self.assertEquals(e.check_kind_3(board), False)
        self.assertEquals(e.relevant, [])

    def test_kind_2_2_ok(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('6', 's'),
            Card('6', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), True)
        board = [
            Card('6', 's'),
            Card('6', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_2_2_ok2(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('6', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), True)
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('6', 'c'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_2_2_ok3(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('6', 'c'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('2', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), True)
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('5', 'd'),
            Card('5', 's'),
            Card('6', 'c'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_2_2_ok4(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('7', 'c'),
            Card('6', 'd'),
            Card('5', 's'),
            Card('2', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), True)
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('2', 's'),
            Card('2', 's'),
            Card('7', 'c'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_2_2_bad1(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('7', 'c'),
            Card('6', 'd'),
            Card('5', 's'),
            Card('4', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), False)
        self.assertEquals(e.relevant, [])

    def test_kind_2_2_bad2(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('7', 'c'),
            Card('6', 'd'),
            Card('5', 's'),
            Card('5', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), False)
        self.assertEquals(e.relevant, [])

    def test_kind_2_2_bad3(self):
        e = Eval()
        board = [
            Card('7', 'c'),
            Card('6', 'd'),
            Card('5', 's'),
            Card('5', 's'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2_2(board), False)
        self.assertEquals(e.relevant, [])

    def test_kind_2_ok1(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('6', 'c'),
            Card('4', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2(board), True)
        board = [
            Card('T', 's'),
            Card('T', 's'),
            Card('6', 'c'),
            Card('4', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_2_ok2(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('8', 's'),
            Card('6', 'c'),
            Card('4', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2(board), True)
        board = [
            Card('8', 's'),
            Card('8', 's'),
            Card('T', 's'),
            Card('9', 's'),
            Card('6', 'c'),
        ]
        self.assertEquals(e.relevant, board)

    def test_kind_2_bad(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 'c'),
            Card('4', 'd'),
            Card('2', 's'),
        ]
        self.assertEquals(e.check_kind_2(board), False)
        self.assertEquals(e.relevant, [])

    def test_royal_ok1(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_ok2(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 'd'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_ok3(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
            Card('5', 's'),
            Card('4', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_ok4(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 'h'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
            Card('5', 's'),
            Card('4', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('8', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_ok5(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('9', 'c'),
            Card('9', 'd'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_ok6(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 'h'),
            Card('9', 'h'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_ok7(self):
        e = Eval()
        board = [
            Card('T', 'h'),
            Card('T', 's'),
            Card('9', 'h'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), True)
        board = [
            Card('T', 's'),
        ]
        self.assertEquals(e.relevant, board)

    def test_royal_bad(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('9', 'c'),
            Card('9', 'd'),
            Card('8', 'c'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), False)
        self.assertEquals(e.relevant, [])

    def test_royal_bad2(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('6', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), False)
        self.assertEquals(e.relevant, [])

    def test_royal_bad3(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 's'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 'h'),
            Card('5', 's'),
        ]
        self.assertEquals(e.check_royal(board), False)
        self.assertEquals(e.relevant, [])

    def test_royal_bad4(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 'c'),
            Card('9', 'd'),
            Card('9', 'h'),
            Card('8', 's'),
            Card('7', 's'),
            Card('6', 's'),
        ]
        self.assertEquals(e.check_royal(board), False)
        self.assertEquals(e.relevant, [])

    def test_get_strength(self):
        e = Eval()
        board = [
            Card('T', 's'),
            Card('T', 'd'),
            Card('9', 'd'),
            Card('9', 'h'),
            Card('2', 's'),
            Card('7', 'c'),
            Card('6', 'c'),
        ]
        self.assertEqual(e.get_strength(board), (7, [
            Card('T', 's'),
            Card('T', 'd'),
            Card('9', 'd'),
            Card('9', 'h'),
            Card('7', 'c'),
        ]))

        e = Eval()
        board = [
            Card('T', 's'),
            Card('9', 'd'),
            Card('7', 'd'),
            Card('6', 'h'),
            Card('4', 's'),
            Card('3', 'c'),
            Card('2', 'c'),
        ]
        self.assertEqual(e.get_strength(board), (9, [
            Card('T', 's'),
            Card('9', 'd'),
            Card('7', 'd'),
            Card('6', 'h'),
            Card('4', 's'),
        ]))
