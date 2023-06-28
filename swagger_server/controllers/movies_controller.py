
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.movie import Movie  # noqa: E501
from swagger_server import util
from swagger_server.services.movies_service import MoviesService


def movies_get(service: MoviesService):  # noqa: E501
    """Get a list of available to get quotes movies

     # noqa: E501


    :rtype: Movie
    """
    return service.find_all_movies()
