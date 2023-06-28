
import sqlite3


def configure_database(binder):
    binder.bind(
        sqlite3.Connection,
        to=sqlite3.connect("./swagger_server/persistence/holy_scripts.db", check_same_thread=False)
    )
