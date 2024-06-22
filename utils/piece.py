import typing

import pygame
from pygame.event import Event
from random import choice
from utils.types import GameType, TeamType, SpawnType, LevelType


class Piece:

    BLACK_PIECE_IMAGE = pygame.image.load('assets/images/black_piece.png')
    WHITE_PIECE_IMAGE = pygame.image.load('assets/images/white_piece.png')
    
    def __init__(self, board_x, board_y, width, height, board_place_row: int, board_place_column: int, game_type: GameType, team_type: TeamType, spawn_type: SpawnType):

        self.board_x = board_x
        self.board_y = board_y
        self.width = width
        self.height = height
        self.board_place_row = board_place_row
        self.board_place_column = board_place_column
        self.minmax_place_row = 0
        self.minmax_place_column = 0

        self.game_type = game_type if game_type else choice([GameType.CHESS_GAME, GameType.CHECKERS_GAME])
        self.team_type = team_type if team_type else TeamType.WHITE_TEAM
        self.spawn_type = spawn_type if spawn_type else SpawnType.BOTTOM_SPAWN

        self.selected = False

    @property
    def x(self):
        return self.board_x + (self.board_place_column * self.width)

    @property
    def y(self):
        return self.board_y + (self.board_place_row * self.height)

    @staticmethod
    def generate_pieces(board_x: int, board_y: int,  board_columns: int, board_rows: int, piece_width: int, piece_height: int, game_type: GameType, team_type: TeamType, spawn_type: SpawnType):

        # direction = -1 if spawn_type == SpawnType.BOTTOM_SPAWN else 1

        created_pieces: typing.List[Piece] = []

        if game_type == GameType.CHECKERS_GAME:
            spawn_row = 0 if spawn_type == SpawnType.TOP_SPAWN else board_rows - 1

            for i_column in range(board_columns):
                i_row = spawn_row if i_column % 2 != 0 else spawn_row + 1
                created_pieces.append(
                    Piece(
                        board_x=board_x,
                        board_y=board_y,
                        width=piece_width,
                        height=piece_height,
                        board_place_row=i_row,
                        board_place_column=i_column,
                        game_type=game_type,
                        team_type=team_type,
                        spawn_type=spawn_type
                    )
                )

        elif game_type == GameType.CHESS_GAME:
            spawn_row = 0 if spawn_type == SpawnType.TOP_SPAWN else board_rows - 1

            for i_column in range(board_columns):

                created_pieces.append(
                    Piece(
                        board_x=board_x,
                        board_y=board_y,
                        width=piece_width,
                        height=piece_height,
                        board_place_row=spawn_row,
                        board_place_column=i_column,
                        game_type=game_type,
                        team_type=team_type,
                        spawn_type=spawn_type
                    )
                )

        return created_pieces

    def draw(self, screen):
        piece_image = pygame.transform.scale(Piece.BLACK_PIECE_IMAGE if self.team_type == TeamType.BLACK_TEAM else Piece.WHITE_PIECE_IMAGE, (self.width * 0.8, self.height * 0.8))
        screen.blit(piece_image, (self.x + self.width * 0.1, self.y + self.height * 0.1))

    def is_clicked(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            return rect.collidepoint(event.pos)
        return False
