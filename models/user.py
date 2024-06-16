import hashlib
from utils.model import BaseModel


class UserModel(BaseModel):
    def __init__(self):
        super().__init__()
        self.initialize_table()

    def initialize_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            games_played INTEGER DEFAULT 0
        );
        """
        self.execute_query(create_table_query)

    def get_fields(self) -> list:
        return ['id', 'username', 'password', 'games_played']

    def add_user(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        add_user_query = "INSERT INTO users (username, password, games_played) VALUES (?, ?, ?);"
        self.execute_query(add_user_query, (username, hashed_password, 0))

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

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
