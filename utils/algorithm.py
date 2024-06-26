import copy
import math
import typing
from typing import Tuple, List, Any, Optional
from utils.cell import Cell
from utils.piece import Piece
from utils.types import TeamType
from random import shuffle


class Algorithm:

    @staticmethod
    def reverse_team(team: TeamType):
        if team == TeamType.WHITE_TEAM:
            return TeamType.BLACK_TEAM
        elif team == TeamType.BLACK_TEAM:
            return TeamType.WHITE_TEAM
        else:
            return TeamType.UNKNOWN_TEAM

    @staticmethod
    def minmax(board_page, current_map: typing.List[typing.List], main_team: TeamType, current_team: TeamType,
               depth: int, skip_if_destroyed_figures=False, iteration=0) -> typing.Tuple[int, Cell or None]:

        current_team_pieces: typing.List[Piece] = []
        enemy_team_pieces: typing.List[Piece] = []
        all_current_team_moves: typing.List[Cell] = []

        for row in current_map:
            for column in row:
                if column is not None:
                    piece: Piece = column

                    if piece.team_type == current_team:
                        current_team_pieces.append(piece)
                        moves = board_page.get_moves(
                            piece_column=piece.minmax_place_column,
                            piece_row=piece.minmax_place_row,
                            team_type=current_team,
                            current_map=current_map
                        )
                        for move in moves:
                            all_current_team_moves.append(move)

                    elif piece.team_type != current_team:
                        enemy_team_pieces.append(piece)

        if depth == 0 and len(all_current_team_moves) == 0:

            if main_team == current_team:
                points = len(current_team_pieces) - len(enemy_team_pieces)
            else:
                points = len(enemy_team_pieces) - len(current_team_pieces)
            return points, None

        best_move = None
        if main_team == current_team:
            max_eval = -math.inf

            for move in all_current_team_moves:

                new_map = Algorithm.get_new_map(current_map, move)

                destroy_figures_count = len(move.destroy_figures)
                if not skip_if_destroyed_figures or destroy_figures_count == 0:
                    current_team = Algorithm.reverse_team(current_team)

                evaluation, _ = Algorithm.minmax(board_page, new_map, main_team, current_team, depth - 1,
                                                 skip_if_destroyed_figures,
                                                 iteration=iteration + 1)

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

            return max_eval, best_move
        else:

            min_eval = math.inf
            for move in all_current_team_moves:

                new_map = Algorithm.get_new_map(current_map, move)

                destroy_figures_count = len(move.destroy_figures)
                if not skip_if_destroyed_figures or destroy_figures_count == 0:
                    current_team = Algorithm.reverse_team(current_team)

                evaluation, _ = Algorithm.minmax(board_page, new_map, main_team, current_team, depth - 1,
                                                 skip_if_destroyed_figures, iteration=iteration + 1)

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move

            return min_eval, best_move

    @staticmethod
    def get_new_map(current_map: typing.List[typing.List[Cell or None]], move: Cell) -> typing.List[
        typing.List[Piece or None]]:

        new_board = copy.deepcopy(current_map)
        new_board[move.piece.minmax_place_row][move.piece.minmax_place_column] = None
        new_piece = copy.deepcopy(move.piece)
        new_board[move.board_row][move.board_column] = new_piece
        new_piece.minmax_place_row = move.board_row
        new_piece.minmax_place_column = move.board_column

        return new_board
