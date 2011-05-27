def movingSum(x, n):
    if len(x) < n:
        return []

    if n == 1:
        return x

    s = 0
    tail = x[0]
    result = []

    for i in xrange(0, n-1):
        s += x[i]

    for i in xrange(n-1, len(x)):
        s += x[i]
        result.append(s)
        s -= tail
        tail = x[i-n+2]

    return result
