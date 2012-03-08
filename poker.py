from poker_data import *
import itertools
import random

_SUITS = [1 << (i + 12) for i in range(4)]
_RANKS = [(1 << (i + 16)) | (i << 8) for i in range(13)]
_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
_DECK = [_RANKS[rank] | _SUITS[suit] | _PRIMES[rank] for rank, suit in 
    itertools.product(range(13), range(4))]

SUITS = 'cdhs'
RANKS = '23456789TJQKA'
DECK = [''.join(s) for s in itertools.product(RANKS, SUITS)]
LOOKUP = dict(zip(DECK, _DECK))

def hash_function(x):
    x += 0xe91aaa35
    x ^= x >> 16
    x += x << 8
    x &= 0xffffffff
    x ^= x >> 4
    b = (x >> 8) & 0x1ff
    a = (x + (x << 2)) >> 19
    r = (a ^ HASH_ADJUST[b]) & 0x1fff
    return HASH_VALUES[r]

def eval5(hand):
    c1, c2, c3, c4, c5 = (LOOKUP[x] for x in hand)
    q = (c1 | c2 | c3 | c4 | c5) >> 16
    if (0xf000 & c1 & c2 & c3 & c4 & c5):
        return FLUSHES[q]
    s = UNIQUE_5[q]
    if s:
        return s
    p = (c1 & 0xff) * (c2 & 0xff) * (c3 & 0xff) * (c4 & 0xff) * (c5 & 0xff)
    return hash_function(p)

def eval7(hand):
    return min(eval5(x) for x in itertools.combinations(hand, 5))

def one_round5():
    # shuffle a deck
    deck = list(DECK)
    random.shuffle(deck)
    # draw two hands
    hand1 = deck[:5]
    hand2 = deck[5:10]
    # evaluate the hands
    score1 = eval5(hand1)
    score2 = eval5(hand2)
    # display the winning hand
    hand1 = '[%s]' % ' '.join(hand1)
    hand2 = '[%s]' % ' '.join(hand2)
    if score1 < score2:
        print '%s beats %s' % (hand1, hand2)
    elif score1 == score2:
        print '%s ties %s' % (hand1, hand2)
    else:
        print '%s beats %s' % (hand2, hand1)

def one_round7():
    # shuffle a deck
    deck = list(DECK)
    random.shuffle(deck)
    # draw community and two hands
    community = deck[:5]
    hand1 = deck[5:7]
    hand2 = deck[7:9]
    # evaluate the hands
    score1 = eval7(community + hand1)
    score2 = eval7(community + hand2)
    # display the winning hand
    community = '[%s]' % ' '.join(community)
    hand1 = '[%s]' % ' '.join(hand1)
    hand2 = '[%s]' % ' '.join(hand2)
    print community
    if score1 < score2:
        print '%s beats %s' % (hand1, hand2)
    elif score1 == score2:
        print '%s ties %s' % (hand1, hand2)
    else:
        print '%s beats %s' % (hand2, hand1)
    print

if __name__ == '__main__':
    for _ in range(100):
        one_round7()
