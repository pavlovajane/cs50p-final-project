
from injector import inject
from swagger_server.models.user import User
from swagger_server.models.users_body import UsersBody
from swagger_server.persistence.repository import DbRepository

from werkzeug.security import check_password_hash, generate_password_hash

class UserService:

    @inject
    def __init__(self, repo: DbRepository) -> None:
        self.repo = repo

    def create_user(self, user: UsersBody) -> User:
        username = user.username
        hash = generate_password_hash(user.password)
        q = """
            INSERT INTO users (username, hash) 
                       VALUES (?, ?)
        """
        self.repo.execute_and_commit(q, (username, hash,))
        rows = self.repo.find_all("SELECT id FROM users WHERE username = ?", (username,))
        id, = rows[0]
        return User(id=id, username=username)
