# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.id_tops_body import IdTopsBody  # noqa: E501
from swagger_server.models.tops import Tops  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.users_body import UsersBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUsersController(BaseTestCase):
    """UsersController integration test stubs"""

    def test_users_id_tops_get(self):
        """Test case for users_id_tops_get

        Get user's top quotes
        """
        response = self.client.open(
            '/users/{id}/tops'.format(id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_id_tops_post(self):
        """Test case for users_id_tops_post

        Add a quote to user's top quotes
        """
        body = IdTopsBody()
        response = self.client.open(
            '/users/{id}/tops'.format(id=56),
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_post(self):
        """Test case for users_post

        Create a new user
        """
        body = UsersBody()
        response = self.client.open(
            '/users',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
