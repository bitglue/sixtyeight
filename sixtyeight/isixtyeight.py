from zope.interface import Interface, Attribute


class IQuotes(Interface):
    quotes = Attribute('a sequence of (date, value) pairs')
    symbol = Attribute('the stock, fund symbol')


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


class IComparisonWindow(Interface):
    '''A pair of quotes with common dates.
    
    Forms the basis for a number of performance vs. benchmark tests.

    Providers of this interface guarantee that each of the referenced quotes
    will have all of their dates in common.
    '''
    xQuotes = Attribute('provides IQuotes, with the same set of dates as yQuotes')
    yQuotes = Attribute('provides IQuotes, with the same set of dates as xQuotes')
