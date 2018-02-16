#!/bin/env python

""" Unit test getter functions of currency module """

# pylint: disable=no-member

import unittest
import currency

class TestCurrencyGetterFunctions(unittest.TestCase):
	""" test currency public functions """

	def test_name(self):
		""" test name """
		self.assertEqual(currency.name('USD'), 'US Dollar')
		self.assertEqual(currency.name('EGP'), 'Egyptian Pound')
		self.assertEqual(currency.name('HKD'), 'Hong Kong Dollar')
		self.assertEqual(currency.name('USD', plural=True), 'US dollars')
		self.assertEqual(currency.name('EGP', plural=True), 'Egyptian pounds')
		self.assertEqual(currency.name('HKD', plural=True), 'Hong Kong dollars')

	def test_symbol(self):
		""" test symbol """
		self.assertEqual(currency.symbol('USD'), '$')
		self.assertEqual(currency.symbol('EUR'), '€')
		self.assertEqual(currency.symbol('JPY'), '￥')

		self.assertEqual(currency.symbol('CAD'), '$')
		self.assertEqual(currency.symbol('CAD', native=False), 'CA$')
		self.assertEqual(currency.symbol('NOK'), 'kr')
		self.assertEqual(currency.symbol('NOK', native=False), 'Nkr')

	def test_decimal_digits(self):
		""" test number of decimals digit of a currency """
		self.assertEqual(currency.decimals('USD'), 2)
		self.assertEqual(currency.decimals('HUF'), 0)
		self.assertEqual(currency.decimals('LYD'), 3)

	def test_rounding(self):
		""" test rounding to maximum decimal in currency """
		self.assertEqual(currency.rounding(100.555, 'USD'), 100.56)
		self.assertEqual(currency.rounding(66.309, 'JPY'), 66)
		self.assertEqual(currency.rounding(23.109793, 'TND'), 23.110)

	def test_round_increment(self):
		""" test the increment used in rounding of currency """
		self.assertEqual(currency.roundto('AUD'), 0)
		self.assertEqual(currency.roundto('RUB'), 0)
		self.assertEqual(currency.roundto('CHF'), 0.05)

	def test_pretty(self):
		""" test formatting of currency price """
		self.assertEqual(currency.pretty(100000.000, 'USD'), '$100,000')
		self.assertEqual(currency.pretty(5000000.1234567, 'AUD'), 'AU$ 5,000,000.12')
		self.assertEqual(currency.pretty(24000.5443, 'EUR', trim=False), '€24,000.5443')
		self.assertEqual(currency.pretty(24000.5443, 'EUR', abbrev=False), '24,000.54 EUR')

	def test_info(self):
		""" test printing currency info """
		KRW_info = {
				'symbol': '₩',
				'name': 'South Korean Won',
				'symbol_native': '₩',
				'decimal_digits': 0,
				'rounding': 0,
				'code': 'KRW',
				'name_plural': 'South Korean won'
				}
		self.assertEqual(currency.info('KRW'), KRW_info)

# vim: nofoldenable
