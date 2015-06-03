import unittest
from poker import Table
from players import Player


class TestTable(unittest.TestCase):
    def setUp(self):
        import os
        if 'DEBUG' in os.environ:
            del os.environ['DEBUG']

    def create_table(self, players=2):
        player_list = []
        for i in xrange(players):
            name = 'Player%s' % i
            player_list.append(Player(name=name))
        t = Table(player_list)
        return t

    def test_init(self):
        p1 = Player(name='A')
        p2 = Player(name='B')
        t = Table([p1, p2])
        bets = {
            0: {p1: [], p2: []}, 
            1: {p1: [], p2: []}, 
            2: {p1: [], p2: []}, 
            3: {p1: [], p2: []}, 
        }
        self.assertEqual(t.bets, bets)
        self.assertIn(t.dealer, (0, 1))
        self.assertEqual(t.nr_players, 2)

    def test_next_dealer(self):
        t = self.create_table(2)
        dealer = t.dealer
        self.assertIn(dealer, range(t.nr_players))
        self.assertEqual(t.next_dealer(), (dealer + 1) % t.nr_players)
        dealer = t.dealer
        t.next_dealer()
        t.next_dealer()
        self.assertEqual(t.next_dealer(), (dealer + 3) % t.nr_players)


        t = self.create_table(6)
        dealer = t.dealer
        self.assertIn(dealer, range(t.nr_players))
        self.assertEqual(t.next_dealer(), (dealer + 1) % t.nr_players)
        dealer = t.dealer
        for _ in xrange(53):
            t.next_dealer()
        self.assertEqual(t.next_dealer(), (dealer + 54) % t.nr_players)

    def test_next_player_id(self):
        t = self.create_table(2)
        t.current_player = 1
        self.assertEqual(t.next_player_id(), (2 % t.nr_players))
        
        t = self.create_table(2)
        t.current_player = 0
        self.assertEqual(t.next_player_id(), (1 % t.nr_players))

        t = self.create_table(7)
        cp = 3
        t.current_player = cp
        for _ in xrange(23):
            t.next_player_id()
        self.assertEqual(t.current_player, (3 + 23) % t.nr_players)

    def test_next_player(self):
        t = self.create_table(2)
        current = 1
        t.current_player = current
        p = None
        for _ in xrange(4):
            p = t.next_player()
        self.assertEqual(p, t.players[(current + 4) % t.nr_players])

        t = self.create_table(8)
        current = 4
        t.current_player = current
        p = None
        for _ in xrange(25):
            p = t.next_player()
        self.assertEqual(p, t.players[(current + 25) % t.nr_players])

    def test_players_active(self):
        t = self.create_table(2)
        t.players_fold = 2
        self.assertEqual(t.players_active(), 0)

        t = self.create_table(2)
        t.players_fold = 0
        t.players_allin = 1
        self.assertEqual(t.players_active(), 1)

        t = self.create_table(5)
        t.players_fold = 1
        t.players_allin = 2
        self.assertEqual(t.players_active(), 2)

    def test_players_in_hand(self):
        t = self.create_table(5)
        t.players_fold = 2
        t.players_allin = 2
        self.assertEqual(t.players_in_hand(), 3)

        t = self.create_table(2)
        t.players_fold = 0
        t.players_allin = 1
        self.assertEqual(t.players_in_hand(), 2)

    def test_to_pay(self):
        t = self.create_table(2)
        p1, p2 = t.players
        model = {p1: [150, 100, 25], p2: []}
        t.bets[0] = model
        self.assertEquals(t.to_pay(p2), 275)
        self.assertEquals(t.to_pay(p1), 0)

        t = self.create_table(4)
        p1, p2, p3, p4 = t.players
        model = {
            p1: [150, 100, 25], p2: [100], p3: [10, 100], p4:[150, 100, 25]}
        t.bets[0] = model
        self.assertEquals(t.to_pay(p1), 0)
        self.assertEquals(t.to_pay(p2), 175)
        self.assertEquals(t.to_pay(p3), 165)
        self.assertEquals(t.to_pay(p4), 0)

        t = self.create_table(4)
        p1, p2, p3, p4 = t.players
        model = {
            p1: [1], p2: [1], p3: [1], p4:[1]}
        t.bets[0] = model
        self.assertEquals(t.to_pay(p1), 0)
        self.assertEquals(t.to_pay(p2), 0)
        self.assertEquals(t.to_pay(p3), 0)
        self.assertEquals(t.to_pay(p4), 0)

        t = self.create_table(4)
        t.state = 3
        p1, p2, p3, p4 = t.players
        model = {
            p1: [100, 100, 100, 100], p2: [100, 100, 100],
            p3: [100, 100], p4:[100]}
        t.bets[3] = model
        self.assertEquals(t.to_pay(p1), 0)
        self.assertEquals(t.to_pay(p2), 100)
        self.assertEquals(t.to_pay(p3), 200)
        self.assertEquals(t.to_pay(p4), 300)

        t = self.create_table(4)
        t.state = 3
        p1, p2, p3, p4 = t.players
        model = {
            p1: [], p2: [],
            p3: [], p4:[100, 200]}
        t.bets[3] = model
        self.assertEquals(t.to_pay(p1), 300)
        self.assertEquals(t.to_pay(p2), 300)
        self.assertEquals(t.to_pay(p3), 300)
        self.assertEquals(t.to_pay(p4), 0)

        t = self.create_table(4)
        t.state = 3
        p1, p2, p3, p4 = t.players
        model = {
            p1: [], p2: [],
            p3: [], p4:[]}
        t.bets[3] = model
        self.assertEquals(t.to_pay(p1), 0)
        self.assertEquals(t.to_pay(p2), 0)
        self.assertEquals(t.to_pay(p3), 0)
        self.assertEquals(t.to_pay(p4), 0)
