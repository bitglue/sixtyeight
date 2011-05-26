from __future__ import division
from zope.interface import implements
from twisted.python import components
from twisted.web import client
import csv, urllib, math, datetime
from cStringIO import StringIO

from sixtyeight import isixtyeight


class Quotes(object):
    implements(isixtyeight.IQuotes)

    def __init__(self, symbol, quotes):
        self.symbol = symbol
        self.quotes = quotes


class Returns(object):
    implements(isixtyeight.IReturns)

    def __init__(self, quotes):
        self.symbol = quotes.symbol
        self.returns = []

        iterQuotes = iter(quotes.quotes)

        for date, value in iterQuotes:
            break

        for prevDate, prevValue in iterQuotes:
            self.returns.append((date, math.log(value/prevValue)))
            date, value = prevDate, prevValue

    def iterReturns(self):
        for date, ret in self.returns:
            yield ret

    def minReturn(self):
        return min(self.iterReturns())

    def maxReturn(self):
        return max(self.iterReturns())

    def meanReturn(self):
        return sum(self.iterReturns()) / len(self.returns)


class YahooSource(object):
    implements(isixtyeight.IQuoteSource)

    getPage = staticmethod(client.getPage)
    url = 'http://ichart.finance.yahoo.com/table.csv'

    def getQuotes(self, symbol):
        url = '%s?s=%s' % (self.url, urllib.quote(symbol, safe=''))
        return self.getPage(url).addCallback(self._cbParseQuotes, symbol)

    def _cbParseQuotes(self, quoteData, symbol):
        r = csv.DictReader(StringIO(quoteData))
        def parseDate(d):
            return datetime.date(*map(int, d.split('-')))
        quotes = [(parseDate(row['Date']), float(row['Adj Close'])) for row in r]
        return Quotes(symbol, quotes)


class ComparisonWindow(object):
    implements(isixtyeight.IComparisonWindow)

    def __init__(self, xQuotes, yQuotes):
        self.xQuotes, self.yQuotes = self._findCommonDays(xQuotes, yQuotes)

    @staticmethod
    def _findCommonDays(self, other):
        myQuotes = dict(self.quotes)
        myResults = []
        otherResults = []
        for d, q in other.quotes:
            if d in myQuotes:
                myResults.append((d, myQuotes[d]))
                otherResults.append((d, q))
        return Quotes(self.symbol, myResults), Quotes(other.symbol, otherResults)


components.registerAdapter(Returns, isixtyeight.IQuotes, isixtyeight.IReturns)
