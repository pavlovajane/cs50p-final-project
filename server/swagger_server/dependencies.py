from functools import lru_cache
import sqlite3
from swagger_server.services.quotes_service import QuotesService
from swagger_server.persistence.repository import DbRepository
from swagger_server.services.movies_service import MoviesService
from swagger_server.services.user_service import UserService
import argparse


def configure_database(binder):
    binder.bind(
        sqlite3.Connection,
        to=sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)
    )

@lru_cache
def get_repository(db: sqlite3.Connection) -> 'DbRepository':
    return DbRepository(db=db)

@lru_cache
def get_movie_service(repo: DbRepository) -> 'MoviesService':
    return MoviesService(repo=repo)

@lru_cache
def get_quotes_service(repo: DbRepository) -> 'QuotesService':
    return QuotesService(repo=repo)

@lru_cache
def get_user_service(repo: DbRepository) -> 'UserService':
    return UserService(repo=repo)

@lru_cache
def get_db(db:str) -> sqlite3.Connection:
    return sqlite3.connect(f"./swagger_server/persistence/{db}", check_same_thread=False)
    # return sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)

class DependencyResolver:
    def __init__(self, db: str):
        self.db = db

    def resolve(self, clazz: any) -> any:
        if clazz == sqlite3.Connection:
            return get_db(self.db)
        if clazz == UserService:
            return get_user_service(self.resolve(DbRepository))
        if clazz == MoviesService:
            return get_movie_service(self.resolve(DbRepository))
        if clazz == DbRepository:
            return get_repository(self.resolve(sqlite3.Connection))
        if clazz == QuotesService:
            return get_quotes_service(self.resolve(DbRepository))
        raise ValueError(f"Can't resolve given class {clazz}")


parser = argparse.ArgumentParser(prog="dependencies.py", description="Resolve dependencies")
parser.add_argument("-db", default="holy_scripts.db", help="Path to a sqlite database db file")
args = parser.parse_args()


dependency_resolver = DependencyResolver(args.db)