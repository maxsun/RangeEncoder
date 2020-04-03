
import decimal
from decimal import Decimal
from typing import NamedTuple

decimal.getcontext().prec = 100

class Range:
    '''Represents a range of Decimals'''
    start: Decimal
    end: Decimal

    def __init__(self, start, end):
        self.start = Decimal(start)
        self.end = Decimal(end)

    def __repr__(self) -> str:
        return '(%0f, %0f)' % (self.start, self.end)

    def length(self) -> Decimal:
        '''Returns the length of the range'''
        return self.end - self.start

    def average(self) -> Decimal:
        '''Returns the midpoint of the range'''
        return (self.start + self.end) / 2

    def __contains__(self, num) -> bool:
        '''Returns whether the range contains <num>'''
        return self.start <= num and self.end > num


class RangeMap:
    '''maps a Decimal to the Ranges which include it'''

    ranges = {}
    min = 0
    max = 0

    def add_range(self, range_id: str, rng: Range) -> None:
        '''Add a IDed range to the RangeMap'''
        if rng.start < self.min:
            self.min = rng.start
        if rng.end > self.max:
            self.max = rng.end

        self.ranges[range_id] = rng

    def containing(self, value):
        '''Find the ranges <value> belongs in'''
        if value < self.min or value > self.max:
            return []
        results = []
        for rng_id in self.ranges:
            if value in self.ranges[rng_id]:
                results.append(rng_id)
        return results

    def __setitem__(self, key, item):
        self.ranges[key] = item

    def __getitem__(self, key):
        return self.ranges[key]

