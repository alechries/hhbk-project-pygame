import json
import os


class Config:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)

    def __init__(self, config_file='config.json'):
        self.config_file = config_file

        self.images_dir: str = 'assets/images/'
        self.sound_dir: str = 'assets/sounds/'
        self.board_size_percent: int = 90

        self.__db_name: str = 'database.sqlite3'
        self.__start_page: str = 'auth'
        self.__app_name: str = 'Project Pygame'
        self.__sound_volume: float = 1.0  # 0.0 to 1.0
        self.__game_difficulty_level: int = 3
        self.__screen_width: int = 800
        self.__screen_height: int = 600
        self.__frame_rate: int = 60

        if not os.path.exists(self.config_file):
            self.save_config()
        else:
            self.load_config()

    def save_config(self):
        config_data = {
            "db_name": self.__db_name,
            "app_name": self.__app_name,
            "start_page": self.__start_page,
            "sound_volume": self.__sound_volume,
            "game_difficulty_level": self.__game_difficulty_level,
            "screen_width": self.__screen_width,
            "screen_height": self.__screen_height,
            "frame_rate": self.__frame_rate,
        }
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=4)

    def load_config(self):
        with open(self.config_file, 'r') as f:
            config_data = json.load(f)
            self.__db_name = config_data.get("db_name", self.__db_name)
            self.__app_name = config_data.get("app_name", self.__app_name)
            self.__start_page = config_data.get("start_page", self.__app_name)
            self.__sound_volume = config_data.get("sound_volume", self.__sound_volume)
            self.__game_difficulty_level = config_data.get("game_difficulty_level", self.__game_difficulty_level)
            self.__screen_width = config_data.get("screen_width", self.__screen_width)
            self.__screen_height = config_data.get("screen_height", self.__screen_height)
            self.__frame_rate = config_data.get("frame_rate", self.__frame_rate)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, f'_{self.__class__.__name__}__{key}'):
                setattr(self, f'_{self.__class__.__name__}__{key}', value)
        self.save_config()

    @property
    def app_name(self) -> str:
        return self.__app_name

    @app_name.setter
    def app_name(self, value: str):
        self.__app_name = value
        self.save_config()

    @property
    def db_name(self) -> str:
        return self.__db_name

    @db_name.setter
    def db_name(self, value: str):
        self.__db_name = value
        self.save_config()

    @property
    def start_page(self) -> str:
        return self.__start_page

    @start_page.setter
    def start_page(self, value: str):
        self.__start_page = value
        self.save_config()

    @property
    def sound_volume(self) -> float:
        return self.__sound_volume

    @sound_volume.setter
    def sound_volume(self, value: float):
        self.__sound_volume = value
        self.save_config()

    @property
    def game_difficulty_level(self) -> int:
        return self.__game_difficulty_level

    @game_difficulty_level.setter
    def game_difficulty_level(self, value: int):
        self.__game_difficulty_level = value
        self.save_config()

    @property
    def screen_width(self) -> int:
        return self.__screen_width

    @screen_width.setter
    def screen_width(self, value: int):
        self.__screen_width = value
        self.save_config()

    @property
    def screen_height(self) -> int:
        return self.__screen_height

    @screen_height.setter
    def screen_height(self, value: int):
        self.__screen_height = value
        self.save_config()

    @property
    def frame_rate(self) -> int:
        return self.__frame_rate

    @frame_rate.setter
    def frame_rate(self, value: int):
        self.__frame_rate = value
        self.save_config()
