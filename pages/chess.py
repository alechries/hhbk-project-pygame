import typing

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

    def handle_event(self, event: Event):
        super().handle_event(event)

    def minimax(self, position, depth: int, alpha: int, beta:int, max_player:bool, game, ):
        if depth == 0 or not self.check_winner() :
            return None, position

        if max_player:
            max_eval = -math.inf
            best_move = None
            for move in get_all_moves(position, WHITE, game):
                evaluation = minimax(move, depth - 1, alpha, beta, False, game)[0]
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                if max_eval == evaluation:
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in get_all_moves(position, RED, game):
                evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
                if min_eval == evaluation:
                    best_move = move
            return min_eval, best_move