from typing import List
from werkzeug.security import check_password_hash
from swagger_server.services.user_service import get_password_hash
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_basicAuth(username, password, required_scopes):
    if check_password_hash(get_password_hash(username), password):
        return {"sub": username}
    return None


