import hashlib
from utils.model import BaseModel
from random import randint


class UserModel(BaseModel):
    def __init__(self):
        super().__init__() # ABC ABC ABC
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
            chess_wins_easy INTEGER DEFAULT 0,
            chess_wins_medium INTEGER DEFAULT 0,
            chess_wins_hard INTEGER DEFAULT 0,
            chess_defeats_easy INTEGER DEFAULT 0,
            chess_defeats_medium INTEGER DEFAULT 0,
            chess_defeats_hard INTEGER DEFAULT 0,
            checkers_wins_easy INTEGER DEFAULT 0,
            checkers_wins_medium INTEGER DEFAULT 0,
            checkers_wins_hard INTEGER DEFAULT 0,
            checkers_defeats_easy INTEGER DEFAULT 0,
            checkers_defeats_medium INTEGER DEFAULT 0,
            checkers_defeats_hard INTEGER DEFAULT 0,
            logged_in INTEGER DEFAULT 0
        );
        """
        self.execute_query(create_table_query)

#        for name in ['Alex', 'Tom', 'Erka', 'Rober', 'Enruqie', 'NhatHuy']:
#            u = UserModel()
#            password = f'abc{randint(100, 10000)}'
#            username = f'{name.lower()}{randint(100, 20000)}'
#            u.add_user(username, password)
#            u.login(username, password)
#            for i in range(randint(1, 20)):
#                u.increment_chess_wins_easy()

    def get_fields(self) -> list:
        return ['id', 'username', 'password', 'games_played', 'best_result_checkers', 'best_result_chess',
                'chess_wins_easy', 'chess_wins_medium', 'chess_wins_hard', 'chess_defeats_easy',
                'chess_defeats_medium', 'chess_defeats_hard', 'checkers_wins_easy', 'checkers_wins_medium',
                'checkers_wins_hard', 'checkers_defeats_easy', 'checkers_defeats_medium', 'checkers_defeats_hard',
                'logged_in']

    def add_user(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        add_user_query = "INSERT INTO users (username, password, games_played, best_result_checkers, best_result_chess, chess_wins_easy, chess_wins_medium, chess_wins_hard, chess_defeats_easy, chess_defeats_medium, chess_defeats_hard, checkers_wins_easy, checkers_wins_medium, checkers_wins_hard, checkers_defeats_easy, checkers_defeats_medium, checkers_defeats_hard, logged_in) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
        self.execute_query(add_user_query, (username, hashed_password, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

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

    def get_data(self):
        get_data_query = "SELECT * FROM users;"
        return self.fetch_query(get_data_query)

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
    def chess_wins_easy(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][6]
        return None

    @chess_wins_easy.setter
    def chess_wins_easy(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET chess_wins_easy = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_chess_wins_easy(self):
        self.chess_wins_easy += 1

    @property
    def chess_wins_medium(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][7]
        return None

    @chess_wins_medium.setter
    def chess_wins_medium(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET chess_wins_medium = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_chess_wins_medium(self):
        self.chess_wins_medium += 1

    @property
    def chess_wins_hard(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][8]
        return None

    @chess_wins_hard.setter
    def chess_wins_hard(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET chess_wins_hard = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_chess_wins_hard(self):
        self.chess_wins_hard += 1

    @property
    def chess_defeats_easy(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][9]
        return None

    @chess_defeats_easy.setter
    def chess_defeats_easy(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET chess_defeats_easy = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_chess_defeats_easy(self):
        self.chess_defeats_easy += 1

    @property
    def chess_defeats_medium(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][10]
        return None

    @chess_defeats_medium.setter
    def chess_defeats_medium(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET chess_defeats_medium = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_chess_defeats_medium(self):
        self.chess_defeats_medium += 1

    @property
    def chess_defeats_hard(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][11]
        return None

    @chess_defeats_hard.setter
    def chess_defeats_hard(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET chess_defeats_hard = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_chess_defeats_hard(self):
        self.chess_defeats_hard += 1

    @property
    def checkers_wins_easy(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][12]
        return None

    @checkers_wins_easy.setter
    def checkers_wins_easy(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET checkers_wins_easy = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_checkers_wins_easy(self):
        self.checkers_wins_easy += 1

    @property
    def checkers_wins_medium(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][13]
        return None

    @checkers_wins_medium.setter
    def checkers_wins_medium(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET checkers_wins_medium = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_checkers_wins_medium(self):
        self.checkers_wins_medium += 1

    @property
    def checkers_wins_hard(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][14]
        return None

    @checkers_wins_hard.setter
    def checkers_wins_hard(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET checkers_wins_hard = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_checkers_wins_hard(self):
        self.checkers_wins_hard += 1

    @property
    def checkers_defeats_easy(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][15]
        return None

    @checkers_defeats_easy.setter
    def checkers_defeats_easy(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET checkers_defeats_easy = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_checkers_defeats_easy(self):
        self.checkers_defeats_easy += 1

    @property
    def checkers_defeats_medium(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][16]
        return None

    @checkers_defeats_medium.setter
    def checkers_defeats_medium(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET checkers_defeats_medium = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_checkers_defeats_medium(self):
        self.checkers_defeats_medium += 1

    @property
    def checkers_defeats_hard(self):
        if self.logged_in and self._username:
            user_data = self.get_user(self._username)
            return user_data[0][17]
        return None

    @checkers_defeats_hard.setter
    def checkers_defeats_hard(self, value: int):
        if self.logged_in and self._username:
            update_query = "UPDATE users SET checkers_defeats_hard = ? WHERE username = ?;"
            self.execute_query(update_query, (value, self._username))

    def increment_checkers_defeats_hard(self):
        self.checkers_defeats_hard += 1

    @property
    def logged_in(self):
        if self._username:
            user_data = self.get_user(self._username)
            return user_data[0][18] == 1
        return False

    @logged_in.setter
    def logged_in(self, value: bool):
        if self._username:
            if value:
                update_all_query = "UPDATE users SET logged_in = 0 WHERE logged_in = 1;"
                self.execute_query(update_all_query)

            update_query = "UPDATE users SET logged_in = ? WHERE username = ?;"
            self.execute_query(update_query, (1 if value else 0, self._username))
