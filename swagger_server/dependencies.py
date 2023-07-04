from functools import lru_cache
import sqlite3
from swagger_server.persistence.repository import DbRepository
from swagger_server.services.movies_service import MoviesService

from swagger_server.services.user_service import UserService

def configure_database(binder):
    binder.bind(
        sqlite3.Connection,
        to=sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)
    )

@lru_cache
def get_repository(db: sqlite3.Connection) -> 'DbRepository':
    print("get_repository")
    return DbRepository(db=db)

@lru_cache
def get_movie_service(repo: DbRepository) -> 'MoviesService':
    print("get_movie_service")
    return MoviesService(repo=repo)

@lru_cache
def get_user_service(repo: DbRepository) -> 'UserService':
    print("get_user_service")
    return UserService(repo=repo)

@lru_cache
def get_db() -> sqlite3.Connection:
    print("get_db")
    return sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)
    

class DependencyResolver:
    def resolve(self, clazz: any) -> any:
        if clazz == sqlite3.Connection:
            return get_db()
        if clazz == UserService:
            return get_user_service(self.resolve(DbRepository))
        if clazz == MoviesService:
            return get_movie_service(self.resolve(DbRepository))
        if clazz == DbRepository:
            return get_repository(self.resolve(sqlite3.Connection))
        raise ValueError(f"Can't resolve given class {clazz}")

dependency_resolver = DependencyResolver()