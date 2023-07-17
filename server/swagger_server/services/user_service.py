from injector import inject
from swagger_server.models.movie import Movie
from swagger_server.models.quote import Quote
from swagger_server.models.scene import Scene
from swagger_server.models.tops import Tops
from swagger_server.models.tops_inner import TopsInner
from swagger_server.models.user import User
from swagger_server.models.users_body import UsersBody
from swagger_server.persistence.repository import DbRepository

from werkzeug.security import generate_password_hash

class UserService:

    @inject
    def __init__(self, repo: DbRepository) -> None:
        self.repo = repo

    def get_user_id(self, username: str) -> int:
        # get user id from current username
        rows = self.repo.find_all("SELECT id FROM users WHERE username = ?", (username,))
        if len(rows) == 0:
            return None
        id, = rows[0]
        return id

    def create_user(self, user: UsersBody) -> User:
        username = user.username
        hash = generate_password_hash(user.password)
        query = """
            INSERT INTO users (username, hash)
                       VALUES (?, ?)
        """
        self.repo.execute_and_commit(query, (username, hash,))
        rows = self.repo.find_all("SELECT id FROM users WHERE username = ?", (username,))
        if len(rows) == 0:
            return None
        id, = rows[0]
        return User(id=id)

    def put_user_tops(self, user_id: int, quote_id: int) -> Tops:
        """Put a qupte into user's top quotes
        :param user_id: User's int ID to get user's tops quotes
        :param quote_id: Quote int ID to put into top list
        :return: Tops object (an array of quotes)
        :rtype: Tops model
        """
        query = """
            INSERT INTO tops (user_id, quote_id)
                       VALUES (?, ?)
        """
        self.repo.execute_and_commit(query, (user_id, quote_id,))
        # TODO This better be re-worked to return not a list but just success - okay for learning purposes for now
        return self.get_user_tops(user_id)


    def get_user_tops(self, user_id: int) -> Tops:
        """Get user's top quotes

        :param user_id: User's int ID to get user's tops quotes

        :return: Tops object (an array of quotes)
        :rtype: Tops model
        """
        query = """
            SELECT
            q.id, q.movie, q.scene_number, q.scene_name, q.type, q.character, q.text
            FROM tops as t
            LEFT JOIN scripts as q
            ON q.id = t.quote_id
            WHERE t.user_id = ?
        """
        rows = self.repo.find_all(query, (user_id,))
        if len(rows) == 0:
            return None

        tops = []
        for r in rows:
            top = TopsInner(quote=Quote(id = r[0],
                                        movie=Movie(name=r[1]),
                                        scene=Scene(number=r[2],name=r[3]),
                                        type=r[4],
                                        character=r[5],
                                        text=r[6]))
            tops.append(top)
        return tops

    def get_password_hash(self, username: str) -> str:
        """Get user's hash from a database

        :param username: str for a username

        :return: user's password hash as str
        :rtype: str
        """
        query = """
                SELECT
                hash
                FROM users WHERE username = ?"""
        rows = self.repo.find_all(query, (username,))
        if len(rows) == 0:
            return None
        hash = rows[0]
        return hash[0]

