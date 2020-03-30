'''example implementation of arithmetic encoding'''
import string
import decimal
from decimal import *
from fractions import *
from typing import NamedTuple, Dict

decimal.getcontext().prec = 100


class Range(NamedTuple):
    '''Represents a range of Decimals'''
    start: Decimal
    end: Decimal

    def length(self) -> Decimal:
        '''Returns the length of the range'''
        return self.end - self.start

    def average(self) -> Decimal:
        '''Returns the midpoint of the range'''
        return (self.start + self.end) / 2

    def __contains__(self, num) -> bool:
        '''Returns whether the range contains <num>'''
        return self.start <= num and self.end > num


Model = Dict[str, Decimal]

TERMINATE_SYMBOL = '~'
SYMBOLS = set(string.printable + TERMINATE_SYMBOL)


def build_interval(model: Model, interval: Range) -> Dict[str, Range]:
    interval_map = {}
    accum = interval.start
    for char in sorted(model):
        prob = model[char]
        interval_size = prob * interval.length()
        interval_map[char] = Range(accum, accum + interval_size)
        accum += interval_size

    return interval_map


def encode(msg: str, model: Model) -> Decimal:
    i = build_interval(model, Range(Decimal(0), Decimal(1)))
    char_interval = None
    for char in msg + TERMINATE_SYMBOL:
        char_interval = i[char]
        i = build_interval(model, char_interval)
    if char_interval:
        return char_interval.average()

    raise Exception('No intervals found while encoding!')


def decode(encoded_msg: Decimal, model: Model) -> str:
    i = build_interval(model, Range(Decimal(0), Decimal(1)))
    decoded_msg = ''
    has_terminated = False
    while not has_terminated:
        for char in i:
            if encoded_msg in i[char]:
                i = build_interval(model, i[char])
                if char == TERMINATE_SYMBOL:
                    has_terminated = True
                    break
                else:
                    decoded_msg += char

    return decoded_msg


MSG = 'One small step for man...'

pdf = {}
for char in SYMBOLS:
    pdf[char] = Decimal(1 / (len(SYMBOLS)))


c = encode(MSG, pdf)
print(c)
x = decode(c, pdf)
print(x)
