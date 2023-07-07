import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.id_tops_body import IdTopsBody  # noqa: E501
from swagger_server.models.tops import Tops  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.users_body import UsersBody  # noqa: E501
from swagger_server import util
from swagger_server.services.user_service import UserService
from werkzeug.exceptions import BadRequest
from swagger_server.dependencies import dependency_resolver
from flask import request


def users_id_tops_get(id=None, **kwargs):  # noqa: E501
    """Get user&#x27;s top quotes sorted by quote&#x27;s text

     # noqa: E501

    :param id: User ID
    :type id: int

    :rtype: Tops
    """
    user_service: UserService = dependency_resolver.resolve(UserService)
    id = request.view_args.get('id')
    return user_service.get_user_tops(id)


def users_id_tops_post(body, id):  # noqa: E501
    """Add a quote to user&#x27;s top quotes

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param id: User id
    :type id: int

    :rtype: Tops
    """
    if connexion.request.is_json:
        body = IdTopsBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def users_post(body, user_service: UserService):  # noqa: E501
    """Create a new user

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: User
    """
    if connexion.request.is_json:
        body = UsersBody.from_dict(connexion.request.get_json())  # noqa: E501
        return user_service.create_user(body)
    return BadRequest("Should be JSON")
