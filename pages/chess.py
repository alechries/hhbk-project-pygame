import copy
import typing
import math
from utils.board import BaseBoardPage
from utils.cell import Cell
from pygame.event import Event
from random import choice
import pygame
from utils.piece import Piece
from utils.types import GameType, SpawnType, TeamType, BoardCellType, LevelType


class ChessBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__(GameType.CHESS_GAME)
        self.page_name = 'chess'

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

        for move_column, move_row in [
            (piece_column, piece_row + direction),
        ]:
            if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_row >= self.num_blocks_vertical:
                continue

            piece_on_move_cell: Piece = current_map[move_row][move_column]
            move = Cell(
                move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                piece=piece, destroy_figures=[piece_on_move_cell, ] if piece_on_move_cell is not None else [])

            if piece_on_move_cell is not None:
                continue

            moves.append(move)

        for move_column, move_row in [
            (piece_column - 1, piece_row + direction),
            (piece_column + 1, piece_row + direction),
        ]:
            if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_row >= self.num_blocks_vertical:
                continue

            piece_on_move_cell: Piece = current_map[move_row][move_column]
            move = Cell(
                move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                piece=piece, destroy_figures=[piece_on_move_cell, ] if piece_on_move_cell is not None else [])

            if piece_on_move_cell is not None:
                if piece_on_move_cell.team_type == team_type:
                    continue
                elif piece_on_move_cell.team_type == enemy_team_type:
                    move.destroy_figures.append(piece_on_move_cell)
                if only_with_destroyed_pieces:
                    if len(move.destroy_figures) == 0:
                        continue
                moves.append(move)
        return moves
