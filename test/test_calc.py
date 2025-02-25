from calc.calc import square_root, factorial, natural_logarithm, power
import unittest
import math
import sys, os

class TestCalculatorFunctions(unittest.TestCase):
    # ... (rest of the test code remains the same) ...
    def test_square_root_positive(self):
        self.assertAlmostEqual(square_root(9), 3.0)
        self.assertAlmostEqual(square_root(16), 4.0)
        self.assertAlmostEqual(square_root(2), math.sqrt(2))

    def test_square_root_zero(self):
        self.assertAlmostEqual(square_root(0), 0.0)

    def test_square_root_negative(self):
        self.assertIsNone(square_root(-1))
        self.assertIsNone(square_root(-9))

    def test_factorial_positive(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)

    def test_factorial_negative(self):
        self.assertIsNone(factorial(-1))
        self.assertIsNone(factorial(-5))

    def test_factorial_non_integer(self):
        self.assertIsNone(factorial(1.5))
        self.assertIsNone(factorial(2.7))

    def test_natural_logarithm_positive(self):
        self.assertAlmostEqual(natural_logarithm(1), 0.0)
        self.assertAlmostEqual(natural_logarithm(math.e), 1.0)
        self.assertAlmostEqual(natural_logarithm(10), math.log(10))

    def test_natural_logarithm_zero(self):
        self.assertIsNone(natural_logarithm(0))

    def test_natural_logarithm_negative(self):
        self.assertIsNone(natural_logarithm(-1))
        self.assertIsNone(natural_logarithm(-10))

    def test_power_positive_base_and_exponent(self):
        self.assertAlmostEqual(power(2, 3), 8.0)
        self.assertAlmostEqual(power(3, 2), 9.0)
        self.assertAlmostEqual(power(2.5, 2), 6.25)

    def test_power_zero_exponent(self):
        self.assertAlmostEqual(power(5, 0), 1.0)
        self.assertAlmostEqual(power(0, 0), 1.0)

    def test_power_zero_base(self):
        self.assertAlmostEqual(power(0, 5), 0.0)

    def test_power_negative_exponent(self):
        self.assertAlmostEqual(power(2, -1), 0.5)
        self.assertAlmostEqual(power(4,-2),0.0625)

    def test_power_negative_base(self):
        self.assertAlmostEqual(power(-2,3),-8.0)
        self.assertAlmostEqual(power(-2,2),4.0)
