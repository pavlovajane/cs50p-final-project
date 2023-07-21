from swagger_server.services.movies_service import MoviesService # noqa: E501
from swagger_server.dependencies import dependency_resolver # noqa: E501


def movies_get():  # noqa: E501
    """Get a list of available to get quotes movies

     # noqa: E501


    :rtype: Movie
    """
    movies_service: MoviesService = dependency_resolver.resolve(MoviesService)

    return movies_service.find_all_movies()
