import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.scene_number_or_name import SceneNumberOrName  # noqa: E501
from swagger_server.models.scene_with_quotes import SceneWithQuotes  # noqa: E501
from swagger_server import util


def scenes_random_get():  # noqa: E501
    """Get a random scene

    Return all quotes from a random scene, sorted # noqa: E501


    :rtype: SceneWithQuotes
    """
    return 'Some magic in the next version!'


def scenes_search_get(movie, scene_number=None, scene_name=None, scene_number_or_name=None):  # noqa: E501
    """Search for a whole scene (all quotes) by scene&#x27;s number/name and movie

     # noqa: E501

    :param movie: Movie name to search a scene in (or part of the name)
    :type movie: str
    :param scene_number: Scene number may be given
    :type scene_number: int
    :param scene_name: Name or part of the a scene name may be given
    :type scene_name: str
    :param scene_number_or_name: Either number or name of the scene should be given
    :type scene_number_or_name: dict | bytes

    :rtype: SceneWithQuotes
    """
    if connexion.request.is_json:
        scene_number_or_name = SceneNumberOrName.from_dict(connexion.request.get_json())  # noqa: E501
    return 'Some magic in the next version!'
