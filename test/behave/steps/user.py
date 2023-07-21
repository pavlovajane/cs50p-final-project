from behave import *
import requests
from utils import get_last_user_id
import random
import pdb

@given("I set Holy Grail API url")
def step_impl(context):
    context.holy_url = "http://localhost:8080"

@given("Holy Grail API url health responds with '200'")
def step_impl(context):
    response = requests.get(f"{context.holy_url}/health")
    assert response.status_code == 200

@when("user send create new user POST '/users'")
def step_impl(context):
    data = context.table.rows[0]
    payload = {
        "username": f"user{random.randint(0, 1000000)}",
        "password": data["password"]
    }
    context.last_id = get_last_user_id(context.cursordb)
    context.response = requests.post(url=f"{context.holy_url}/users", json=payload)

@then("'{status_code}' response is returned")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)

@then("the following details are returned")
def step_impl(context):
    if context.response.status_code == 200:
        data = context.response.json()
        user_id = data["id"]
        
        assert (int(context.last_id)+1) == int(user_id)
    else:
        assert False