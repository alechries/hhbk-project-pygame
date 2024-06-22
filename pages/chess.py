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

    def get_moves(self, selected_piece: Piece) -> typing.List[Cell]:

        direction = self.current_step_direction
        return self.get_valid_moves_inside(
            [
                (selected_piece.board_place_column - 1, selected_piece.board_place_row + direction),
                (selected_piece.board_place_column + 1, selected_piece.board_place_row + direction),
            ]
        )

    def get_moves_by_board_placement(self, column: int, row: int, team: TeamType) -> typing.List[Cell]:

        direction = BaseBoardPage.get_current_step_direction_by_team(team)
        return self.get_valid_moves_inside(
            [
                (column - 1, row + direction),
                (column + 1, row + direction),
            ]
        )

    def make_move(self, pieces_with_moves: typing.List[typing.Tuple[Piece, typing.List[Cell]]]):
        for p in self.all_pieces:
            p.minmax_place_row = p.board_place_row
            p.minmax_place_column = p.board_place_column

        if self.config.game_difficulty_level == LevelType.EASY:
            minimax_result = self.minimax(
                current_map=self.get_current_map_with_pieces(
                    self.get_current_map_with_pieces(BoardCellType.ENEMY_CELL)),
                main_team=self.current_step,
                current_team=self.current_step,
                depth=4,
                alpha=0,
                beta=0,
            )
            if minimax_result is not None:
                piece: Piece = minimax_result[2]
                cell: Cell = minimax_result[3]
                self.selected_piece = piece
                return cell
            else:
                return None
        else:
            self.selected_piece, moves = choice(pieces_with_moves)
            move = choice(moves)
            return move

    def get_moves_v2(self, piece_column: int, piece_row: int, team_type: TeamType,
                     current_map: typing.List[typing.List[Piece]]) -> \
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
            (piece_column - 1, piece_row + direction),
            (piece_column + 1, piece_row + direction),
        ]:
            if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_column >= self.num_blocks_vertical:
                continue

            piece_on_move_cell: Piece = current_map[move_row][move_column]
            move = Cell(move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size, piece=piece, destroy_figures=[piece_on_move_cell, ] if piece_on_move_cell is not None else [])

            if piece_on_move_cell is not None:
                if piece_on_move_cell.team_type == team_type:
                    continue
                elif piece_on_move_cell.team_type == enemy_team_type:
                    move.destroy_figures.append(piece_on_move_cell)

            moves.append(move)
        return moves
