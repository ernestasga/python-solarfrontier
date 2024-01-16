from python_solarfrontier.api import SolarFrontierAPI
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import asyncio
import aiohttp

class TestSolarFrontierAPI(unittest.TestCase):

    def setUp(self):
        self.api = SolarFrontierAPI('localhost')

    def test_initialization(self):
        self.assertEqual(self.api.host, 'http://localhost')
        
    def test_valid_http_url(self):
        api = SolarFrontierAPI('http://example.com')
        self.assertEqual(api.host, 'http://example.com')

    def test_valid_https_url(self):
        api = SolarFrontierAPI('https://example.com')
        self.assertEqual(api.host, 'https://example.com')

    def test_invalid_url_format(self):
        api = SolarFrontierAPI('example.com')
        self.assertEqual(api.host, 'http://example.com')

    def test_ip_address_as_host(self):
        api = SolarFrontierAPI('192.168.1.1')
        self.assertEqual(api.host, 'http://192.168.1.1')

    def test_localhost_as_host(self):
        api = SolarFrontierAPI('localhost')
        self.assertEqual(api.host, 'http://localhost')

    def test_empty_string_as_host(self):
        api = SolarFrontierAPI('')
        self.assertEqual(api.host, 'http://')

    # Test test_connection()

    @patch('aiohttp.ClientSession.get')
    def test_test_connection_successful(self, mock_get):
        # Mock a successful response
        mock_response_text = '<td>Name</td><td>test_model</td>'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.test_connection())
        self.assertTrue(result)

    @patch('aiohttp.ClientSession.get')
    def test_test_connection_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.test_connection())
        self.assertFalse(result)

    @patch('aiohttp.ClientSession.get')
    def test_test_connection_unexpected_response(self, mock_get):
        # Mock an unexpected response
        mock_response_text = 'unexpected response format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.test_connection())
        self.assertFalse(result)

    # Tests for get_system_info()

    @patch('aiohttp.ClientSession.get')
    def test_get_system_info_successful(self, mock_get):
        # Mock a successful response
        mock_response_text = '<td>Name</td><td>test_model</td>'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_system_info())
        self.assertEqual(result, {'model_name': 'test_model'})

    @patch('aiohttp.ClientSession.get')
    def test_get_system_info_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.get_system_info())
        self.assertEqual(result, {})

    @patch('aiohttp.ClientSession.get')
    def test_get_system_info_unexpected_response(self, mock_get):
        # Mock an unexpected response
        mock_response_text = 'unexpected response format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_system_info())
        self.assertEqual(result, {})

    # Tests for get_measurements()

    @patch('aiohttp.ClientSession.get')
    def test_get_measurements_success(self, mock_get):
        # Mock a successful response
        mock_response_text = "<tr><td>P DC</td><td align='right'>5.0</td><td>W</td></tr>"  # Example format
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_measurements())
        self.assertEqual(result.get('dc_power'), '5.0W')

    @patch('aiohttp.ClientSession.get')
    def test_get_measurements_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.get_measurements())
        self.assertEqual(result, {})

    @patch('aiohttp.ClientSession.get')
    def test_get_measurements_unexpected_response(self, mock_get):
        # Mock an unexpected response format
        mock_response_text = 'unexpected format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_measurements())
        self.assertEqual(result, {})

    # Tests for get_yield_day()

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_day_success(self, mock_get):
        # Mock a successful response
        mock_response_text = 'document.getElementById("labelValueId").innerHTML = "5.0Wh"'  # Example format
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_day())
        self.assertEqual(result, '5.0Wh')

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_day_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.get_yield_day())
        self.assertEqual(result, 0.0)

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_day_unexpected_response(self, mock_get):
        # Mock an unexpected response format
        mock_response_text = 'unexpected format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_day())
        self.assertEqual(result, None)
        
    # Tests for get_yield_month()

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_month_success(self, mock_get):
        # Mock a successful response
        mock_response_text = 'document.getElementById("labelValueId").innerHTML = "100.0Wh"'  # Example format
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_month())
        self.assertEqual(result, '100.0Wh')

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_month_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.get_yield_month())
        self.assertEqual(result, 0.0)

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_month_unexpected_response(self, mock_get):
        # Mock an unexpected response format
        mock_response_text = 'unexpected format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_month())
        self.assertEqual(result, None)

    # Tests for get_yield_year()

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_year_success(self, mock_get):
        # Mock a successful response
        mock_response_text = 'document.getElementById("labelValueId").innerHTML = "500.0Wh"'  # Example format
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_year())
        self.assertEqual(result, '500.0Wh')

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_year_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.get_yield_year())
        self.assertEqual(result, 0.0)

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_year_unexpected_response(self, mock_get):
        # Mock an unexpected response format
        mock_response_text = 'unexpected format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_year())
        self.assertEqual(result, None)

    # Tests for get_yield_total()

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_total_success(self, mock_get):
        # Mock a successful response
        mock_response_text = 'document.getElementById("labelValueId").innerHTML = "1000.0Wh"'  # Example format
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_total())
        self.assertEqual(result, '1000.0Wh')

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_total_client_error(self, mock_get):
        # Mock a client error
        mock_get.side_effect = aiohttp.ClientError

        result = asyncio.run(self.api.get_yield_total())
        self.assertEqual(result, 0.0)

    @patch('aiohttp.ClientSession.get')
    def test_get_yield_total_unexpected_response(self, mock_get):
        # Mock an unexpected response format
        mock_response_text = 'unexpected format'
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_response_text)

        result = asyncio.run(self.api.get_yield_total())
        self.assertEqual(result, None)

    # Tests for close()

    @patch('aiohttp.ClientSession.close', new_callable=AsyncMock)
    def test_close(self, mock_close):
        session = self.api.session

        # Close the API session
        asyncio.run(self.api.close())

        # Check if the close method of the session was called
        mock_close.assert_called()


    def tearDown(self):
        # check if the session is closed
        asyncio.run(self.api.close())

    

if __name__ == '__main__':
    unittest.main()