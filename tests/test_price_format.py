import unittest
from decimal import Decimal

from price_format import format_inr, format_price_units, indian_number


class IndianPriceTests(unittest.TestCase):
    def test_rupee_grouping_and_crore_boundary(self):
        cases = [(0, '₹0'), (999, '₹999'), (1000, '₹1,000'),
                 (450000, '₹4,50,000'), (9999999, '₹99,99,999'),
                 (10000000, '₹1,00,00,000'), (12500000, '₹1,25,00,000')]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(format_inr(value), expected)

    def test_units_use_crore_only_at_the_boundary(self):
        self.assertEqual(format_price_units(450000), '₹4,50 lakh')
        self.assertEqual(format_price_units(9999999), '₹99,99 lakh')
        self.assertEqual(format_price_units(10000000), '₹1,00 crore')
        self.assertEqual(format_price_units(12500000), '₹1,25 crore')

    def test_rounding_negative_and_decimal_input(self):
        self.assertEqual(format_inr(Decimal('999.5')), '₹1,000')
        self.assertEqual(format_inr(-123456), '-₹1,23,456')
        self.assertEqual(indian_number(Decimal('1234567.25'), 2), '12,34,567.25')

    def test_non_finite_values_are_rejected(self):
        for value in [float('nan'), float('inf'), None, 'not a price']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                format_inr(value)


if __name__ == '__main__':
    unittest.main()
