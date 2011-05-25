from zope.interface import Interface, Attribute


class IQuotes(Interface):
    quotes = Attribute('a sequence of (date, value) pairs')
    symbol = Attribute('the stock, fund symbol')

    def findCommonDays(other):
        '''Find the days common to this and another IQuotes provider.

        Returns a pair of IQuotes providers that will have only quotes for days
        which the original two have in common. Either of the quotes in this
        pair may be the original quotes provided, or a new instance.
        '''


class IReturns(Interface):
    returns = Attribute('a sequence of (date, return) pairs')
    symbol = Attribute('the stock, fund symbol')

    def iterReturns():
        '''Return an iterator over just the returns (no date)'''

    def minReturn():
        '''Return the smallest single return'''

    def maxReturn():
        '''Return the greatest single return'''

    def meanReturn():
        '''Return the arithmetic mean return'''


class IQuoteSource(Interface):
    def getQuotes(symbol):
        '''Return a deferred IQuotes provider.'''
