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
        self.guide_message = [
            'Das Ziel des Spiels ist es, seine eigene Figur (Spieler = Weiß)',
            'auf die Grundlinie des Gegners (Computer = Schwarz) zu setzen.',
            'Die eigene Figur hat zwei verschiedene Züge.',
            'Man kann einmal den Bauern nach vorne bewegen,',
            'solange kein eigener oder gegnerischer Bauer im Feld steht.',
            'Falls diagonal vom Bauer ein gegnerischer Bauer steht,',
            'so kann man diesen durch einen diagonalen Zug schlagen.',
            'Falls man selber keinen Zug mehr durchführen kann oder es keine Figuren mehr gibt,',
            'dann ist die Partie auch beendet.',
        ]

    def get_moves(self, piece_column: int, piece_row: int, team_type: TeamType,
                  current_map: typing.List[typing.List[Piece]], only_with_destroyed_pieces=False) -> \
            typing.List[Cell]:

        piece: Piece = current_map[piece_row][piece_column]

        if team_type == TeamType.WHITE_TEAM:
            direction = -1
            enemy_team_type = TeamType.BLACK_TEAM
        elif team_type == TeamType.BLACK_TEAM:
            direction = 1
            enemy_team_type = TeamType.WHITE_TEAM
        else:
            return []

        if piece is None:
            return []

        moves: typing.List[Cell] = []

        if not only_with_destroyed_pieces:

            for move_column, move_row in [
                (piece_column, piece_row + direction),
            ]:
                if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_row >= self.num_blocks_vertical:
                    continue

                piece_on_move_cell: Piece = current_map[move_row][move_column]

                if piece_on_move_cell is None:
                    move = Cell(
                        move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                        piece=piece)
                    moves.append(move)

        for move_column, move_row in [
            (piece_column - 1, piece_row + direction),
            (piece_column + 1, piece_row + direction),
        ]:
            if move_column < 0 or move_column >= self.num_blocks_horizontal or move_row < 0 or move_row >= self.num_blocks_vertical:
                continue

            piece_on_move_cell: Piece = current_map[move_row][move_column]

            if piece_on_move_cell is not None:
                if piece_on_move_cell.team_type == enemy_team_type:
                    move = Cell(
                        move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                        piece=piece, destroy_figures=[piece_on_move_cell, ])

                    if only_with_destroyed_pieces:
                        if len(move.destroy_figures) == 0:
                            continue
                    moves.append(move)
        return moves

    def generate_pieces(self, team_type: TeamType, spawn_type: SpawnType) -> typing.List[Piece]:

        # direction = -1 if spawn_type == SpawnType.BOTTOM_SPAWN else 1

        created_pieces: typing.List[Piece] = []

        spawn_row = 0 if spawn_type == SpawnType.TOP_SPAWN else self.num_blocks_vertical - 1

        for i_column in range(self.num_blocks_horizontal):
            created_pieces.append(
                Piece(
                    board_x=self.board_x,
                    board_y=self.board_y,
                    width=self.piece_size,
                    height=self.piece_size,
                    board_place_row=spawn_row,
                    board_place_column=i_column,
                    game_type=self.game_type,
                    team_type=team_type,
                    spawn_type=spawn_type
                )
            )

        return created_pieces
