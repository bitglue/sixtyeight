#!/usr/bin/python

from __future__ import division
import sys
from matplotlib import pyplot, mlab
from itertools import izip
from scipy.stats import linregress
from twisted.internet import reactor, defer
from sixtyeight import quote, isixtyeight, mathutil


def main():
    source = quote.YahooSource()
    defer.DeferredList([source.getQuotes(sys.argv[1]), source.getQuotes(sys.argv[2])], fireOnOneErrback=True).addCallback(gotQuotes).addBoth(end)
    reactor.run()

def end(f):
    if f:
        print f
    reactor.stop()

def gotQuotes(quotes):
    ((_, quotesX), (_, quotesY)) = quotes

    #f = mathutil.IIR.lowPass(1/40)
    #quotesX.values = f.filter(f.filter(f.filter(f.filter(quotesX.values))))
    #quotesY.values = f.filter(f.filter(f.filter(f.filter(quotesY.values))))

    window = quote.ComparisonWindow(quotesX, quotesY)
    returnsX = isixtyeight.IReturns(window.xQuotes)
    returnsY = isixtyeight.IReturns(window.yQuotes)

    minReturn = min([returnsX.minReturn(), returnsY.minReturn()])
    maxReturn = max([returnsX.maxReturn(), returnsY.maxReturn()])

    print 'mean day logrithmic returns'
    print '%s: %g' % (returnsX.symbol, returnsX.meanReturn())
    print '%s: %g' % (returnsY.symbol, returnsY.meanReturn())

    fig = pyplot.figure(1, figsize=(5.5,5.5))

    x = returnsX.returns
    y = returnsY.returns

    axScatter = fig.add_subplot(1, 2, 2)
    axScatter.set_title('daily return correlation')
    axScatter.scatter(x, y, s=1)
    axScatter.set_xlabel(window.xQuotes.symbol)
    axScatter.set_ylabel(window.yQuotes.symbol)

    m, b, r, p, e = linregress(x, y)

    print "y = %g * x + %g" % (m, b)
    print "r^2 = %g" % (r**2,)
    print "p = %g" % (p,)
    print "standard error = %g" % (e,)
    axScatter.plot([minReturn, maxReturn], [minReturn, maxReturn], 'g')
    axScatter.plot([min(x), max(x)], [m*min(x) + b, m*max(x) + b], 'r')
    axScatter.set_aspect(1.)

    axValue = fig.add_subplot(4, 2, 1)
    axValue.set_title('relative value')

    axValue.set_yscale('log', basey=2)
    axValue.plot(window.xQuotes.dates, [v / window.xQuotes.values[0] for v in window.xQuotes.values], label=window.xQuotes.symbol)
    axValue.plot(window.yQuotes.dates, [v / window.yQuotes.values[0] for v in window.yQuotes.values], label=window.yQuotes.symbol)
    axValue.legend(loc=0, ncol=2)

    returnDiffs = [y-x for (x,y) in izip(returnsX.returns, returnsY.returns)]
    axExcess = fig.add_subplot(2, 2, 3)
    axExcess.set_title('rolling excess return (%s over %s)' % (window.yQuotes.symbol, window.xQuotes.symbol))

    axExcess.set_ylabel('excess force of interest (%)')
    axExcess.set_xlabel('period ending')

    oneYear = [i*25000 for i in mlab.movavg(returnDiffs, 250)]
    axExcess.plot(returnsX.dates[250-1:], oneYear, label="250 day")
    #threeYear = [i*25000 for i in mlab.movavg(returnDiffs, 250*3)]
    #axExcess.plot(returnsX.dates[250*3-1:], threeYear, label="3 yr", color="green")
    #fiveYear = [i*25000 for i in mlab.movavg(returnDiffs, 250*5)]
    #axExcess.plot(returnsX.dates[250*5-1:], fiveYear, label="5 yr", color="red")
    axExcess.axhline(color="black")
    axExcess.axhline(y=sum(oneYear)/len(oneYear), color="blue")
    #axExcess.axhline(y=sum(threeYear)/len(threeYear), color="green")
    #axExcess.axhline(y=sum(fiveYear)/len(fiveYear), color="red")

    axExcess.set_xlim((window.dates[0], window.dates[-1]))
    axExcess.legend(loc='upper left', ncol=4)

    axAccum = fig.add_subplot(4, 2, 3)
    axAccum.set_title('cumulative excess return (%s over %s)' % (window.yQuotes.symbol, window.xQuotes.symbol))
    acc = 0
    accList = []
    for x, y in izip(returnsX.returns, returnsY.returns):
        acc += y-x
        accList.append(acc)

    axAccum.plot(returnsX.dates, accList)
    axAccum.set_xlim((window.dates[0], window.dates[-1]))

    x = [d.toordinal() for d in returnsX.dates]
    m, b, r, p, e = linregress(x, accList)

    #print "y = %g * x + %g" % (m, b)
    #print "r^2 = %g" % (r**2,)
    #print "p = %g" % (p,)
    #print "standard error = %g" % (e,)
    axAccum.plot([min(returnsX.dates), max(returnsX.dates)], [m*min(x) + b, m*max(x) + b], 'r')

    pyplot.draw()
    pyplot.show()

if __name__ == '__main__':
    main()
