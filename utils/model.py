import sqlite3
from sqlite3 import Connection
from utils.config import Config
import os
import inspect
import importlib
from pathlib import Path


class BaseModel:
    def __init__(self):
        self.config = Config()
        self.db_name = self.config.db_name
        self.conn = self.connect()

    @staticmethod
    def initialize_tables():
        models_path = Path(__file__).parent.parent / "models"

        for file in models_path.glob("*.py"):
            if file.name == "__init__.py":
                continue

            module_name = f"models.{file.stem}"
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):

                if issubclass(obj, BaseModel) and obj is not BaseModel:
                    instance = obj()
                    instance.initialize_table()

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
