import typing
from enum import IntEnum

import pygame


class TeamType(IntEnum):
    UNKNOWN_TEAM = 0
    WHITE_TEAM = 1
    BLACK_TEAM = 2


class GameType(IntEnum):

    UNKNOWN = 0
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


class BoardCellType(IntEnum):

    EMPTY_CELL = 0
    TEAM_CELL = 1
    ENEMY_CELL = 2
    ALL_CELL = 0


class BoardMoveType(IntEnum):

    NORMAL_MOVE = 0
    COMPLICATING_MOVE = 1
    WINNING_MOVE = 2


class BoardMove:

    def __init__(self, coord: typing.Tuple[int, int], move_type: BoardMoveType):
        self.coord = coord
        self.move_type = move_type


class EventType(IntEnum):

    ENEMY_MOVE_EVENT = pygame.USEREVENT + 1

class BoardPlacement:

    def __init__(self, board: typing.List[typing.List[BoardCellType]], moves: typing.List[BoardMove], game_type: GameType, level_type: LevelType, spawn_type: SpawnType):
        self.board = board
        self.moves = moves
        self.game_type = game_type
        self.level_type = level_type
        self.spawn_type = spawn_type
