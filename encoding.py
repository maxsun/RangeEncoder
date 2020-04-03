'''example implementation of arithmetic encoding'''
import string
import decimal
from decimal import *
from fractions import *
from typing import NamedTuple, Dict
from range_map import *

decimal.getcontext().prec = 100

Model = Dict[str, Decimal]

TERMINATE_SYMBOL = '~'
SYMBOLS = set(string.printable + TERMINATE_SYMBOL)


def build_interval(model: Model, interval: Range) -> RangeMap:
    interval_map = RangeMap()
    accum = interval.start
    for char in sorted(model):
        prob = model[char]
        interval_size = prob * interval.length()
        interval_map.add_range(char, Range(accum, accum + interval_size))
        accum += interval_size

    return interval_map


def encode(msg: str, model: Model) -> Decimal:
    i = build_interval(model, Range(0, 1))
    char_interval = None
    for char in msg + TERMINATE_SYMBOL:
        char_interval = i[char]
        i = build_interval(model, char_interval)
    return char_interval.average()


def decode(encoded_msg: Decimal, model: Model) -> str:
    i = build_interval(model, Range(0, 1))
    decoded_msg = ''
    while True:
        char = i.containing(encoded_msg)[0]
        if char == TERMINATE_SYMBOL:
            break
        i = build_interval(model, i[char])
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
