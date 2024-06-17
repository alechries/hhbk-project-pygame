
class Config:

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self):

        self.images_dir: str = 'assets/images/'
        self.sound_dir: str = 'assets/sounds/'
        self.__db_name: str = 'game_database.sqlite3'
        self.__app_name: str = 'My Game'
        self.__sound_volume: float = 1  # 0.0 to 1.0
        self.__game_difficulty_level: int = 3
        self.__screen_width: int = 800
        self.__screen_height: int = 600
        self.__frame_rate: int = 60

    @property
    def app_name(self) -> str:
        return self.__app_name

    @property
    def db_name(self) -> str:
        return self.__db_name

    @property
    def sound_volume(self) -> float:
        return self.__sound_volume

    @property
    def game_difficulty_level(self) -> int:
        return self.__game_difficulty_level

    @property
    def screen_width(self) -> int:
        return self.__screen_width

    @property
    def screen_height(self) -> int:
        return self.__screen_height

    @property
    def frame_rate(self) -> int:
        return self.__frame_rate

