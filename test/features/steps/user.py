from behave import *
import subprocess
import time
import os

@fixture
def server():
    # Start the server as a subprocess
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'server'))
    server_process = subprocess.Popen(['python', '-m', 'swagger_server'], cwd=module_path)

    # Wait for the server to start
    time.sleep(2)

    # Yield control to the tests
    yield

    # Stop the server
    server_process.terminate()
    server_process.wait(timeout=2)

@given("I set Holy Grail API url")
def step_impl(context):
    pass

@given("Holy Grail API url health responds with '200'")
def step_impl(context):
    pass

@when("I send create user endpoint POST '{create_user_url}'")
def step_impl(context, create_user_url):
    pass

@when(u'new user name \'Hase02\'')
def step_impl(context):
    raise NotImplementedError(u'STEP: When new user name \'Hase02\'')


@when(u'new user password \'2\'')
def step_impl(context):
    raise NotImplementedError(u'STEP: When new user password \'2\'')


@then(u'\'200\' response is returned')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then \'200\' response is returned')


@then(u'the following details are returned')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the following details are returned')