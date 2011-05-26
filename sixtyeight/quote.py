from __future__ import division
from itertools import izip
from zope.interface import implements
from twisted.python import components
from twisted.web import client
import csv, urllib, math, datetime
from cStringIO import StringIO

from sixtyeight import isixtyeight


class Quotes(object):
    implements(isixtyeight.IQuotes)

    def __init__(self, symbol, dates, values):
        self.symbol = symbol
        self.dates = dates
        self.values = values

    def iterDateValues(self):
        return izip(self.dates, self.values)


class Returns(object):
    implements(isixtyeight.IReturns)

    def __init__(self, quotes):
        self.symbol = quotes.symbol
        self.dates = []
        self.returns = []

        iterDV = quotes.iterDateValues()

        for prevDate, prevValue in iterDV:
            break

        for date, value in iterDV:
            self.dates.append(date)
            self.returns.append(math.log(value/prevValue))
            prevDate, prevValue = date, value

    def minReturn(self):
        return min(self.returns)

    def maxReturn(self):
        return max(self.returns)

    def meanReturn(self):
        return sum(self.returns) / len(self.returns)


class YahooSource(object):
    implements(isixtyeight.IQuoteSource)

    getPage = staticmethod(client.getPage)
    url = 'http://ichart.finance.yahoo.com/table.csv'

    def getQuotes(self, symbol):
        url = '%s?s=%s' % (self.url, urllib.quote(symbol, safe=''))
        return self.getPage(url).addCallback(self._cbParseQuotes, symbol)

    def _cbParseQuotes(self, quoteData, symbol):
        try:
            def parseDate(d):
                return datetime.date(*map(int, d.split('-')))
            dates = []
            values = []
            for row in csv.DictReader(StringIO(quoteData)):
                dates.append(parseDate(row['Date']))
                values.append(float(row['Adj Close']))

            dates.reverse()
            values.reverse()
            return Quotes(symbol, dates, values)
        except:
            import traceback
            traceback.print_exc()


class ComparisonWindow(object):
    implements(isixtyeight.IComparisonWindow)

    def __init__(self, xQuotes, yQuotes):
        self.dates, self.xQuotes, self.yQuotes = self._findCommonDays(xQuotes, yQuotes)

    @staticmethod
    def _findCommonDays(self, other):
        myQuotes = dict(self.iterDateValues())
        myResults = []
        otherResults = []
        dates = []
        for d, q in other.iterDateValues():
            if d in myQuotes:
                dates.append(d)
                myResults.append(myQuotes[d])
                otherResults.append(q)
        return dates, Quotes(self.symbol, dates, myResults), Quotes(other.symbol, dates, otherResults)


components.registerAdapter(Returns, isixtyeight.IQuotes, isixtyeight.IReturns)
