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
