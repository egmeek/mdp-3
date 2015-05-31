from random import randrange
from game import Player
from poker import DeucesWrapper
from deuces.deuces import Card, Evaluator


class QLearning(Player):
    state = {
        'preflop': 0,
        'flop': 1,
        'turn': 2,
        'river': 3,
        'showdown': 4,
        'fold': 5,
    }
    strength = {
        's': 0,
        'm': 1,
        'l': 2
    }
    strength_intervals = {
        'l': 1000,
        'm': 3000,
        's': 10000,
    }
    eps = 0.5                       # Exploration tendency
    exploration_rate = 0.01         # Exploration decay
    gamma = 0.8                     # Future rewards importance
    alpha = 0.5                     # Adapting rate

    def __init__(self):
        self.Q = [
            {'check': 0, 'bet': 0, 'fold': 0, 'call': 0}
            for _ in xrange(len(self.strength))
            for _ in xrange(len(self.states))
        ]
        self.T = [
            {'check': 0, 'bet': 0, 'fold': 0, 'call': 0}
            for _ in xrange(len(self.strength))
            for _ in xrange(len(self.states))
        ]
        self.prev_state = None
        self.nr_plays = 0

    def calculate_strength(self, board, hand):
        '''Returns S M L'''
        dw = DeucesWrapper()
        score = dw.evaluate(board, hand)
        strength = None
        for label, interval in self.strength_intervals.iteritems():
            if score <= interval:
                return label
        raise Exception('Bad strength interval configuration!')

    def has_previous_state(self, r):
        return self.prev_state is not None and self.prev_state['round'] == r

    def update_previous_state(self, state, strength, action):
        self.prev_state = {
            'state': state, 'strength': strength, 'action': action}

    def update_Q(self, state, strength):
        '''The heart of our Q learning algorithm.'''
        self.nr_plays += 1
        prev_state = self.prev_state['state']
        prev_str = self.prev_state['strength']
        prev_action = self.prev_state['action']

        # Get probability of getting from previous state to this one
        this = self.T[prev_state][prev_str][prev_action]
        total = sum(self.T[prev_state][prev_str].keys())
        t = this/total

        # Get max Q value of this state
        qmax = max(self.Q[state][strength].keys())

        # Get reward of this state
        reward = self.get_reward()

        # Update
        sample = reward + qmax
        old = self.Q[prev_state][prev_str][prev_action]
        self.Q[prev_state][prev_str][prev_action] =\
            (1 - self.alpha) * old + self.alpha * sample

    def update_T(self, strength='s', action='fold', table_state=0):
        self.T[table_state][strength][action] += 1

    def should_explore(self):
        return True if randrange(0, 1, 0.001) <= self.eps else False

    def get_optimum_bet(self, topay, bb):
        return topay + 3*bb

    def decide(self, table, strength='s', table_state=0):
        current_state = self.Q[table_state][strength]
        explore = self.should_explore()
        topay = table.to_pay(self)
        action = 'fold'
        valid_actions = current_state.keys()
        if topay > 0:
            current_state.remove('check')
        if topay == 0:
            current_state.remove('call')
        valid_action_scores = [current_state[x] for x in valid_actions]
        if explore:
            random_index = randint(0, len(valid_actions) - 1)
            best_action_score = [valid_action_scores][random_index]
        else:
            best_action_score = max(valid_action_scores)
        for a in valid_actions:
            if current_state[a] == best_action_score:
                if action == 'fold':
                    topay = 0
                elif action == 'bet':
                    topay = self.get_optimum_bet(topay, table.bigblind)
        return a, topay

    def lower_exploration(self):
        self.eps -= self.eps * self.exploration_rate

    def move(self, table, nr_round=None):
        assert nr_round is not None
        state = table.state

        # Categorize hand strength in 's', 'm', or 'l'
        strength_label = self.calculate_strength(self.family_cards, self.hand)

        # Decide which action to take based on the Q table and exploration rate
        action, amt = self.decide(strength=strength_label, table_state=state)

        # Decrease desire to explore
        self.lower_exploration()

        # Update T table based on the decision we took
        self.update_T(
            strength=strength_label, table_state=state, action=action)

        # Update Q table if there is a previous state this round
        if self.has_previous_state(nr_round):
            self.update_Q(table.state, strength)

        # Rewrite the last state
        self.update_prev_state(table_state, strength, action)

        if action == 'check':
            action = 1
        elif action == 'call':
            action = 2:
        elif action == 'bet':
            action = 3:
        elif action == 'fold':
            action = 6

        return action, amt
