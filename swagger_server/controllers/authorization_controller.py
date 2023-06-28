from typing import List
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""
def check_basicAuth(username, password, required_scopes):
    if username == "test" and password == "test":
        return {'test_key': 'test_value'}
    return None


