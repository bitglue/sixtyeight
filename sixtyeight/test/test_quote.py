from __future__ import division

from twisted.trial.unittest import TestCase
from zope.interface import implements
from zope.interface.verify import verifyObject
from twisted.python.util import sibpath
from twisted.web import client
from twisted.internet import defer
from itertools import izip
from datetime import date
import math

from sixtyeight import quote, isixtyeight

_threeDates = [date(2011, 05, 18), date(2011, 05, 19), date(2011, 05, 20)]
_threeValues = [12.38, 12.42, 12.33]

class TestQuotes(TestCase):
    def setUp(self):
        self.dates = _threeDates
        self.values = _threeValues
        self.quotes = quote.Quotes('SYM', self.dates, self.values)

    def test_interfaces(self):
        verifyObject(isixtyeight.IQuotes, self.quotes)
        self.assertEqual(self.quotes.dates, self.dates)
        self.assertEqual(self.quotes.values, self.values)
        self.assertEqual(self.quotes.symbol, 'SYM')

    def test_iterDateValues(self):
        self.assertEqual(list(self.quotes.iterDateValues()), zip(self.dates, self.values))


class TestAdaptation(TestCase):
    def test_IQuotes_to_IReturns(self):
        class Q(object):
            implements(isixtyeight.IQuotes)
            dates = _threeDates
            values = _threeValues
            symbol = 'SYMBOL'
            def iterDateValues(self):
                return izip(self.dates, self.values)
        quotes = Q()
        verifyObject(isixtyeight.IQuotes, quotes)
        verifyObject(isixtyeight.IReturns, isixtyeight.IReturns(quotes))


class TestReturns(TestCase):
    symbol = 'SYM'
    threeQuotes = quote.Quotes(symbol, _threeDates, _threeValues)

    def test_usual(self):
        returns = quote.Returns(self.threeQuotes)

        verifyObject(isixtyeight.IReturns, returns)
        self.assertEqual(returns.symbol, self.symbol)

        self.assertEqual(returns.returns, [math.log(12.42/12.38), math.log(12.33/12.42)])
        self.assertEqual(returns.dates, [date(2011, 05, 19), date(2011, 05, 20)])

    def test_noQuote(self):
        quotes = quote.Quotes(self.symbol, [], [])
        returns = quote.Returns(quotes)
        self.assertEqual(returns.returns, [])

    def test_oneQuote(self):
        quotes = quote.Quotes(self.symbol, [date(2011, 05, 18)], [12.38])
        returns = quote.Returns(quotes)
        self.assertEqual(returns.returns, [])

    def test_minReturn(self):
        returns = quote.Returns(self.threeQuotes)
        self.assertEqual(returns.minReturn(), math.log(12.33/12.42))

    def test_maxReturn(self):
        returns = quote.Returns(self.threeQuotes)
        self.assertEqual(returns.maxReturn(), math.log(12.42/12.38))

    def test_meanReturn(self):
        returns = quote.Returns(self.threeQuotes)
        self.assertEqual(returns.meanReturn(), (math.log(12.33/12.42) + math.log(12.42/12.38)) / 2)


class TestYahooSource(TestCase):
    symbol = 'ASDF!/'

    def setUp(self):
        self.source = quote.YahooSource()

        self.assertEqual(self.source.getPage, client.getPage)
        self.source.getPage = self.getPage

        self.assertEqual(self.source.url, 'http://ichart.finance.yahoo.com/table.csv')
        self.source.url = 'http://example.com/'

    def getPage(self, url):
        self.assertEqual(url, 'http://example.com/?s=ASDF%21%2F')
        data = open(sibpath(__file__, 'yahooQuotes.csv')).read()
        return defer.succeed(data)

    def test_interfaces(self):
        verifyObject(isixtyeight.IQuoteSource, self.source)

    def test_getQuotes(self):
        result = []
        d = self.source.getQuotes(self.symbol).addCallback(result.append)
        quotes, = result
        verifyObject(isixtyeight.IQuotes, quotes)
        self.assertEqual(quotes.dates, _threeDates)
        self.assertEqual(quotes.values, _threeValues)
        self.assertEqual(quotes.symbol, self.symbol)
        return d


class TestComparisonWindow(TestCase):
    def setUp(self):
        self.q1 = quote.Quotes('SYM', _threeDates, _threeValues)
        self.q2 = quote.Quotes('BOL', [_threeDates[1]], [13.55])

        self.window = quote.ComparisonWindow(self.q1, self.q2)

    def test_interfaces(self):
        verifyObject(isixtyeight.IComparisonWindow, self.window)

    def test_symbols(self):
        self.assertEqual(self.window.xQuotes.symbol, 'SYM')
        self.assertEqual(self.window.yQuotes.symbol, 'BOL')

    def test_commonDates(self):
        self.assertEqual(self.window.dates, [_threeDates[1]])
        self.assertEqual(self.window.dates, self.window.xQuotes.dates)
        self.assertEqual(self.window.dates, self.window.yQuotes.dates)

        self.assertEqual(self.window.xQuotes.values, [_threeValues[1]])
        self.assertEqual(self.window.yQuotes.values, [13.55])
