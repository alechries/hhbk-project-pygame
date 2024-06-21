import typing

from utils.board import BaseBoardPage
from utils.cell import Cell
from pygame.event import Event
from random import choice
import pygame
from utils.piece import Piece
from utils.types import GameType, LevelType


class ChessBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__(GameType.CHESS_GAME)
        self.page_name = 'chess'

    def get_moves(self, selected_piece: Piece) -> typing.List[Cell]:

        direction = self.current_step_direction
        return self.get_valid_moves_inside(
            [
                (selected_piece.board_place_column - 1, selected_piece.board_place_row + direction),
                (selected_piece.board_place_column + 1, selected_piece.board_place_row + direction),
            ]
        )

    def minmax_move(self, pieces_with_moves: typing.List[typing.Tuple[Piece, typing.List[Cell]]]) -> Cell:

        if self.config.game_difficulty_level == LevelType.EASY:
            self.selected_piece, moves = choice(pieces_with_moves)
            move = choice(moves)
            return move
        else:
            self.selected_piece, moves = choice(pieces_with_moves)
            move = choice(moves)
            return move
        # current_map_enemy = self.get_current_map_with_pieces(self.get_current_map_with_pieces(BoardCellType.ENEMY_CELL))
