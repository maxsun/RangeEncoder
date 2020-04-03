'''example implementation of arithmetic encoding'''
import string
from decimal import *
from typing import NamedTuple, Dict
from range_map import *


Model = Dict[str, Decimal]

TERMINATE_SYMBOL = '~'
SYMBOLS = set(string.printable + TERMINATE_SYMBOL)


def build_range_map(model: Model, interval: Range) -> RangeMap:
    rm = RangeMap()
    accum = interval.start
    for char in sorted(model):
        prob = model[char]
        interval_size = prob * interval.length()
        rm.add_range(char, Range(accum, accum + interval_size))
        accum += interval_size

    return rm


def encode(msg: str, model: Model) -> Decimal:
    rm = build_range_map(model, Range(0, 1))
    char_interval = None
    for char in msg + TERMINATE_SYMBOL:
        char_interval = rm[char]
        rm = build_range_map(model, char_interval)
    return char_interval.average()


def decode(encoded_msg: Decimal, model: Model) -> str:
    rm = build_range_map(model, Range(0, 1))
    decoded_msg = ''
    while True:
        char = rm.containing(encoded_msg)[0]
        if char == TERMINATE_SYMBOL:
            break
        rm = build_range_map(model, rm[char])
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
