import typing

from utils.board import BaseBoardPage
from utils.cell import Cell
from pygame.event import Event
from random import choice
import pygame
from utils.piece import Piece
from utils.types import GameType, LevelType, TeamType


class CheckersBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__(GameType.CHECKERS_GAME)
        self.page_name = 'checkers'

    def get_moves(self, piece_column: int, piece_row: int, team_type: TeamType,
                  current_map: typing.List[typing.List[Piece]], only_with_destroyed_pieces=False) -> \
            typing.List[Cell]:

        if team_type == TeamType.WHITE_TEAM:
            direction = -1
            enemy_team_type = TeamType.BLACK_TEAM
        elif team_type == TeamType.BLACK_TEAM:
            direction = 1
            enemy_team_type = TeamType.WHITE_TEAM
        else:
            return []

        piece: Piece = current_map[piece_row][piece_column]
        if piece is None:
            return []

        moves: typing.List[Cell] = []

        if not only_with_destroyed_pieces:
            for move_column, move_row in [
                (piece_column - 1, piece_row + direction),
                (piece_column + 1, piece_row + direction),
            ]:
                if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_column >= self.num_blocks_vertical:
                    continue

                piece_on_move_cell: Piece = current_map[move_row][move_column]

                if piece_on_move_cell is not None:
                    continue
                move = Cell(
                    move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                    piece=piece, destroy_figures=[])
                moves.append(move)

        for move_column, move_row, destroy_column, destroy_row in [
            (piece_column - 2, piece_row + 2, piece_column - 1, piece_row + 1),
            (piece_column + 2, piece_row + 2, piece_column + 1, piece_row + 1),
            (piece_column - 2, piece_row - 2, piece_column - 1, piece_row - 1),
            (piece_column + 2, piece_row - 2, piece_column + 1, piece_row - 1),
        ]:
            if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_row >= self.num_blocks_vertical or destroy_column < 0 or destroy_column >= self.num_blocks_horizontal or destroy_row < 0 or destroy_row >= self.num_blocks_vertical:
                continue

            piece_on_move_cell: Piece = current_map[move_row][move_column]
            destroy_piece = current_map[destroy_row][destroy_column]

            if piece_on_move_cell is not None or destroy_piece is None:
                continue
            print(destroy_piece.team_type)
            if destroy_piece.team_type != enemy_team_type:
                continue

            move = Cell(
                move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                piece=piece, destroy_figures=[destroy_piece, ])

            moves.append(move)
        return moves
