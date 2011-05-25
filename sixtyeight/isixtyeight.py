from zope.interface import Interface, Attribute


class IQuotes(Interface):
    quotes = Attribute('a sequence of (date, value) pairs')
    symbol = Attribute('the stock, fund symbol')


class IReturns(Interface):
    returns = Attribute('a sequence of (date, return) pairs')
    symbol = Attribute('the stock, fund symbol')

    def iterReturns():
        '''Return an iterator over just the returns (no date)'''


class IQuoteSource(Interface):
    def getQuotes(symbol):
        '''Return a deferred IQuotes provider.'''
