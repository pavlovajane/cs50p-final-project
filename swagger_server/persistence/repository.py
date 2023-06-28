import sqlite3
import typing as t
from injector import inject

class DbRepository:

    @inject
    def __init__(self, db: sqlite3.Connection) -> None:
        self.db = db

    def find_all(self, query: str, params: tuple = tuple()) -> t.List[t.Any]:
        return self.db.execute(query, params).fetchall()
    
    def execute_and_commit(self, query: str, params: t.Any) -> None:
        self.db.execute(query, params)
        self.db.commit()