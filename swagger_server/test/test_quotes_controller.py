# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.quote import Quote  # noqa: E501
from swagger_server.models.quotes import Quotes  # noqa: E501
from swagger_server.test import BaseTestCase


class TestQuotesController(BaseTestCase):
    """QuotesController integration test stubs"""

    def test_quotes_random_get(self):
        """Test case for quotes_random_get

        Get a random quote
        """
        response = self.client.open(
            '/quotes/random',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_quotes_search_get(self):
        """Test case for quotes_search_get

        Get a quote or quotes by quote's part
        """
        query_string = [('text', 'text_example')]
        response = self.client.open(
            '/quotes/search',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
