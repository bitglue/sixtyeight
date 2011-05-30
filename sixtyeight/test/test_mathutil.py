from twisted.trial.unittest import TestCase

from sixtyeight import mathutil

class TestMovingSum(TestCase):
    def test_usual(self):
        r = range(6)
        s = mathutil.movingSum(r, 3)
        self.assertEqual(s, [3, 6, 9, 12])

    def test_inputTooShort(self):
        r = range(5)
        s = mathutil.movingSum(r, 6)
        self.assertEqual(s, [])

    def test_emptyInput(self):
        r = []
        s = mathutil.movingSum(r, 2)
        self.assertEqual(s, [])

    def test_windowOne(self):
        r = range(10)
        s = mathutil.movingSum(r, 1)
        self.assertEqual(r, s)

    def test_inputJustBigEnough(self):
        r = range(5)
        s = mathutil.movingSum(r, 5)
        self.assertEqual(s, [sum(r)])


class TestIIR(TestCase):
    def test_identity(self):
        f = mathutil.IIR([1], [0])
        x = range(5)
        y = f.filter(x)
        self.assertEqual(x, y)

    def test_init(self):
        a = [2, 3]
        b = [4, 5]
        f = mathutil.IIR(a, b)
        self.assertEqual(f.a, a)
        self.assertEqual(f.b, b)

        x = range(4)
        y = f.filter(x)

        self.assertEqual(len(x), len(y))

        i = 0
        self.assertEqual(y[i], a[0]*x[i] + 0           + 0           + 0          )

        i = 1
        self.assertEqual(y[i], a[0]*x[i] + a[1]*x[i-1] + b[0]*y[i-1] + 0          )

        i = 2
        self.assertEqual(y[i], a[0]*x[i] + a[1]*x[i-1] + b[0]*y[i-1] + b[1]*y[i-2])

        i = 3
        self.assertEqual(y[i], a[0]*x[i] + a[1]*x[i-1] + b[0]*y[i-1] + b[1]*y[i-2])
