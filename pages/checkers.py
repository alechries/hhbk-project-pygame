import typing

from utils.board import BaseBoardPage
from utils.cell import Cell
from pygame.event import Event
import pygame
from utils.piece import Piece
from utils.types import GameType, SpawnType, TeamType, BoardCellType


class CheckersBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__(GameType.CHESS_GAME)
        self.page_name = 'checkers'

    def get_moves(self, selected_piece: Piece) -> typing.List[Cell]:

        direction = self.current_step_direction
        return self.get_valid_moves_inside(
            [
                (selected_piece.board_place_column - 1, selected_piece.board_place_row + direction),
                (selected_piece.board_place_column + 1, selected_piece.board_place_row + direction),
            ]
        )

    def handle_event(self, event: Event):

        super().handle_event(event)
