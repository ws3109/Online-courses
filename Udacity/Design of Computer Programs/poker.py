import random
import itertools

def poker(hands):
    return allmax(hands, key = hand_rank)

def allmax(hands, key = None):
    # break up the tie, i.e., return all hands with the highest rank
    result, max_val = [], None
    key = key or (lambda x: x)
    for hand in hands:
        score = key(hand)
        if not max_val or score > max_val:
            max_val, result = score, [hand]
        elif max_val == score:
            result.append(hand)
    return result

def hand_rank(hands):
    count_rank = {(4, 1): 7, (3, 2): 6, (3, 1, 1): 3, (2, 2, 1): 2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}
    groups = group(['--23456789TJQKA'.index(r) for r, s in hands])
    # a = [(1,2),(3,4),(5,6)], zip(*a) = [(1,3,5), (2,4,6)]
    counts, ranks = zip(*groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r, s in hands])) == 1
    return max(count_rank[counts], 4 * straight + 5 * flush), ranks

def group(items):
    # return a list of [(count_x, s)], highest count first, then highest x first.
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups,reverse=True)

'''
Different implementation of hand_rank, use if and else condition.
def hand_rank(hands):
    groups = group(['--23456789TJQKA'.index(r) for r, s in hands])
    counts, ranks = zip(*groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r, s in hands])) == 1
    return (8 if straight and flush else
            7 if counts == (4, 1) else
            6 if counts == (3, 2) else
            5 if flush else
            4 if straight else
            3 if counts == (3, 1, 1) else
            2 if counts == (2, 2, 1) else
            1 if counts == (2, 1, 1, 1) else
            0), ranks
allranks = '23456789TJQKA'
redcards = [r+s for r in allranks for s in 'DH']
blackcards = [r+s for r in allranks for s in 'SC']
def best_hand(hand):
    # If we have 7 cards, we want the best 5 cards.
    return max([itertools.combinations(hand, 5)], key = hand_rank)
def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selectios"
    hands = set(best_hand(x) for x in itertools.product(*map(replace, hand)))
    # itertools.product((1,2), (3,4)) = (1,3), (1,4), (2,3), (2,4)
    return max(hands, key = hand_rank)
If the form *identifier is present, it is initialized to a tuple receiving 
any excess positional parameters, defaulting to the empty tuple. 
If the form **identifier is present, it is initialized to a new dictionary receiving 
any excess keyword arguments, defaulting to a new empty dictionary.
def replace(card):
    if card == '?B': return blackcards
    elif card == '?R': return redcards
    else: return [card]
'''

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
def deal(numhands, n = 5, deck = mydeck):
    random.shuffle(deck)
    return [deck[n * i : n * (i+1)] for i in range(numhands)]

def test():
    sf1 = "6C 7C 8C 9C TC".split()  # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split()  # Straight Flush
    fk = "9D 9H 9S 9C 7D".split()  # Four of a Kind
    fh = "TD TC TH 7C 7D".split()  # Full House
    tp = "TD TC 7H 7C 3D".split()  # Full House
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    assert poker([fk, fk]) == [fk, fk]
    return 'tests pass'

test()
