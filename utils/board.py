import typing

import pygame

from utils.cell import Cell
from utils.page import BasePage
from pygame.event import Event

from time import sleep

from utils.piece import Piece
from utils.start_app import start_app
from utils.types import GameType, TeamType, SpawnType, BoardCellType, EventType
from random import choice


class BaseBoardPage(BasePage):

    def __init__(self, game_type: GameType):
        super().__init__()

        self.current_step = TeamType.WHITE_TEAM
        self.game_type = game_type
        self.__selected_piece = None
        self.__current_moves = []
        self.won = False

        self.num_blocks_horizontal = 6
        self.num_blocks_vertical = self.num_blocks_horizontal
        self.block_border_width = 0
        self.outer_border_width = 2

        self.w = self.SCREEN.get_width()
        self.h = self.SCREEN.get_height()

        self.smaller_side_size = self.w if self.w < self.h else self.h
        self.smaller_num_blocks = self.num_blocks_vertical if self.num_blocks_vertical < self.num_blocks_horizontal else self.num_blocks_horizontal

        self.block_size = (self.smaller_side_size / 100 * self.config.board_size_percent) / self.smaller_num_blocks
        self.piece_size = self.block_size * 0.8

        self.board_x = (self.SCREEN.get_width() - (self.num_blocks_horizontal * self.block_size)) // 2
        self.board_y = (self.SCREEN.get_height() - (self.num_blocks_vertical * self.block_size)) // 2

        self.board_indent = self.SCREEN.get_width() // 100 * 5
        self.storage_left_x = self.board_x - self.board_indent - self.block_size
        self.storage_left_y = self.board_y
        self.storage_left_width = self.block_size
        self.storage_left_height = self.num_blocks_vertical * self.block_size
        self.storage_right_x = self.board_x + self.block_size * self.num_blocks_horizontal + self.board_indent
        self.storage_right_y = self.board_y
        self.storage_right_width = self.block_size
        self.storage_right_height = self.storage_left_height

        self.white_team_pieces = Piece.generate_pieces(
            self.board_x, self.board_y, self.num_blocks_horizontal, self.num_blocks_vertical,
            self.block_size, self.block_size, game_type, TeamType.WHITE_TEAM, SpawnType.BOTTOM_SPAWN
        )
        self.white_team_pieces_storage: typing.List[Piece] = []
        self.black_team_pieces = Piece.generate_pieces(
            self.board_x, self.board_y, self.num_blocks_horizontal, self.num_blocks_vertical,
            self.block_size, self.block_size, game_type, TeamType.BLACK_TEAM, SpawnType.TOP_SPAWN)
        self.black_team_pieces_storage: typing.List[Piece] = []

    def change_step_side(self):
        if self.won:
            self.current_step = TeamType.UNKNOWN_TEAM
        elif self.current_step == TeamType.WHITE_TEAM:
            self.current_step = TeamType.BLACK_TEAM
        elif self.current_step == TeamType.BLACK_TEAM:
            self.current_step = TeamType.WHITE_TEAM

    def draw(self):

        # BOARD

        for row in range(self.num_blocks_vertical):
            for column in range(self.num_blocks_horizontal):

                x = self.board_x + (column * self.block_size)
                y = self.board_y + (row * self.block_size)
                color = self.thema.table_part_0 if (row + column) % 2 == 0 else self.thema.table_part_1
                pygame.draw.rect(self.SCREEN, color, [x, y, self.block_size, self.block_size], border_radius=5)
                if self.block_border_width > 0:
                    pygame.draw.rect(self.SCREEN, self.thema.border, [x, y, self.block_size, self.block_size],
                                     self.block_border_width, border_radius=5)

        if self.outer_border_width > 0:
            outer_rect = [
                self.board_x - self.block_border_width // 2,
                self.board_y - self.block_border_width // 2,
                self.num_blocks_horizontal * self.block_size + self.block_border_width,
                self.num_blocks_vertical * self.block_size + self.block_border_width
            ]
            pygame.draw.rect(self.SCREEN, self.thema.border, outer_rect, self.outer_border_width, border_radius=5)

        # STORAGE PIECES

        black_team_pieces_storage_length = len(self.black_team_pieces_storage)
        if black_team_pieces_storage_length > 0:
            pygame.draw.rect(self.SCREEN, self.config.GRAY,
                             [self.storage_left_x, self.storage_left_y, self.storage_left_width,
                              self.block_size * black_team_pieces_storage_length], border_radius=5)

        white_team_pieces_storage_length = len(self.white_team_pieces_storage)
        if white_team_pieces_storage_length > 0:
            pygame.draw.rect(self.SCREEN, self.config.GRAY,
                             [self.storage_right_x, self.storage_right_y, self.storage_right_width,
                              self.block_size * white_team_pieces_storage_length], border_radius=5)

        # if len(self.white_team_pieces_storage) > 0:
        #     pygame.draw.rect(self.SCREEN, self.config.GRAY,
        #                      [self.storage_right_x, self.storage_right_y, self.storage_right_width,
        #                       self.storage_right_height])

        # ALL PIECES

        for piece in self.all_pieces:
            piece.draw(self.SCREEN)

        # SELECTED PIECE

        if self.selected_piece is not None:
            pygame.draw.rect(
                self.SCREEN, self.config.BLACK,
                [
                    self.selected_piece.x, self.selected_piece.y,
                    self.selected_piece.width, self.selected_piece.height
                ],
                2, border_radius=5
            )

        # PIECES BY CURRENT TEAMS STEP

        elif self.config.board_side_lighting:
            for piece in self.pieces_by_current_teams_step:
                pygame.draw.rect(
                    self.SCREEN, self.config.BLUE,
                    [
                        piece.x + 2, piece.y + 2,
                        piece.width - 4, piece.height - 4
                    ],
                    2, border_radius=5
                )

        # STEPS

        for move in self.current_moves:
            pygame.draw.rect(self.SCREEN, self.config.RED, [
                self.board_x + (move.board_column * self.block_size),
                self.board_y + (move.board_row * self.block_size),
                self.block_size, self.block_size
            ], 3, border_radius=5)

    def get_current_map_with_pieces(self, board_cell_type=BoardCellType.EMPTY_CELL):
        matrix = [[None for _ in range(self.num_blocks_horizontal)] for _ in range(self.num_blocks_vertical)]

        if board_cell_type == BoardCellType.ENEMY_CELL:
            for p in self.enemy_pieces_by_current_teams_step:
                matrix[p.board_place_row][p.board_place_column] = p
        elif board_cell_type == BoardCellType.TEAM_CELL:
            for p in self.pieces_by_current_teams_step:
                matrix[p.board_place_row][p.board_place_column] = p
        else:
            for p in self.active_pieces:
                matrix[p.board_place_row][p.board_place_column] = p

        return matrix

    @property
    def current_moves(self) -> typing.List[Cell]:
        return self.__current_moves

    @property
    def active_pieces(self) -> typing.List[Piece]:
        return self.white_team_pieces + self.black_team_pieces

    @property
    def all_pieces(self) -> typing.List[Piece]:
        return self.active_pieces + self.inactive_pieces

    @property
    def inactive_pieces(self) -> typing.List[Piece]:
        return self.white_team_pieces_storage + self.black_team_pieces_storage

    def minmax_move(self, pieces_with_moves: typing.List[typing.Tuple[Piece, typing.List[Cell]]]) -> Cell:
        pass

    @property
    def pieces_by_current_teams_step(self) -> typing.List[Piece]:
        if self.current_step == TeamType.WHITE_TEAM:
            return self.white_team_pieces
        elif self.current_step == TeamType.BLACK_TEAM:
            return self.black_team_pieces

    @property
    def enemy_pieces_by_current_teams_step(self) -> typing.List[Piece]:
        if self.current_step == TeamType.WHITE_TEAM:
            return self.black_team_pieces
        elif self.current_step == TeamType.BLACK_TEAM:
            return self.white_team_pieces

    def get_valid_moves_inside(self, move_coord_list: typing.List[typing.Tuple[int, int]]) -> typing.List[Cell]:
        moves: typing.List[Cell] = []

        for move_column, move_row in move_coord_list:
            if 0 <= move_column < self.num_blocks_horizontal and 0 <= move_row < self.num_blocks_vertical:
                if not any(
                        [piece_on_way.board_place_column == move_column and piece_on_way.board_place_row == move_row for
                         piece_on_way in self.pieces_by_current_teams_step]):
                    moves.append(Cell(
                        move_row, move_column, self.board_x, self.board_y, self.block_size, self.block_size,
                    ))
        return moves

    def get_moves(self, selected_piece: Piece) -> typing.List[Cell]:
        return []

    @property
    def current_step_direction(self):
        direction_team = -1 if self.current_step == TeamType.WHITE_TEAM else 1
        return direction_team

    @property
    def selected_piece(self) -> Piece:
        return self.__selected_piece

    @selected_piece.setter
    def selected_piece(self, value: Piece):
        self.__selected_piece = value
        self.won = False
        if value is not None:
            self.__current_moves = self.get_moves(self.selected_piece)
        else:
            self.__current_moves = []

    def check_winner(self):

        if self.current_step == TeamType.BLACK_TEAM:
            return any((
                len(self.white_team_pieces) == 0,
                any([p.board_place_row == self.num_blocks_vertical - 1 for p in self.black_team_pieces])
            ))
        elif self.current_step == TeamType.WHITE_TEAM:
            return any((
                len(self.black_team_pieces) == 0,
                any([p.board_place_row == 0 for p in self.white_team_pieces])
            ))
        else:
            return False

    def make_enemy_move(self):

        pieces_with_moves: typing.List[typing.Tuple[Piece, typing.List[Cell]]] = []

        for enemy in self.pieces_by_current_teams_step:
            moves = self.get_moves(enemy)

            if len(moves) > 0:
                pieces_with_moves.append(
                    (enemy, moves)
                )

        # self.selected_piece, moves = choice(pieces_with_moves)
        # move = choice(moves)

        move = self.minmax_move(pieces_with_moves)

        self.selected_piece.board_place_column = move.board_column
        self.selected_piece.board_place_row = move.board_row

        enemy_piece_on_move = self.get_current_map_with_pieces(BoardCellType.ENEMY_CELL)[move.board_row][
            move.board_column]
        if enemy_piece_on_move is not None:

            if self.current_step == TeamType.BLACK_TEAM:

                enemy_piece_on_move.board_x = self.storage_left_x
                enemy_piece_on_move.board_y = self.storage_left_y
                enemy_piece_on_move.board_place_row = len(self.black_team_pieces_storage)
                enemy_piece_on_move.board_place_column = 0

                self.black_team_pieces_storage.append(enemy_piece_on_move)

            self.enemy_pieces_by_current_teams_step.remove(enemy_piece_on_move)

    def handle_event(self, event: Event):

        if event.type == EventType.ENEMY_MOVE_EVENT:
            pygame.time.set_timer(EventType.ENEMY_MOVE_EVENT, 0)

            self.make_enemy_move()
            self.selected_piece = None
            self.change_step_side()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.current_step == TeamType.WHITE_TEAM:
                for i, piece in enumerate(self.pieces_by_current_teams_step):
                    if piece.is_clicked(event):
                        if self.selected_piece is not None:
                            self.selected_piece = None if self.selected_piece.is_clicked(event) else piece
                        else:
                            self.selected_piece = piece

            if self.selected_piece is not None:

                for move in self.current_moves:
                    if move.is_clicked(event):

                        self.selected_piece.board_place_column = move.board_column
                        self.selected_piece.board_place_row = move.board_row

                        enemy_piece_on_move = self.get_current_map_with_pieces(BoardCellType.ENEMY_CELL)[move.board_row][
                            move.board_column]
                        if enemy_piece_on_move is not None:

                            if self.current_step == TeamType.WHITE_TEAM:

                                enemy_piece_on_move.board_x = self.storage_right_x
                                enemy_piece_on_move.board_y = self.storage_right_y
                                enemy_piece_on_move.board_place_row = len(self.white_team_pieces_storage)
                                enemy_piece_on_move.board_place_column = 0

                                self.white_team_pieces_storage.append(enemy_piece_on_move)

                            self.enemy_pieces_by_current_teams_step.remove(enemy_piece_on_move)

                        if self.check_winner():
                            self.won = True

                        self.selected_piece = None
                        self.change_step_side()

                        pygame.time.set_timer(EventType.ENEMY_MOVE_EVENT, 1000)



    def exit_event(self):
        pass
