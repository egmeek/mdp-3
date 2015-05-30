from random import randint
from game import Player


class DeterministicPlayer(Player):
    def move(self, table):
        state = table.state
        bets = table.bets[state]
        topay = table.to_pay(self)
        strength = sum([c.rank_num() for c in self.hand.cards()])
        fold = [0, 6]
        check = [0, 1]
        bet = [0, 3]
        call = [0, 2]
        raisee = [0, 4]
        if strength >= 20:
            if topay == 0:
                check[0] = 0.2
                bet[0] = 0.8
            else:
                call[0] = 0.5
                raisee[0] = 0.5
        elif strength >= 10 and strength < 20:
            if topay == 0:
                check[0] = 0.7
                bet[0] = 0.3
            else:
                fold[0] = 0.2
                call[0] = 0.8
        elif strength < 10:
            if topay == 0:
                check[0] = 0.9
                bet[0] = 0.1
            else:
                fold[0] = 1

        prob_space = fold[0] + check[0] + bet[0] + call[0] + raisee[0]
        prob = randint(0, prob_space * 10) / 10.0
        probs = sorted([raisee, fold, check, bet, call], key=lambda x: x[0])
        s = 0
        for p in probs:
            p[0] += s
            s += p[0]
        action = 0

        if prob < probs[0][0]:
            action = probs[0][1]
        elif prob < probs[1][0]:
            action = probs[1][0]
        elif prob < probs[2][0]:
            action = probs[2][1]
        elif prob < probs[3][0]:
            action = probs[3][1]
        else:
            action = probs[4][1]

        if action in (0, 1, 6):
            topay = 0

        if action in (3, 4):
            topay += int(topay + table.bigblind * 1.5)

        if topay >= self.bankroll:
            topay = self.bankroll
            action = 5

        return action, topay
