import unittest

from stock import Stock


class TestStock(unittest.TestCase):
    def test_create(self):
        s = Stock('goog', 100, 490.1)
        self.assertEqual(s.name, 'goog')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_create_with_kwargs(self):
        s = Stock(name='goog', shares=100, price=490.1)
        self.assertEqual(s.name, 'goog')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_cost(self):
        s = Stock('goog', 100, 490.1)
        self.assertEqual(s.cost, 49010)

    def test_sell(self):
        s = Stock('goog', 100, 490.1)
        s.sell(20)
        self.assertEqual(s.shares, 80)
        self.assertEqual(s.price, 490.1)

    def test_from_row(self):
        s = Stock.from_row(['goog', 100, 490.1])
        self.assertEqual(s.name, 'goog')
        self.assertEqual(s.shares, 100)
        self.assertEqual(s.price, 490.1)

    def test_repr(self):
        s = Stock('goog', 100, 490.1)
        self.assertEqual(
            repr(s),
            # "Stock(name='goog', shares=100, price=490.1)",
            "Stock('goog', 100, 490.1)",
        )

    def test_equal(self):
        s1 = Stock('goog', 100, 490.1)
        s2 = Stock('goog', 100, 490.1)
        self.assertTrue(s1 == s2)

    def test_bad_shares_type(self):
        s = Stock('goog', 100, 490.1)
        with self.assertRaises(TypeError):
            s.shares = '50'

    def test_bad_shares_value(self):
        s = Stock('goog', 100, 490.1)
        with self.assertRaises(ValueError):
            s.shares = -1

    def test_bad_price_type(self):
        s = Stock('goog', 100, 490.1)
        with self.assertRaises(TypeError):
            s.price = '50'

    def test_bad_price_value(self):
        s = Stock('goog', 100, 490.1)
        with self.assertRaises(ValueError):
            s.price = -1.5


if __name__ == '__main__':
    unittest.main()