from sqlite3 import Cursor

def get_last_user_id(cursor: Cursor)->str:
    """
    Receive the last user id in the database by its cursor
    :param cursor: Cursor of sqlite3
    :return: Returns max user id as a string
    :rtype: str
    """
    query = "SELECT MAX(CAST(id AS INTEGER)) FROM users;"
    rows = cursor.execute(query)
    row = rows.fetchone()
    return row[0] if row is not None else ""