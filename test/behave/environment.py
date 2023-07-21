import subprocess
import time
import os
from behave import fixture, use_fixture
import sqlite3

@fixture(name="fixture.server")
def server(context, *args, **kwargs):

    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'server'))
    server_process = subprocess.Popen(['python', '-m', 'swagger_server', '-db', 'holy_scripts_tests.db'], cwd=module_path)

    time.sleep(2)

    yield

    server_process.terminate()
    server_process.wait(timeout=2)

@fixture(name="fixture.database")
def database(context, *args, **kwargs):

    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'server/swagger_server/persistence'))
    database = sqlite3.connect(f"{db_path}/holy_scripts_tests.db", check_same_thread=False)

    context.cursordb = database.cursor()
    context.db = database

    yield

    if database is not None:
        database.close()

def before_feature(context, feature):
    use_fixture(server, context)
    use_fixture(database, context)