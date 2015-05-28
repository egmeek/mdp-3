from random import randint
from game import Card, Hand, Deck, Player


DEBUG = True


def log(msg):
    if DEBUG:
        print msg


states = {
    0: 'Pre-Flop',
    1: 'Flop',
    2: 'Turn',
    3: 'River',
}


class Table(object):
    '''
    Class responsable for the information available to all players. What
    part of the game were in, bets, pots, winners etc.
    When a player needs to make a decision, the Player object receives an
    instance of the Table class that contains all the necessary information
    to make one.
    '''
    default_bb = 100

    def __init__(self, players, deck=None, bigblind=None):
        self.deck = deck if deck is not None else Deck()
        self.bigblind = bigblind if bigblind is not None else self.default_bb
        self.game_state = 0
        self.dealer = None
        self.players = players
        self.current_player = None
        self.nr_players = len(players)
        self.dealer = randint(0, self.nr_players - 1)
        self.initiator = None

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
        player.bankroll -= (self.table.bigblind / 2)
        log('Player %s is the small blind. (%s)' %
            (player.name, player.bankroll))

    def big_blind(self):
        player = self.table.next_player()
        player.bankroll -= self.table.bigblind
        log('Player %s is the big blind. (%s)' %
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
            log('To move: %s' % player.name)
            move, amt = player.move(self.table)
            player = self.table.next_player()


def main():
    deck = Deck()
    p1 = Player(name='A', bankroll=1500)
    p2 = Player(name='B', bankroll=1500)
    p3 = Player(name='C', bankroll=1500)
    table = Table([p1, p2, p3], deck=deck, bigblind=100)
    g = Game(table)
    g.play(rounds=1)


main()
