from typing import List
from injector import inject
from werkzeug.security import check_password_hash
from swagger_server.services.user_service import UserService
from swagger_server.persistence.repository import DbRepository
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_basicAuth(user_service: UserService, username, password, required_scopes):

    if check_password_hash(user_service.get_password_hash(username), password):
        return {"sub": username}
    return None


