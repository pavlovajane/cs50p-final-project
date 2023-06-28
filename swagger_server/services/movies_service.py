

from swagger_server.persistence.repository import DbRepository
from swagger_server.models.movie import Movie
from injector import inject

class MoviesService:

    @inject
    def __init__(self, repo: DbRepository) -> None:
        self.repo = repo

    def find_all_movies(self):
        movies = []
        results =  self.repo.find_all("SELECT distinct 0, movie FROM scripts")
        for r in results:
            id, name = r
            movie = Movie(id=id, name=name)
            movies.append(movie)
        return movies
