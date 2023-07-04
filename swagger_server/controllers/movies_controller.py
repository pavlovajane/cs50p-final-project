
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.movie import Movie  # noqa: E501
from swagger_server import util
from swagger_server.services.movies_service import MoviesService
from swagger_server.dependencies import dependency_resolver


def movies_get():  # noqa: E501
    """Get a list of available to get quotes movies

     # noqa: E501


    :rtype: Movie
    """
    movies_service: MoviesService = dependency_resolver.resolve(MoviesService)
    return movies_service.find_all_movies()
