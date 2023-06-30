from injector import inject
from swagger_server.models.tops import Tops
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
    
    def get_user_tops(self, repo: DbRepository) -> Tops:
        pass

    def get_password_hash(self, username: str) -> str:

        query = """
                SELECT 
                hash 
                FROM users WHERE username = ?"""
        rows = self.repo.find_all(query, (username,))
        if len(rows) == 0:
            return None
        hash = rows[0]
        return hash
        
