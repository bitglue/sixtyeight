sixtyeight
==========

Apply naive data analysis to investment performance.

This is a crude hack written to satisify my own curiosity, long ago.
Here's the problem: I had professional advisors suggesting that I
invest my retirement in managed funds with a relatively high expense
ratio. The manager, I was told, is a really smart cookie, and by
giving up some of my gains to pay him, he'd earn for me higher gains
relative to an index fund.

This should be a pretty easy hypothesis to test, I thought. After
all, index and managed funds are nothing new. Daily quotes are
available for free to anyone on the internet going back for years.
There should be some easy way to compare the past performance of
two options, right?

Apparently not. Typically, the everyday Joe is presented with the
returns of some investment option in the past 1, 5, and 10 years.
This is horrible. That the 10 year return is high doesn't indicate
consistent performance over 10 years. It means that exactly 10 years
ago, the price of that investment option was especially low. It
compares exactly two instants in time (10 years ago and today) and
says nothing of what happened between those times. Maybe 10 years ago,
there was a huge crash in some segment where the fund was heavily
invested. That's coincidence, not management skill.

If some investment option is truly superior, we should be able to
pick any period length, and for most such periods, the return should
be better than some benchmark.

That's esentially what this does. Taking my dilema as an example,
run `python plotstocks.py SWPPX VVOAX`. The first graph is the relative
value of the two, with their earliest common date normalized as 1.

The next graph, "cumulative excess return", shows the integral of the
difference of the two. If this line is flat, the two are matching in
performance at that point in time. If the line is going up, VVOAX is
outperforming SWPPX. Going down, VVOAX is underperforming. The red line
is a best fit linear trend, but frequently the relationship is anything
but linear, so the trend has little meaning.

Next, "rolling excess return" is essentially the smoothed derivitive
of the previous graph. The smoothing is done by taking a sliding window
of some number of trading days. The default of 250 days corresponds to
one year on the calandar. If at some point on the graph the value is
above 0, it means that if I bought VVOAX one year ago then sold it, I
did better than if I did the same with SWPPX. If VVOAX is better than
SWPPX, then the line should be positive more often than not.
