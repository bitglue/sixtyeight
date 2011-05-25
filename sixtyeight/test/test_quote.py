from __future__ import division

from twisted.trial.unittest import TestCase
from zope.interface.verify import verifyObject
from twisted.python.util import sibpath
from twisted.web import client
from twisted.internet import defer
import math

from sixtyeight import quote, isixtyeight

class TestQuotes(TestCase):
    def setUp(self):
        self._q = object()
        self.quotes = quote.Quotes('SYM', self._q)

    def test_interfaces(self):
        verifyObject(isixtyeight.IQuotes, self.quotes)
        self.assertEqual(self.quotes.quotes, self._q)
        self.assertEqual(self.quotes.symbol, 'SYM')


class TestReturns(TestCase):
    symbol = 'SYM'
    threeQuotes = quote.Quotes(symbol, [
        ('2011-05-20', 12.33),
        ('2011-05-19', 12.42),
        ('2011-05-18', 12.38),
    ])

    def test_usual(self):
        returns = quote.Returns(self.threeQuotes)

        verifyObject(isixtyeight.IReturns, returns)
        self.assertEqual(returns.symbol, self.symbol)

        self.assertEqual(returns.returns, [
            ('2011-05-20', math.log(12.33/12.42)),
            ('2011-05-19', math.log(12.42/12.38)),
        ])

    def test_noQuote(self):
        quotes = quote.Quotes(self.symbol, [])
        returns = quote.Returns(quotes)
        self.assertEqual(returns.returns, [])

    def test_oneQuote(self):
        quotes = quote.Quotes(self.symbol, [
            ('2011-05-18', 12.38),
        ])
        returns = quote.Returns(quotes)
        self.assertEqual(returns.returns, [])

    def test_iterReturns(self):
        returns = quote.Returns(self.threeQuotes)
        i = returns.iterReturns()
        self.assertEqual(i, iter(i))
        self.assertEqual(list(i), [
            math.log(12.33/12.42),
            math.log(12.42/12.38),
       ])

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
        self.assertEqual(quotes.quotes, [
            ('2011-05-20', 12.33),
            ('2011-05-19', 12.42),
            ('2011-05-18', 12.38),
        ])
        self.assertEqual(quotes.symbol, self.symbol)
        return d
