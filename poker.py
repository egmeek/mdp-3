import sys
from os import environ
from random import randint
from game import Card, Hand, Deck, Player, player_states
from players import DeterministicPlayer
from deuces.deuces import Card as DCard, Evaluator
from qlearning import QLearning


def log(msg):
    if environ.get('DEBUG'):
        print msg


game_states = {
    0: 'PREFLOP',
    1: 'FLOP',
    2: 'TURN',
    3: 'RIVER',
    4: 'SHOWDOWN',
}


class Table(object):
    '''
    Class responsable for the information available to all players. What
    part of the game were in, bets, pots, winners etc.
    When a player needs to make a decision, the Player object receives an
    instance of the Table class that contains all the necessary information
    to make one.

    bets = {0: {player1: [100, 200], player2: [100, 200, 400] ...
    '''
    default_bb = 100

    def __init__(self, players, deck=None, bigblind=None):
        self.deck = deck if deck is not None else Deck()
        self.bigblind = bigblind if bigblind is not None else self.default_bb
        self.players = players
        self.nr_players = len(players)
        self.dealer = randint(0, self.nr_players - 1)
        self.deck = deck if deck is not None else Deck()
        self.reset()

    def pot(self):
        pot = 0
        for state_bets in self.bets.values():
            for bets in state_bets.values():
                pot += sum(bets)
        return pot

    def next_dealer(self):
        if self.dealer is None:
            self.dealer = randint(0, self.nr_players - 1)
        else:
            self.dealer = (self.dealer + 1) % self.nr_players
        return self.dealer

    def next_player(self):
        pid = self.next_player_id()
        return self.players[pid]

    def next_player_id(self):
        if self.current_player is None:
            self.current_player = (self.dealer + 1) % self.nr_players
        else:
            self.current_player = (self.current_player + 1) % self.nr_players
        return self.current_player

    def to_pay(self, player):
        payed = sum(self.bets[self.state][player])
        topay = 0
        for state in self.bets:
            for p in self.bets[state]:
                if p is not player:
                    summ = sum(self.bets[self.state][p])
                    topay = max(summ, topay)
        topay = topay - payed
        topay = max(topay, 0)
        return topay

    def players_active(self):
        return self.nr_players - (self.players_fold + self.players_allin)

    def players_in_hand(self):
        return self.nr_players - self.players_fold

    def reset(self):
        self.state = 0
        self.bets = {}
        for state in [k for k in game_states.keys() if k != 4]:
            self.bets[state] = {}
            for player in self.players:
                self.bets[state][player] = []
        for p in self.players:
            p.state = 0
            p.hand = None
        self.players_fold = 0
        self.players_allin = 0
        self.initiator = None
        self.current_player = None
        self.family_cards = []


class Game(object):
    '''
    Main class responsable for managing the state of a round, managing
    players, the deck, winners, the pot etc...
    '''
    def __init__(self, table):
        self.table = table
        self.nr_round = 0

    def small_blind(self):
        player = self.table.next_player()
        self.action(3, self.table.bigblind / 2)
        log('[%s](%s) SMALL BLIND' %
            (player.name, player.bankroll))

    def big_blind(self):
        player = self.table.next_player()
        self.action(3, self.table.bigblind)
        log('[%s](%s) BIG BLIND' %
            (player.name, player.bankroll))
        self.table.initiator = player

    def play(self, rounds=1):
        self.current_player = None
        last = 0
        while self.nr_round < rounds:
            self.table.reset()
            self.pre_flop()
            for state in (1, 2, 3):
                if self.table.players_in_hand() >= 2:
                    self.game_state(state)
            if self.table.players_in_hand() >= 2:
                self.table.state = 4
            self.manage_winnings()
            self.table.next_dealer()
            self.table.deck = Deck()
            self.nr_round += 1
            new = self.table.players[1].bankroll
            if self.nr_round % 1000 == 0:
                bankroll_history.append(self.table.players[1].bankroll)
            new = int((float(self.nr_round) / rounds) * 100)
            if new > last:
                last = new
                print '(%s%%)' % new

    def manage_bets(self):
        '''
        Function that takes care of the betting in the current state until
        no more players are required to make an action.
        '''
        if self.table.players_active() < 2:
            return
        player = self.table.next_player()
        self.table.initiator = Player(name='None')
        first_after_bb = True
        while (self.table.initiator is not player and
               self.table.players_in_hand() >= 2):
            if player.state not in (5, 6):
                move, amt = player.move(self.table, nr_round=self.nr_round)
                self.action(move, amt)
                log('[%s](%s)(%s%s) %s %s' % (
                    player.name, player.bankroll, player.hand.card1,
                    player.hand.card2, player_states[move], amt))
                if first_after_bb:
                    first_after_bb = False
                    self.table.initiator = player
            player = self.table.next_player()

    def manage_winnings(self):
        '''
        Function that checks who the winners are and distributes the pot
        acordingly.
        '''
        if self.table.state < 4:
            # A single player remained, the rest have folded
            # Go through each bet, if they dont belong to the un-folded player,
            # add them upp so we can transfer them to the winner.
            winnings = 0
            winner = None
            for player in self.table.bets[self.table.state]:
                for state in xrange(self.table.state + 1):
                    winnings += sum(self.table.bets[state][player])
                if player.state != 6:
                    winner = player
            winner.bankroll += winnings
            winner.signal_end(win=True, amt=winnings, nr_round=self.nr_round)
            log('WINNER: %s %s' % (winner.name, winnings))
            for p in self.table.players:
                if p is not winner:
                    lost_amt = 0
                    for bets in self.table.bets.values():
                        lost_amt += sum(bets[p])
                    p.signal_end(win=False, amt=lost_amt, nr_round=self.nr_round)
        else:
            # A so called 'showdown'
            e = Evaluator()
            dboard = []
            for card in self.table.family_cards:
                dboard.append(DCard.new(repr(card)))
            vals = {}
            for p in self.table.players:
                vals[p] = [0, 0]
            for p in self.table.players:
                for s in self.table.bets:
                    vals[p][0] += sum(self.table.bets[s][p])
                hand = [
                    DCard.new(repr(p.hand.cards()[0])),
                    DCard.new(repr(p.hand.cards()[1])),
                ]
                vals[p][1] = e.evaluate(dboard, hand) if p.state != 6 else 9000

            to_distribute = sum([v[0] for v in vals.values()])
            best_card_score = min([v[1] for v in vals.values()])
            winners = [
                p
                for p, v in vals.iteritems()
                if v[1] == best_card_score
            ]
            winnings = 0
            for p, v in vals.iteritems():
                if p in winners:
                    p.bankroll += v[0]
                    winnings += v[0]
                else:
                    for w in winners:
                        w.bankroll += int(v[0]/len(winners))
                        winnings += int(v[0]/len(winners))
            for w in winners:
                w.signal_end(
                    win=True, amt=int(winnings/len(winners)),
                    nr_round=self.nr_round)
            for p in self.table.players:
                if p not in winners:
                    lost_amt = 0
                    for bets in self.table.bets.values():
                        lost_amt += sum(bets[p])
                    p.signal_end(win=False, amt=lost_amt, nr_round=self.nr_round)
            log('WINNER(s): %s %s' %
                (', '.join([w.name for w in winners]),
                 int(winnings/len(winners))))

    def game_state(self, state):
        self.table.deck.pop_card()
        cards = []
        nr_cards = 3 if state is 1 else 1
        for _ in xrange(nr_cards):
            self.table.family_cards.append(self.table.deck.pop_card())
        log('---------- %s: %s ----------' %
            (game_states[state],
             ' '.join([repr(c) for c in self.table.family_cards])))
        ''' Does the work in the 'flop', 'turn' and 'river' states'''
        self.table.state = state
        self.table.current_player = self.table.dealer
        self.manage_bets()

    def pre_flop(self):
        log('-' * 10 + ' Preflop ' + '-' * 10)
        # Prepare the deck
        deck = self.table.deck
        deck.shuffle()
        log('Dealer: %s' % self.table.players[self.table.dealer].name)
        # Distribute starting hands
        for player in self.table.players:
            if player.hand is None:
                hand = deck.pop_hand()
                player.hand = hand
        # Pre-Flop action
        self.small_blind()
        self.big_blind()
        self.manage_bets()

    def action(self, code, amt=0):
        player = self.table.players[self.table.current_player]
        if code is 2:
            # Call
            player.bankroll -= amt
            self.table.bets[self.table.state][player].append(amt)
        elif code in (3, 4):
            # Bet & Raise
            player.bankroll -= amt
            self.table.bets[self.table.state][player].append(amt)
            self.table.initiator = player
        elif code is 5:
            # All-in
            player.bankroll -= amt
            self.table.bets[self.table.state][player].append(amt)
            self.table.initiator = player
            self.table.players_allin += 1
            assert player.bankroll == 0
        elif code is 6:
            # Fold
            self.table.players_fold += 1
            lost_amt = 0
            for bets in self.table.bets.values():
                lost_amt += sum(bets[player])
        player.state = code

        assert player.bankroll >= 0

bankroll_history = []

def main():
    import pprint
    deck = Deck()
    p1 = DeterministicPlayer(name='A', bankroll=10**7)
    p2 = QLearning(name='Q', bankroll=10**7)
    table = Table([p1, p2], deck=deck, bigblind=10)
    g = Game(table)
    g.play(rounds=int(sys.argv[1]))


    if len(sys.argv) == 3:
        f = open(sys.argv[2], 'w')
        f.write('rounds=' + sys.argv[1])
        f.write('\n')
        f.write('alpha=' + str(p2.alpha))
        f.write('\n')
        f.write('gamma=' + str(p2.gamma))
        f.write('\n')
        f.write('eps=' + str(p2.eps))
        f.write('\n')
        f.write('eps decay=' + str(p2.exploration_rate))
        f.write('\n')
        f.write(str(p2.bankroll) + ' ' + str(p2.eps))
        f.write('\n')
        f.write(pprint.pformat(p2.Q))
        f.write('\n')
        f.write(pprint.pformat(p2.T))
        f.write('\n')
        f.write('Sanity Check: %s' % sum([p.bankroll for p in g.table.players]))
        f.write('\n')
        f.write(str(p2.test))
        f.write('\n')
        for k, v in p2.test.iteritems():
            f.write(str(k) + ' ' + str(sum(v.values())))
            f.write('\n')
        f.write(str(p2.strength_intervals))
        f.write('\n')
        f.write(str(bankroll_history))
        f.write('\n')
        f.close()
    else:
        print 'rounds=', sys.argv[1]
        print 'alpha=', p2.alpha
        print 'gamma=', p2.gamma
        print 'eps=', p2.eps
        print 'eps decay=', p2.exploration_rate
        print p2.bankroll, p2.eps
        pprint.pprint(p2.Q)
        print 
        pprint.pprint(p2.T)
        print 'Sanity Check: %s' % sum([p.bankroll for p in g.table.players])
        print p2.test
        for k, v in p2.test.iteritems():
            print k, sum(v.values())
        print p2.strength_intervals
        print bankroll_history


if __name__ == "__main__":
    main()
