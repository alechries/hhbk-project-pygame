import sqlite3
from sqlite3 import Connection
from utils.config import Config


class BaseModel:
    def __init__(self):
        self.config = Config()
        self.db_name = self.config.db_name
        self.conn = self.connect()

    def connect(self) -> Connection:
        return sqlite3.connect(self.db_name)

    def execute_query(self, query: str, params: tuple = ()):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()

    def fetch_query(self, query: str, params: tuple = ()) -> list:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def initialize_table(self):
        raise NotImplementedError()

    def get_fields(self) -> list:
        raise NotImplementedError()
