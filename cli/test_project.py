from project import check_choice_validity, send_get, show_exit
import pytest
import requests
import subprocess
import time
import os
import sys
from io import StringIO

# Get the path to the server module
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'server'))

# Define a fixture to start and stop the server
@pytest.fixture(scope='session', autouse=True)
def server():
    # Start the server as a subprocess
    server_process = subprocess.Popen(['python', '-m', 'swagger_server', '-db', '/holy_scripts_tests.db'], cwd=module_path)

    # Wait for the server to start
    time.sleep(2)

    # Yield control to the tests
    yield

    # Stop the server
    server_process.terminate()
    server_process.wait(timeout=2)

def test_server_running(server):
    response = requests.get("http://localhost:8080/health")
    assert response.status_code == 200

def test_send_get():
    assert send_get("http://localhost:8080/movies") == requests.get("http://localhost:8080//movies").json()

def test_function_check_choice_validity():
    assert check_choice_validity("1", []) == False
    assert check_choice_validity("1", None) == False
    assert check_choice_validity(None, [
        "1 - Repeat the last action",
        "2 - Return to the main menu",
        "3 - Exit the program"
        ]) == False
    assert check_choice_validity(None, None) == False
    assert check_choice_validity("1", [
        "1 - Repeat the last action",
        "2 - Return to the main menu",
        "3 - Exit the program"
        ]) == True
    assert check_choice_validity("4", [
        "1 - Repeat the last action",
        "2 - Return to the main menu",
        "3 - Exit the program"
        ]) == False


def test_should_generate_start_menu():
    cli_process = subprocess.Popen(['python', 'project.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = cli_process.communicate(input=b'1\n7\n')[0]
    print(out.decode().split("===================================")[2])


def test_show_exit():
    oldstdout = sys.stdout
    out = StringIO()
    sys.stdout = out
    show_exit()
    sys.stdout = oldstdout
    output = out.getvalue().strip()
    assert output == """
===================================
Program closed by user
===================================
""".strip()