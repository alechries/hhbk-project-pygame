from enum import IntEnum


class TeamType(IntEnum):

    WHITE_TEAM = 1
    BLACK_TEAM = 2


class GameType(IntEnum):

    CHESS_GAME = 1
    CHECKERS_GAME = 2
    TICTACTOE_GAME = 3


class LevelType(IntEnum):

    EASY = 1
    MEDIUM = 2
    HARD = 3


class SpawnType(IntEnum):

    TOP_SPAWN = 1
    BOTTOM_SPAWN = 2

