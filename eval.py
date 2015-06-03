from deuces.deuces import Card as DCard, Evaluator as DEvaluator
from game import Card, suits, ranks, Deck


class DeucesWrapper(object):
    def __init__(self):
        self.e = DEvaluator()

    def evaluate(self, board, hand):
        dhand = []
        dboard = []
        for c in board:
            dcard = DCard.new(repr(c))
            dboard.append(dcard)
        for c in hand.cards():
            dcard = DCard.new(repr(c))
            dhand.append(dcard)
        return self.e.evaluate(dboard, dhand)


hand_ranks = {
'K4s': 57, 'K4o': 131, '64o': 135, 'JJ': 4, 'KQs': 6, '82o': 167, 'Q4s':
70, '22': 50, 'J3o': 152, '53o': 137, 'K7s': 43, 'A6s': 33, 'A6o': 112, '53s':
76, '72s': 119, 'Q4o': 142, '92s': 110, 'KQo': 19, '82s': 117, 'QJo': 34,
'76s': 55, 'K5s': 54, 'T7o': 123, 'K5o': 127, 'T7s': 56, '76o': 120, 'T5o':
156, 'QJs': 12, 'Q5s': 68, '93o': 164, '55': 45, 'A7s': 29, '54o': 126, 'A7o':
101, '54s': 64, '65o': 122, '93s': 106, 'Q5o': 140, 'J9s': 25, 'T2o': 161,
'A4o': 103, 'T4o': 157, 'J5o': 148, '88': 20, 'A4s': 31, 'J9o': 79, 'T2s': 97,
'43o': 141, '84s': 93, 'J5s': 81, '73s': 102, 'K7o': 121, 'Q2o': 145, '64s':
69, 'Q2s': 74, '84o': 155, '43s': 83, 'K6s': 52, 'T8o': 99, 'J8s': 40, '98s':
39, '72o': 168, 'A5o': 100, 'A5s': 27, '98o': 98, 'J8o': 107, '83s': 115,
'T9o': 72, '42o': 153, '33': 51, '52o': 150, 'Q3o': 143, 'JTs': 15, 'Q3s': 71,
'T4s': 94, 'JTo': 46, 'J3s': 86, '92o': 165, '42s': 96, '83o': 166, 'T9s': 22,
'75s': 66, '63s': 89, 'QTs': 14, 'J7s': 63, 'Q8o': 114, 'Q8s': 42, '66': 35,
'J7o': 128, 'QTo': 48, '75o': 129, '63o': 147, 'A2s': 38, 'K9o': 80, '96s': 67,
'AKs': 3, 'ATo': 41, '86s': 61, 'AKo': 10, 'ATs': 11, '86o': 125, 'J2o': 154,
'K9s': 21, 'J2s': 88, '96o': 133, 'A2o': 116, '62s': 109, 'Q7o': 130, 'J6s':
78, '99': 16, 'J6o': 146, '62o': 162, 'T3s': 95, 'A3s': 32, '97s': 53, '85s':
77, 'KK': 1, 'T8s': 37, 'KJo': 30, 'Q9s': 24, 'KJs': 8, 'Q9o': 82, '65s': 62,
'97o': 118, '85o': 138, 'A3o': 108, 'K6o': 124, 'A8s': 23, 'T5s': 92, 'AQs': 5,
'T3o': 159, 'K2s': 58, '32o': 158, 'K2o': 134, 'AQo': 17, 'A8o': 90, 'Q6o':
136, '87o': 113, 'TT': 9, '94s': 105, 'T6s': 73, '94o': 163, 'T6o': 139, 'Q6s':
65, 'AA': 0, 'A9o': 75, '74s': 84, 'K3s': 59, '73o': 160, '52s': 91, 'J4s': 85,
'77': 28, 'J4o': 151, 'K3o': 132, 'A9s': 18, '74o': 144, 'QQ': 2, 'K8o': 111,
'95s': 87, 'AJs': 7, '87s': 47, 'KTs': 13, '32s': 104, 'KTo': 44, '95o': 149,
'AJo': 26, 'K8s': 36, 'Q7s': 60, '44': 49
}


cards = (
Card(rank='A', suit='h'), Card(rank='A', suit='s'), Card(rank='A', suit='c'),
Card(rank='A', suit='d'), Card(rank='K', suit='h'), Card(rank='K', suit='s'),
Card(rank='K', suit='c'), Card(rank='K', suit='d'), Card(rank='Q', suit='h'),
Card(rank='Q', suit='s'), Card(rank='Q', suit='c'), Card(rank='Q', suit='d'),
Card(rank='J', suit='h'), Card(rank='J', suit='s'), Card(rank='J', suit='c'),
Card(rank='J', suit='d'), Card(rank='T', suit='h'), Card(rank='T', suit='s'),
Card(rank='T', suit='c'), Card(rank='T', suit='d'), Card(rank='9', suit='h'),
Card(rank='9', suit='s'), Card(rank='9', suit='c'), Card(rank='9', suit='d'),
Card(rank='8', suit='h'), Card(rank='8', suit='s'), Card(rank='8', suit='c'),
Card(rank='8', suit='d'), Card(rank='7', suit='h'), Card(rank='7', suit='s'),
Card(rank='7', suit='c'), Card(rank='7', suit='d'), Card(rank='6', suit='h'),
Card(rank='6', suit='s'), Card(rank='6', suit='c'), Card(rank='6', suit='d'),
Card(rank='5', suit='h'), Card(rank='5', suit='s'), Card(rank='5', suit='c'),
Card(rank='5', suit='d'), Card(rank='4', suit='h'), Card(rank='4', suit='s'),
Card(rank='4', suit='c'), Card(rank='4', suit='d'), Card(rank='3', suit='h'),
Card(rank='3', suit='s'), Card(rank='3', suit='c'), Card(rank='3', suit='d'),
Card(rank='2', suit='h'), Card(rank='2', suit='s'), Card(rank='2', suit='c'),
Card(rank='2', suit='d'),
)


class Eval(object):
    def __init__(self):
        self.relevant = []

    def get_probs(self, cards, board):
        win, eq, loss = 0, 0, 0
        ourstr = self.get_strength(cards + board)
        d = Deck()
        for i in xrange(len(d.cards)):
            for j in xrange(i + 1, len(d.cards)):
                if (d.cards[i] not in cards + board and
                        d.cards[j] not in cards + board):
                    hand = [d.cards[i], d.cards[j]]
                    itsstr = self.get_strength(hand + board)
                    outcome = self.get_winner(ourstr, itsstr)
                    if outcome == -1:
                        win += 1
                    elif outcome == 1:
                        loss += 1
                    else:
                        eq += 1
        return win, eq, loss

    def get_hand_rank(self, cards):
        c1, c2 = cards
        if c2.rank_num() > c1.rank_num():
            c2, c1 = c1, c2
        suit = ''
        if c1.rank_num() != c2.rank_num():
            suit = 'o' if c1.suit != c2.suit else 's'
        key = c1.rank + c2.rank + suit
        return hand_ranks[key]

    def get_winner(self, s1, s2):
        # -1 board1, board1 == board2, 1 board2
        if s1[0] > s2[0]:
            return 1
        elif s1[0] < s2[0]:
            return -1
        assert len(s1[1]) == len(s2[1])
        for i in xrange(len(s1[1])):
            if s1[1][i] > s2[1][i]:
                return -1
            elif s1[1][i] < s2[1][i]:
                return 1
        return 0

    def get_strength(self, board):
        board = sorted(board, key=lambda x: x.rank_num(), reverse=True)
        if self.check_royal(board):
            return 1, self.relevant[:]
        elif self.check_kind_4(board):
            return 2, self.relevant[:]
        elif self.check_full(board):
            return 3, self.relevant[:]
        elif self.check_flush(board):
            return 4, self.relevant[:]
        elif self.check_straight(board):
            return 5, self.relevant[:]
        elif self.check_kind_3(board):
            return 6, self.relevant[:]
        elif self.check_kind_2_2(board):
            return 7, self.relevant[:]
        elif self.check_kind_2(board):
            return 8, self.relevant[:]
        else:
            return 9, board[:][:5]

    def check_royal(self, cards):
        self.relevant = []
        hist = {}
        for c in cards:
            hist[c.suit] = hist.setdefault(c.suit, 0) + 1
        if max(hist.values()) < 5:
            return False
        new = []
        for c in cards:
            if hist[c.suit] >= 5:
                new.append(c)

        return self.check_straight(new)

    def check_straight(self, cards):
        c = 1
        self.relevant = []
        for i in xrange(len(cards) - 1):
            if c == 1:
                best = cards[i]
            if cards[i].rank_num() - 1 == cards[i+1].rank_num():
                c += 1
                if c == 5:
                    self.relevant.append(best)
                    return True
            elif cards[i].rank_num() != cards[i+1].rank_num():
                c = 1
        return False

    def check_flush(self, cards):
        colors = {'s': 0, 'h': 0, 'c': 0, 'd': 0}
        self.relevant = []
        for c in cards:
            colors[c.suit] += 1
            if colors[c.suit] == 5:
                for c2 in cards:
                    if c2.suit == c.suit:
                        self.relevant.append(c2)
                self.relevant = self.relevant[:5]
                return True
        return False

    def check_kind_4(self, cards):
        self.relevant = []
        freq = {}
        for c in cards:
            freq[c.rank_num()] = freq.setdefault(c.rank_num(), 0) + 1
        if freq.values().count(4) != 1:
            return False
        high = None
        for c in cards:
            if freq[c.rank_num()] == 4:
                self.relevant.append(c)
            elif not high:
                high = c
        self.relevant.append(high)
        return True

    def check_full(self, cards):
        self.relevant = []
        freq = {}
        for c in cards:
            freq[c.rank_num()] = freq.setdefault(c.rank_num(), 0) + 1

        if not (
            (freq.values().count(3) == 1 and freq.values().count(2) >= 1) or
            freq.values().count(3) == 2
        ):
            return False
        card2, card3 = None, None
        for c in cards:
            if freq[c.rank_num()] >= 3:
                card3 = c
                break
        for c in cards:
            if freq[c.rank_num()] >= 2 and c.rank_num() != card3.rank_num():
                card2 = c
                break
        for c in cards:
            if c.rank_num() == card3.rank_num():
                self.relevant.append(c)
        k = 0
        for c in cards:
            if c.rank_num() == card2.rank_num() and k < 2:
                self.relevant.append(c)
                k += 1
        return True

    def check_kind_3(self, cards):
        self.relevant = []
        freq = {}
        for c in cards:
            freq[c.rank_num()] = freq.setdefault(c.rank_num(), 0) + 1
        if 3 not in freq.values():
            return False
        for c in cards:
            if freq[c.rank_num()] == 3:
                self.relevant.append(c)
        k = 0
        for c in cards:
            if freq[c.rank_num()] < 3 and k < 2:
                self.relevant.append(c)
                k += 1
        return True

    def check_kind_2_2(self, cards):
        self.relevant = []
        freq = {}
        for c in cards:
            freq[c.rank_num()] = freq.setdefault(c.rank_num(), 0) + 1
        if freq.values().count(2) < 2:
            return False
        k = 0
        for c in cards:
            if k < 4:
                if freq[c.rank_num()] == 2:
                    self.relevant.append(c)
                    k += 1
        for c in cards:
            if c not in self.relevant:
                self.relevant.append(c)
                break
        return True

    def check_kind_2(self, cards):
        self.relevant = []
        freq = {}
        for c in cards:
            freq[c.rank_num()] = freq.setdefault(c.rank_num(), 0) + 1
        if freq.values().count(2) != 1:
            return False
        for c in cards:
            if freq[c.rank_num()] == 2:
                self.relevant.append(c)
        k = 0
        for c in cards:
            if c not in self.relevant and k < 3:
                self.relevant.append(c)
                k += 1
        return True
