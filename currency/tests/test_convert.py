#!/bin/env python

""" Unit test converting and caching result between currencies """

# pylint: disable=no-member

import unittest
from unittest import mock
import os

import currency

def mocked_requests_get(*_, **kwargs):
	""" fake requests.get() operation by providing an api_url and expect the exact responses
	corresponding to a set of urls params below """
	usd_php_params = {'compact': 'ultra', 'q': 'USD_PHP'}
	eur_jpy_params = {'compact': 'ultra', 'q': 'EUR_JPY'}
	gbp_dkk_params = {'compact': 'ultra', 'q': 'GBP_DKK'}
	usd_eur_params = {'compact': 'ultra', 'q': 'USD_EUR'}

	class MockedRequestsModelsResponse():
		""" a fake result from requests.get() """
		def __init__(self, json_result, status_code):
			self.json_result = json_result
			self.status_code = status_code

		def json(self):
			""" a mock of requests.get().json() """
			return self.json_result

	if kwargs['params'] == usd_php_params:
		return MockedRequestsModelsResponse({'USD_PHP': 46.211}, 200)
	elif kwargs['params'] == eur_jpy_params:
		return MockedRequestsModelsResponse({'EUR_JPY': 133.2801}, 200)
	elif kwargs['params'] == gbp_dkk_params:
		return MockedRequestsModelsResponse({'GBP_DKK': 8.377764}, 200)
	elif kwargs['params'] == usd_eur_params:
		return MockedRequestsModelsResponse({'USD_EUR': 0.805001}, 200)
	return MockedRequestsModelsResponse({}, 200)

class TestCurrencyConverter(unittest.TestCase):
	""" test currency public functions """
	@classmethod
	def setUpClass(cls):
		""" Run before all the tests """
		cls.cache_path = os.path.join(os.path.dirname(__file__), 'cache')

	@classmethod
	def tearDownClass(cls):
		""" Run after all the tests """
		pass

	@mock.patch('currency.currency.requests.get', side_effect=mocked_requests_get)
	@mock.patch('currency.currency.cache.get_cache_path')
	def test_convert(self, mock_get_cache_path, _):
		""" test converting between currencies """
		mock_get_cache_path.return_value = '/tmp/test_cache_write'

		self.assertEqual(currency.convert('USD', 'PHP'), 46.211)
		self.assertEqual(currency.convert('EUR', 'JPY'), 133.2801)
		self.assertEqual(currency.convert('GBP', 'DKK'), 8.377764)

		self.assertEqual(currency.convert('USD', 'PHP', 2), 92.422)
		self.assertEqual(currency.convert('EUR', 'JPY', 10), 1332.801)
		self.assertEqual(currency.convert('GBP', 'DKK', 0), 0)

	@mock.patch('currency.currency.time.time')
	@mock.patch('currency.currency.cache.get_cache_path')
	def test_not_update_cache(self, mock_get_cache_path, mock_timenow):
		""" test should not requests API if cache data less than 30 mins old """
		mock_get_cache_path.return_value = self.cache_path
		mock_timenow.return_value = 900 # 15 mins
		usd_aud_cache = currency.cache.read()['USD']['AUD']['value']

		self.assertEqual(currency.convert('USD', 'AUD'), usd_aud_cache)

	@mock.patch('currency.currency.cache.write')
	@mock.patch('currency.currency.requests.get', side_effect=mocked_requests_get)
	@mock.patch('currency.currency.time.time')
	@mock.patch('currency.currency.cache.get_cache_path')
	def test_update_cache(self, mock_get_cache_path, mock_timenow, _, __):
		""" test to request API if cache data is 30 mins old """
		mock_get_cache_path.return_value = self.cache_path
		mock_timenow.return_value = 1800 # 30 mins

		self.assertEqual(currency.convert('USD', 'EUR'), 0.805001)

# vim: nofoldenable
