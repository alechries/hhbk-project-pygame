import hashlib
from utils.model import BaseModel


class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self._username = None

    def initialize_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            games_played INTEGER DEFAULT 0,
            best_result_checkers INTEGER DEFAULT 0,
            best_result_chess INTEGER DEFAULT 0,
            logged_in INTEGER DEFAULT 0
        );
        """
        self.execute_query(create_table_query)

    def get_fields(self) -> list:
        return ['id', 'username', 'password', 'games_played', 'best_result_checkers', 'best_result_chess', 'logged_in']

    def add_user(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        add_user_query = "INSERT INTO users (username, password, games_played, best_result_checkers, best_result_chess, logged_in) VALUES (?, ?, ?, ?, ?, ?);"
        self.execute_query(add_user_query, (username, hashed_password, 0, 0, 0, 0))

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> bool:
        if self.check_password(username, password):
            self._username = username
            self.logged_in = True
            return True
        return False

    def get_user(self, username: str):
        get_user_query = "SELECT * FROM users WHERE username = ?;"
        return self.fetch_query(get_user_query, (username,))

    def update_games_played(self, username: str, games_played: int):
        update_query = "UPDATE users SET games_played = ? WHERE username = ?;"
        self.execute_query(update_query, (games_played, username))

    def check_password(self, username: str, password: str) -> bool:
        user_data = self.get_user(username)
        if user_data:
            stored_hashed_password = user_data[0][2]
            return self.hash_password(password) == stored_hashed_password
        return False

    @property
    def games_played(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][3]
        return None

    @games_played.setter
    def games_played(self, value: int):
        if self.logged_in and self._username:
            self.update_games_played(self._username, value)

    @property
    def best_result_checkers(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][4]
        return None

    @best_result_checkers.setter
    def best_result_checkers(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET best_result_checkers = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    @property
    def best_result_chess(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][5]
        return None

    @best_result_chess.setter
    def best_result_chess(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET best_result_chess = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    @property
    def logged_in(self):
        if self._username:
            user_data = self.get_user(self._username)
            return user_data[0][6] == 1
        return False

    @logged_in.setter
    def logged_in(self, value: bool):
        if self._username:
            if value:
                update_all_query = "UPDATE users SET logged_in = 0 WHERE logged_in = 1;"
                self.execute_query(update_all_query)

            update_query = "UPDATE users SET logged_in = ? WHERE username = ?;"
            self.execute_query(update_query, (1 if value else 0, self._username))
