from os import environ
from random import randint
from game import Card, Hand, Deck, Player, player_states
from players import DeterministicPlayer


def log(msg):
    if environ.get('DEBUG'):
        print msg


game_states = {
    0: 'PREFLOP',
    1: 'FLOP',
    2: 'TURN',
    3: 'RIVER',
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
        self.state = 0
        self.dealer = None
        self.players = players
        self.current_player = None
        self.nr_players = len(players)
        self.dealer = randint(0, self.nr_players - 1)
        self.initiator = None
        self.bets = {}
        self.players_fold = 0
        self.players_allin = 0
        for state in game_states:
            self.bets[state] = {}
            for player in self.players:
                self.bets[state][player] = []

    def action(self, code, amt=0):
        player = self.players[self.current_player]
        if code is 2:
            # Call
            player.bankroll -= amt
            self.bets[self.state][player].append(amt)
        elif code in (3, 4):
            # Bet & Raise
            player.bankroll -= amt
            self.bets[self.state][player].append(amt)
            self.initiator = player
        elif code is 5:
            # All-in
            player.bankroll -= amt
            self.bets[self.state][player].append(amt)
            self.initiator = player
            self.players_allin += 1
            assert player.bankroll == 0
        elif code is 6:
            # Fold
            self.players_fold += 1

        assert player.bankroll >= 0

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
        log('%s, %s' % (topay, payed))
        return topay

    def players_active(self):
        return self.nr_players - (self.players_fold + self.players_allin)

    def players_in_hand(self):
        return self.nr_players - self.players_fold


class Game(object):
    '''
    Main class responsable for managing the state of a round, managing
    players, the deck, winners, the pot etc...
    '''

    def __init__(self, table):
        self.table = table

    def small_blind(self):
        player = self.table.next_player()
        self.table.action(3, self.table.bigblind / 2)
        log('[%s](%s) SMALL BLIND' %
            (player.name, player.bankroll))

    def big_blind(self):
        player = self.table.next_player()
        self.table.action(3, self.table.bigblind)
        log('[%s](%s) BIG BLIND' %
            (player.name, player.bankroll))
        self.table.initiator = player

    def distribute_winnings(self):
        pass

    def play(self, rounds=1):
        nr_round = 0
        while nr_round < rounds:
            self.pre_flop()
            for state in (1, 2, 3):
                if self.table.players_in_hand() >= 2:
                    self.game_state(state)
            '''
            self.showdown()
            '''
            nr_round += 1
        self.distribute_winnings()

    def collect_bets(self):
        '''
        Function that takes care of the betting in the current state until
        no more players are required to make an action.
        '''
        if self.table.players_active() < 2:
            return
        player = self.table.next_player()
        self.table.initiator = Player(name='None')
        first_after_bb = True
        log('initiator: %s, player: %s' % (
            self.table.initiator.name, player.name))
        while self.table.initiator is not player:
            if player.state not in (5, 6):
                move, amt = player.move(self.table)
                self.table.action(move, amt)
                log('[%s](%s)(%s%s) %s %s' % (
                    player.name, player.bankroll, player.hand.card1,
                    player.hand.card2, player_states[move], amt))
                if first_after_bb:
                    first_after_bb = False
                    self.table.initiator = player
            log('initiator: %s' % self.table.initiator.name)
            player = self.table.next_player()

    def game_state(self, state):
        log('---------- %s ----------' % game_states[state])
        ''' Does the work in the 'flop', 'turn' and 'river' states'''
        self.table.state = state
        self.table.current_player = self.table.dealer
        self.collect_bets()

    def pre_flop(self):
        log('-' * 10 + ' Preflop ' + '-' * 10)
        # Prepare the deck
        deck = self.table.deck
        deck.shuffle()
        log('Deck shuffled')
        log('Dealer: %s' % self.table.players[self.table.dealer].name)
        # Distribute starting hands
        for player in self.table.players:
            hand = deck.pop_hand()
            player.hand = hand
        # Pre-Flop action
        self.small_blind()
        self.big_blind()
        self.collect_bets()


def main():
    deck = Deck()
    p1 = DeterministicPlayer(name='A', bankroll=1500)
    p2 = DeterministicPlayer(name='B', bankroll=1500)
    p3 = DeterministicPlayer(name='C', bankroll=1500)
    p4 = DeterministicPlayer(name='D', bankroll=1500)
    table = Table([p1, p2, p3, p4], deck=deck, bigblind=100)
    g = Game(table)
    g.play(rounds=1)


if __name__ == "__main__":
    main()

