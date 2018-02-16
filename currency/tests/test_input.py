#!/bin/env python

""" Unit test parameters passed in functions """

# pylint: disable=no-member

import unittest
from currency.exceptions import CurrencyException
import currency

class TestInput(unittest.TestCase):
	""" test currency public functions """

	def test_currency_input(self):
		""" test user input to uppercase currency code """
		self.assertEqual(currency.name('USD'), 'US Dollar')
		self.assertEqual(currency.name('usd'), 'US Dollar')
		self.assertEqual(currency.name('Usd'), 'US Dollar')
		with self.assertRaises(CurrencyException):
			currency.name('XXX')

	def test_price_input(self):
		""" test price datatype """
		self.assertEqual(currency.pretty(24000.00, 'EUR'), '€24,000')
		self.assertEqual(currency.pretty(24000.01, 'EUR'), '€24,000.01')
		self.assertEqual(currency.pretty('24000.01', 'EUR'), '€24,000.01')

# vim: nofoldenable
