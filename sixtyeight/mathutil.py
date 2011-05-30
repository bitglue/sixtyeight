from __future__ import division
from math import exp, pi


def movingSum(x, n):
    if len(x) < n:
        return []

    if n == 1:
        return x

    s = 0
    tail = x[0]
    result = []

    for i in xrange(0, n-1):
        s += x[i]

    for i in xrange(n-1, len(x)):
        s += x[i]
        result.append(s)
        s -= tail
        tail = x[i-n+2]

    return result


class IIR(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def filter(self, x):
        def getitem(seq, i):
            if i < 0:
                return 0
            return seq[i]

        y = []

        for i in xrange(len(x)):
            nextValue = 0
            for j, a in enumerate(self.a):
                nextValue += a * getitem(x, i-j)
            for j, b in enumerate(self.b):
                nextValue += b * getitem(y, i-1-j)
            y.append(nextValue)

        return y

    @classmethod
    def lowPass(cls, fc):
        x = exp(-2*pi*fc)
        return cls([1-x], [x])
