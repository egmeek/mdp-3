from random import randint
from game import Card, Hand, Deck, Player, player_states
from players import DeterministicPlayer


DEBUG = True


def log(msg):
    if DEBUG:
        print msg


game_states = {
    0: 'PREFLOP',
    1: 'FLOP',
    2: 'TURN',
    3: 'RIVER',
}


class Bets(object):
    pass


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
        for state in game_states:
            self.bets[state] = {}
            for player in self.players:
                self.bets[state][player] = []

    def action(self, code, amt=0):
        if code is 2:
            # Call
            self.players[self.current_player].bankroll -= amt
        elif code in (3, 4, 5):
            # Bet & Raise & All-in
            self.players[self.current_player].bankroll -= amt
            player = self.players[self.current_player]
            self.bets[self.state][player].append(amt)
            self.initiator = self.players[self.current_player]

    def next_dealer(self):
        if self.dealer is None:
            self.dealer = randint(0, self.nr_players - 1)
        else:
            self.dealer = (self.dealer + 1) % self.nr_players

    def next_player(self):
        pid = self.next_player_id()
        return self.players[pid]

    def next_player_id(self):
        if self.current_player is None:
            self.current_player = (self.dealer + 1) % self.nr_players
        else:
            self.current_player = (self.current_player + 1) % self.nr_players
        return self.current_player


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

    def play(self, rounds=1):
        nr_round = 0
        while nr_round < rounds:
            self.pre_flop()
            '''
            self.flop()
            self.turn()
            self.river()
            self.showdown()
            '''
            nr_round += 1

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
        player = self.table.next_player()
        while self.table.initiator is not player:
            if player.state not in (5, 6):
                move, amt = player.move(self.table)
                self.table.action(move, amt)
                log('[%s](%s) %s %s' % (
                    player.name, player.bankroll, player_states[move], amt))
            player = self.table.next_player()


def main():
    deck = Deck()
    p1 = DeterministicPlayer(name='A', bankroll=1500)
    p2 = DeterministicPlayer(name='B', bankroll=1500)
    p3 = DeterministicPlayer(name='C', bankroll=1500)
    p4 = DeterministicPlayer(name='D', bankroll=1500)
    table = Table([p1, p2, p3, p4], deck=deck, bigblind=100)
    g = Game(table)
    g.play(rounds=1)


main()
