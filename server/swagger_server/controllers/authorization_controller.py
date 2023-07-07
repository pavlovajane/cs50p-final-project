from typing import List
from injector import inject
from werkzeug.security import check_password_hash
from swagger_server.services.user_service import UserService
from swagger_server.dependencies import dependency_resolver
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_basicAuth(username, password, required_scopes):
    user_service: UserService = dependency_resolver.resolve(UserService)
    
    if check_password_hash(user_service.get_password_hash(username), password):
        return {"sub": username}
    return None


