from random import random, randint
from game import Player
from eval import DeucesWrapper, Eval


class QLearning(Player):
    states = {
        'preflop': 0,
        'flop': 1,
        'turn': 2,
        'river': 3,
    }
    strength = {
        's': 0,
        'm': 1,
        'l': 2
    }
    combinations = {
        1: 1081.0,
        2: 1035.0,
        3: 990.0,
    }
    strength_ints = {'s': 0.33, 'm': 0.66, 'l': 1.0}
    preflop_ints = (21, 130)
    strength_intervals = (
        ('l', 4000),
        ('m', 6000),
        ('s', 10000),
    )
    eps = 0.5                       # Exploration tendency
    exploration_rate = 0.0001       # Exploration decay
    gamma = 0.9                     # Future rewards importance
    alpha = 0.1                     # Adapting rate

    def __init__(self, name=None, bankroll=None):
        super(QLearning, self).__init__(name=name, bankroll=bankroll)
        self.Q = [[
            {'check': 0, 'bet': 0, 'fold': 0, 'call': 0}
            for _ in xrange(len(self.strength))]
            for _ in xrange(len(self.states))
        ]
        self.T = [[
            {'check': 0, 'bet': 0, 'fold': 0, 'call': 0}
            for _ in xrange(len(self.strength))]
            for _ in xrange(len(self.states))
        ]
        self.prev_state = None
        self.nr_plays = 0
        #@TODO
        self.test = {'s': {'call': 0, 'check': 0, 'bet': 0}, 'm': {'call': 0, 'check': 0, 'bet': 0}, 'l': {'call': 0, 'check': 0, 'bet': 0}}

    def calculate_strength(self, board, hand, state):
        '''Returns s m or l'''
        e = Eval()
        if not board:
            s = e.get_hand_rank(hand.cards())
            if s < self.preflop_ints[0]:
                return 'l'
            elif s < self.preflop_ints[1]:
                return 'm'
            else:
                return 's'
        else:
            probs = e.get_probs(hand.cards(), board)
            wewin = (probs[0] + 0.5 * probs[1]) / self.combinations[state]
            for k, p in self.strength_ints.iteritems():
                if wewin <= p:
                    return k

        raise Exception('Bad strength interval configuration!')

    def calculate_strength2(self, board, hand):
        '''Returns s m or l'''
        c1, c2 = hand.cards()
        if c1.rank_num() >= 10 and c2.rank_num() >= 10:
            return 'l'
        elif c1.rank_num() > 10 or c2.rank_num() > 10 or (c1.suit == c2.suit) or (c1.rank_num() > 7 and c2.rank_num() > 7):
            return 'm'
        else:
            return 's'

    def has_previous_state(self, r):
        return self.prev_state is not None and self.prev_state['round'] == r

    def update_prev_state(self, state, strength, action, nr_round):
        self.prev_state = {
            'state': state, 'strength': strength, 'action': action,
            'round': nr_round}

    def update_Q(self, state, strength, reward=0, qmax=None):
        '''The heart of our Q learning algorithm.'''
        #@TODO DELETE
        if state == 1 and self.prev_state['state'] == 0 and strength == 'l':
            self.test[self.prev_state['strength']][self.prev_state['action']] += 1
        self.nr_plays += 1
        prev_state = self.prev_state['state']
        prev_str = self.prev_state['strength']
        prev_action = self.prev_state['action']

        # Get probability of getting from previous state to this one
        this = self.T[prev_state][self.strength[prev_str]][prev_action]
        total = sum(self.T[prev_state][self.strength[prev_str]].values())
        t = this/total

        # Get expected Q value of this state
        if qmax is None:
            total_actions = sum(self.T[state][self.strength[strength]].values())
            unweighed_sum = 0
            for action, times in self.T[state][self.strength[strength]].iteritems():
                unweighed_sum += times * self.Q[state][self.strength[strength]][action]
            qmax = unweighed_sum / total_actions

        # Update
        sample = reward + qmax
        old = self.Q[prev_state][self.strength[prev_str]][prev_action]
        new = (1 - self.alpha) * old + self.alpha * sample
        self.Q[prev_state][self.strength[prev_str]][prev_action] = round(new, 2)

    def update_T(self, strength='s', action='fold', table_state=0):
        self.T[table_state][self.strength[strength]][action] += 1

    def should_explore(self):
        return True if random() <= self.eps else False

    def get_optimum_bet(self, topay, bb, pot=0):
        return topay + 10 * bb

    def decide(self, table, strength='s', table_state=0):
        current_state = self.Q[table_state][self.strength[strength]]
        explore = self.should_explore()
        topay = table.to_pay(self)
        valid_actions = current_state.keys()
        if topay > 0:
            valid_actions.remove('check')
        if topay == 0:
            valid_actions.remove('call')
        valid_action_scores = [current_state[x] for x in valid_actions]
        if explore:
            random_index = randint(0, len(valid_actions) - 1)
            action = valid_actions[random_index]
        else:
            best_action_score = max(valid_action_scores)
            for a in valid_actions:
                if current_state[a] == best_action_score:
                    action = a
                    break
        if action == 'fold':
            topay = 0
        elif action == 'bet':
            topay = self.get_optimum_bet(topay, table.bigblind)

        return action, topay

    def lower_exploration(self):
        self.eps -= self.eps * self.exploration_rate

    def signal_end(self, win=False, amt=0, nr_round=0):
        assert win or self.has_previous_state(nr_round)
        if not win:
            amt *= -1
        if self.has_previous_state(nr_round):
            self.update_Q(0, 0, amt, 0)
        self.prev_state = None

    def move(self, table, nr_round=None):
        assert nr_round is not None
        state = table.state

        # Categorize hand strength in 's', 'm', or 'l'
        strength_label = self.calculate_strength(table.family_cards, self.hand, state)

        # Decide which action to take based on the Q table and exploration rate
        action, amt = self.decide(
            table, strength=strength_label, table_state=state)

        # Decrease desire to explore
        self.lower_exploration()

        # Update T table based on the decision we took
        self.update_T(
            strength=strength_label, table_state=state, action=action)

        # Update Q table if there is a previous state this round
        if self.has_previous_state(nr_round):
            self.update_Q(table.state, strength_label, reward=state)

        # Rewrite the last state
        self.update_prev_state(state, strength_label, action, nr_round)

        if action == 'check':
            action = 1
        elif action == 'call':
            action = 2
        elif action == 'bet':
            action = 3
        elif action == 'fold':
            action = 6

        return action, amt
