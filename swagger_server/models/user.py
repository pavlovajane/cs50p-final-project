# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class User(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, username: str=None, password: str=None):  # noqa: E501
        """User - a model defined in Swagger

        :param id: The id of this User.  # noqa: E501
        :type id: int
        :param username: The username of this User.  # noqa: E501
        :type username: str
        :param password: The password of this User.  # noqa: E501
        :type password: str
        """
        self.swagger_types = {
            'id': int,
            'username': str,
            'password': str
        }

        self.attribute_map = {
            'id': 'id',
            'username': 'username',
            'password': 'password'
        }
        self._id = id
        self._username = username
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'User':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The User of this User.  # noqa: E501
        :rtype: User
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this User.

        The user ID  # noqa: E501

        :return: The id of this User.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this User.

        The user ID  # noqa: E501

        :param id: The id of this User.
        :type id: int
        """

        self._id = id

    @property
    def username(self) -> str:
        """Gets the username of this User.

        The user name  # noqa: E501

        :return: The username of this User.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this User.

        The user name  # noqa: E501

        :param username: The username of this User.
        :type username: str
        """

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this User.

        Hash for the user password  # noqa: E501

        :return: The password of this User.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this User.

        Hash for the user password  # noqa: E501

        :param password: The password of this User.
        :type password: str
        """

        self._password = password