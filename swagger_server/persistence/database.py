import sqlite3
from swagger_server.persistence.repository import DbRepository
from swagger_server.services.movies_service import MoviesService

from swagger_server.services.user_service import UserService

def configure_database(binder):
    binder.bind(
        sqlite3.Connection,
        to=sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)
    )

def get_repository(db: sqlite3.Connection) -> 'DbRepository':
    return DbRepository(db=db)

def get_movie_service(repo: DbRepository) -> 'MoviesService':
    return MoviesService(repo=repo)

def get_user_service(repo: DbRepository) -> 'UserService':
    return UserService(repo=repo)

def get_db() -> sqlite3.Connection:
    return sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)
    

def get_dependencies() -> dict:
    db = get_db()
    repo = get_repository(db)
    return {
        "movies_service": get_movie_service(repo),
        "user_service": get_user_service(repo),
    }