from zope.interface import Interface, Attribute

class IQuotes(Interface):
    quotes = Attribute('a sequence of (date, value) pairs')
    symbol = Attribute('the stock, fund symbol')


class IQuoteSource(Interface):
    def getQuotes(symbol):
        '''Return a deferred IQuotes provider.'''
