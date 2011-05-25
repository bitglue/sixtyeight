from zope.interface import implements
from twisted.web import client
import csv, urllib
from cStringIO import StringIO

from sixtyeight import isixtyeight


class Quotes(object):
    implements(isixtyeight.IQuotes)

    def __init__(self, symbol, quotes):
        self.symbol = symbol
        self.quotes = quotes


class YahooSource(object):
    implements(isixtyeight.IQuoteSource)

    getPage = staticmethod(client.getPage)
    url = 'http://ichart.finance.yahoo.com/table.csv'

    def getQuotes(self, symbol):
        url = '%s?s=%s' % (self.url, urllib.quote(symbol, safe=''))
        return self.getPage(url).addCallback(self._cbParseQuotes, symbol)

    def _cbParseQuotes(self, quoteData, symbol):
        r = csv.DictReader(StringIO(quoteData))
        quotes = [(row['Date'], float(row['Adj Close'])) for row in r]
        return Quotes(symbol, quotes)