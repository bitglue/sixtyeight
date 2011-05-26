from zope.interface import Interface, Attribute


class IQuotes(Interface):
    '''Stores the value of a thing at specified points in time.

    The data are stored in chronological order, oldest first.
    '''
    values = Attribute('a sequence of floats')
    dates = Attribute('a sequence of datetime.date instances')
    symbol = Attribute('the stock, fund symbol')

    def iterDateValues():
        '''Return an iterator over (date, value) pairs.'''


class IReturns(Interface):
    returns = Attribute('a sequence of floats')
    dates = Attribute('a sequence of datetime.date instances')
    symbol = Attribute('the stock, fund symbol')

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
    dates = Attribute('a sequence of datetime.date instances. These will be the same dates as in xQuotes and yQuotes.')
