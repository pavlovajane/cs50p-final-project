# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.scene_number_or_name import SceneNumberOrName  # noqa: E501
from swagger_server.models.scene_with_quotes import SceneWithQuotes  # noqa: E501
from swagger_server.test import BaseTestCase


class TestScenesController(BaseTestCase):
    """ScenesController integration test stubs"""

    def test_scenes_random_get(self):
        """Test case for scenes_random_get

        Get a random scene
        """
        response = self.client.open(
            '/scenes/random',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_scenes_search_get(self):
        """Test case for scenes_search_get

        Search for a whole scene (all quotes) by scene's number/name and movie
        """
        query_string = [('movie', 'movie_example'),
                        ('scene_number', 56),
                        ('scene_name', 'scene_name_example'),
                        ('scene_number_or_name', SceneNumberOrName())]
        response = self.client.open(
            '/scenes/search',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
