

from swagger_server.persistence.repository import DbRepository
from swagger_server.models.movie import Movie
from injector import inject

class MoviesService:

    @inject
    def __init__(self, repo: DbRepository) -> None:
        self.repo = repo

    def find_all_movies(self):
        movies = []
        results =  self.repo.find_all("SELECT distinct movie FROM scripts")
        for r in results:
            name = r
            movie = Movie(name=name)
            movies.append(movie)
        return movies
