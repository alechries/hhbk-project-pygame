import copy
import typing

from utils.board import BaseBoardPage
from utils.cell import Cell
from pygame.event import Event
from random import choice
import pygame
from utils.piece import Piece
from utils.types import GameType, SpawnType, TeamType, BoardCellType, LevelType
import math


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
                current_map=self.get_current_map_with_pieces(self.get_current_map_with_pieces(BoardCellType.ENEMY_CELL)),
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

    def handle_event(self, event: Event):
        super().handle_event(event)

    def minimax(self, current_map: typing.List[typing.List[Piece]], main_team: TeamType, current_team: TeamType,
                depth: int, alpha: int, beta: int) -> typing.Tuple[Piece, Cell] or None:

        if depth == 0 or not self.check_winner():
            return None

        # temp_map = self.get_current_map_with_pieces(BoardCellType.EMPTY_CELL)

        current_team_pieces = []
        for row in current_map:
            for piece in row:
                if piece is None:
                    continue

                if piece.team_type == current_team:
                    current_team_pieces.append(piece)

        all_moves = []

        for current_team_piece in current_team_pieces:
            for move in self.get_moves_by_board_placement(current_team_piece.minmax_place_column, current_team_piece.minmax_place_row, current_team_piece.team_type):
                cell = current_map[move.board_row][move.board_column]
                if cell is not None:
                    if cell.team_type == current_team:
                        continue

                all_moves.append(
                    (current_team_piece, move)
                )

        for piece, move in all_moves:
            new_board = copy.deepcopy(current_map)
            new_board[piece.minmax_place_row][piece.minmax_place_column] = None
            new_piece = copy.deepcopy(piece)
            new_board[move.board_row][move.board_column] = new_piece
            new_piece.minmax_place_row = move.board_row
            new_piece.minmax_place_column = move.board_column

            if main_team == current_team:

                max_eval = -math.inf

                best_move = None
                
                evaluation = \
                    self.minimax(new_board, main_team, self.reverse_team(current_team), depth - 1, alpha, beta)[0]
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                if max_eval == evaluation:
                    best_move = move

                return max_eval, best_move, piece, move
            else:

                min_eval = math.inf

                best_move = None
                evaluation = \
                    self.minimax(new_board, main_team, self.reverse_team(current_team), depth - 1, alpha, beta)[0]
                min_eval = min(min_eval, evaluation)
                alpha = min(alpha, evaluation)
                if beta <= alpha:
                    break
                if min_eval == evaluation:
                    best_move = move

                return min_eval, best_move, piece, move
