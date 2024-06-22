import typing

import pygame

from utils.cell import Cell
from utils.page import BasePage
from utils.button import Button
import copy
import typing
import math
from pygame.event import Event
from os import path

from time import sleep

from utils.piece import Piece
from utils.start_app import start_app
from utils.types import GameType, TeamType, SpawnType, BoardCellType, EventType, LevelType
from random import shuffle, choice


class BaseBoardPage(BasePage):

    def __init__(self, game_type: GameType):
        super().__init__()
        self.game_type = game_type
        self.current_step = TeamType.WHITE_TEAM
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
            self.block_size, self.block_size, self.game_type, TeamType.WHITE_TEAM, SpawnType.BOTTOM_SPAWN
        )
        self.white_team_pieces_storage: typing.List[Piece] = []
        self.black_team_pieces = Piece.generate_pieces(
            self.board_x, self.board_y, self.num_blocks_horizontal, self.num_blocks_vertical,
            self.block_size, self.block_size, self.game_type, TeamType.BLACK_TEAM, SpawnType.TOP_SPAWN)
        self.black_team_pieces_storage: typing.List[Piece] = []

        self.winner_overlay = pygame.Surface((self.SCREEN.get_width(), self.SCREEN.get_height()), pygame.SRCALPHA)
        self.winner_overlay.fill(self.thema.winner_glow)

        self.loser_overlay = pygame.Surface((self.SCREEN.get_width(), self.SCREEN.get_height()), pygame.SRCALPHA)
        self.loser_overlay.fill(self.thema.loser_glow)

        button_width = 300
        button_height = 50
        buttons_margin = 20
        button_x = self.SCREEN.get_width() // 2 - button_width // 2
        button_y = self.SCREEN.get_height() // 2.5

        self.menu_button = Button(button_x, button_y, button_width, button_height, "Menu",
                                  self.thema.button_text, background=self.thema.button_background, )
        button_y += button_height + buttons_margin
        self.repeat_button = Button(button_x, button_y, button_width, button_height, "Spiel wiederholen",
                                    self.thema.button_text, background=self.thema.button_background, )

        button_y += button_height + buttons_margin
        self.toptable_button = Button(button_x, button_y, button_width, button_height, "Rating-Tabelle",
                                    self.thema.button_text, background=self.thema.button_background, )

        self.drawing_button_list = (
            self.menu_button,
            self.repeat_button,
            self.toptable_button
        )

    def change_step_side(self):
        if self.won or self.check_winner():
            self.won = True

        elif self.current_step == TeamType.WHITE_TEAM:
            self.current_step = TeamType.BLACK_TEAM
        elif self.current_step == TeamType.BLACK_TEAM:
            self.current_step = TeamType.WHITE_TEAM

    def draw(self):
        super().draw()

        # BOARD

        outer_rect = [
            self.board_x - self.block_border_width // 2,
            self.board_y - self.block_border_width // 2,
            self.num_blocks_horizontal * self.block_size + self.block_border_width,
            self.num_blocks_vertical * self.block_size + self.block_border_width
        ]
        pygame.draw.rect(self.SCREEN, self.thema.background, outer_rect, border_radius=5)

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

        # WINNER OR LOSER

        if self.won:
            if self.current_step == TeamType.WHITE_TEAM:
                self.SCREEN.blit(self.winner_overlay, (0, 0))
                text = self.BIG_FONT.render('SIE SIND GEWINNER :)', True, self.thema.winner_notification_text,
                                            self.thema.winner_notification_background)
                text_rect = text.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 3))
                self.SCREEN.blit(text, text_rect)
            elif self.current_step == TeamType.BLACK_TEAM:
                self.SCREEN.blit(self.loser_overlay, (0, 0))
                text = self.BIG_FONT.render('SIE SIND VERLIERER :(', True, self.thema.loser_notification_text,
                                            self.thema.loser_notification_background)
                text_rect = text.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 3))
                self.SCREEN.blit(text, text_rect)

            for button in self.drawing_button_list:
                button.draw(self.SCREEN)

    def minimax(self, current_map: typing.List[typing.List], main_team: TeamType, current_team: TeamType,
                depth: int, alpha: int, beta: int, skip_if_destroyed_figures=False) -> typing.Tuple[int, Cell or None]:

        if depth == 0:
            return 0, None  # Assuming 0 is the base evaluation at depth 0

        current_team_pieces = [piece for row in current_map for piece in row if
                               piece and piece.team_type == current_team]

        all_moves = []
        for piece in current_team_pieces:
            moves = self.get_moves(
                piece_column=piece.minmax_place_column,
                piece_row=piece.minmax_place_row,
                team_type=current_team,
                current_map=current_map
            )
            all_moves.extend(moves)

        best_move = []
        if main_team == current_team:
            max_eval = -math.inf
            for move in all_moves:
                new_board = copy.deepcopy(current_map)
                new_board[move.piece.minmax_place_row][move.piece.minmax_place_column] = None
                new_piece = copy.deepcopy(move.piece)
                new_board[move.board_row][move.board_column] = new_piece
                new_piece.minmax_place_row = move.board_row
                new_piece.minmax_place_column = move.board_column

                destroy_figures_count = len(move.destroy_figures)
                if not skip_if_destroyed_figures or destroy_figures_count == 0:
                    current_team = self.reverse_team(current_team)
                evaluation, _ = self.minimax(new_board, main_team, current_team, depth - 1, alpha,
                                             beta, skip_if_destroyed_figures)

                evaluation += len(move.destroy_figures)

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = [move, ]
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in all_moves:
                new_board = copy.deepcopy(current_map)
                new_board[move.piece.minmax_place_row][move.piece.minmax_place_column] = None
                new_piece = copy.deepcopy(move.piece)
                new_board[move.board_row][move.board_column] = new_piece
                new_piece.minmax_place_row = move.board_row
                new_piece.minmax_place_column = move.board_column

                destroy_figures_count = len(move.destroy_figures)
                if not skip_if_destroyed_figures or destroy_figures_count == 0:
                    current_team = self.reverse_team(current_team)
                evaluation, _ = self.minimax(new_board, main_team, current_team, depth - 1, alpha,
                                             beta, skip_if_destroyed_figures)
                evaluation -= len(move.destroy_figures)

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = [move, ]
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def handle_event(self, event: Event):

        if self.won:

            if self.repeat_button.is_clicked(event):
                self.restart_game()
            elif self.menu_button.is_clicked(event):
                self.set_as_current_page_by_page_name('menu')
            elif self.toptable_button.is_clicked(event):
                self.set_as_current_page_by_page_name('toptable')

        elif event.type == EventType.ENEMY_MOVE_EVENT and self.current_step == TeamType.BLACK_TEAM:

            pygame.time.set_timer(EventType.ENEMY_MOVE_EVENT, 0)

            self.make_enemy_move()
            self.selected_piece = None
            self.change_step_side()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.current_step == TeamType.WHITE_TEAM:
                for i, piece in enumerate(self.pieces_by_current_teams_step):
                    if piece.is_clicked(event):
                        self.selected_piece = piece

            if self.selected_piece is not None:

                for move in self.current_moves:
                    if move.is_clicked(event):

                        self.selected_piece.board_place_column = move.board_column
                        self.selected_piece.board_place_row = move.board_row

                        enemy_piece_on_move = \
                            self.get_current_map_with_pieces(BoardCellType.ENEMY_CELL)[move.board_row][
                                move.board_column]

                        skip_next_team_change = False
                        if enemy_piece_on_move is not None:

                            if self.current_step == TeamType.WHITE_TEAM:
                                enemy_piece_on_move.board_x = self.storage_right_x
                                enemy_piece_on_move.board_y = self.storage_right_y
                                enemy_piece_on_move.board_place_row = len(self.white_team_pieces_storage)
                                enemy_piece_on_move.board_place_column = 0

                                self.white_team_pieces_storage.append(enemy_piece_on_move)

                            self.enemy_pieces_by_current_teams_step.remove(enemy_piece_on_move)

                            if not move.skip_next_team_change:
                                moves = self.get_moves(
                                    piece_column=self.selected_piece.board_place_column,
                                    piece_row=self.selected_piece.board_place_row,
                                    team_type=self.selected_piece.team_type,
                                    current_map=self.get_current_map_with_pieces(BoardCellType.ALL_CELL),
                                    only_with_destroyed_pieces=True
                                )
                                self.__current_moves = moves
                                if len(moves) == 0:
                                    skip_next_team_change = False

                        if not skip_next_team_change:
                            self.selected_piece = None
                            self.change_step_side()

                        pygame.time.set_timer(EventType.ENEMY_MOVE_EVENT, 1000)
                        break

    def get_current_map_with_pieces(self, board_cell_type=BoardCellType.ALL_CELL):
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

    def make_move(self, pieces_with_moves: typing.List[typing.Tuple[Piece, typing.List[Cell]]]) -> Cell:
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
    
    def get_moves(self, piece_column: int, piece_row: int, team_type: TeamType,
                     current_map: typing.List[typing.List[Piece or None]], only_with_destroyed_pieces=False) -> \
            typing.List[Cell]:
        return []
    
    @property
    def current_step_direction(self):
        direction_team = -1 if self.current_step == TeamType.WHITE_TEAM else 1
        return direction_team

    @staticmethod
    def get_current_step_direction_by_team(team: TeamType):
        direction_team = -1 if team == TeamType.WHITE_TEAM else 1
        return direction_team

    @staticmethod
    def reverse_team(team: TeamType):
        if team == TeamType.WHITE_TEAM:
            return TeamType.BLACK_TEAM
        elif team == TeamType.BLACK_TEAM:
            return TeamType.WHITE_TEAM
        else:
            return TeamType.UNKNOWN_TEAM

    @property
    def selected_piece(self) -> Piece:
        return self.__selected_piece

    def restart_game(self):

        self.__selected_piece = None
        self.__current_moves = []

        self.white_team_pieces = Piece.generate_pieces(
            self.board_x, self.board_y, self.num_blocks_horizontal, self.num_blocks_vertical,
            self.block_size, self.block_size, self.game_type, TeamType.WHITE_TEAM, SpawnType.BOTTOM_SPAWN
        )
        self.white_team_pieces_storage: typing.List[Piece] = []
        self.black_team_pieces = Piece.generate_pieces(
            self.board_x, self.board_y, self.num_blocks_horizontal, self.num_blocks_vertical,
            self.block_size, self.block_size, self.game_type, TeamType.BLACK_TEAM, SpawnType.TOP_SPAWN)
        self.black_team_pieces_storage: typing.List[Piece] = []

        self.current_step = TeamType.WHITE_TEAM
        self.won = False

    @selected_piece.setter
    def selected_piece(self, value: Piece):
        self.__selected_piece = value
        self.won = False
        if value is not None:
            self.__current_moves = self.get_moves(
                self.selected_piece.board_place_column,
                self.selected_piece.board_place_row,
                self.selected_piece.team_type,
                self.get_current_map_with_pieces(BoardCellType.ALL_CELL)
            )
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

        if self.current_step == TeamType.BLACK_TEAM:

            if self.config.game_difficulty_level == LevelType.EASY:
                depth = 1
            elif self.config.game_difficulty_level == LevelType.MEDIUM:
                depth = 2
            elif self.config.game_difficulty_level == LevelType.HARD:
                depth = 4
            else:
                depth = 0

            if depth > 0:
                _, cells = self.minimax(
                    current_map=self.get_current_map_with_pieces(BoardCellType.ALL_CELL),
                    main_team=TeamType.BLACK_TEAM,
                    current_team=TeamType.BLACK_TEAM,
                    depth=depth,
                    alpha=0,
                    beta=0
                )
            else:
                cells = []
                shuffle(self.black_team_pieces)
                for piece in self.black_team_pieces:
                    moves = self.get_moves(piece.board_place_column, piece.board_place_row, piece.team_type, self.get_current_map_with_pieces(BoardCellType.ALL_CELL))
                    if len(moves) > 0:
                        cells = [choice(moves),]

            for cell in cells:
                move: Cell = cell
                self.selected_piece = move.piece
                self.selected_piece.board_place_column = move.board_column
                self.selected_piece.board_place_row = move.board_row

                for destroy_piece in move.destroy_figures:

                    self.enemy_pieces_by_current_teams_step.remove(destroy_piece)

                    destroy_piece.board_x = self.storage_left_x
                    destroy_piece.board_y = self.storage_left_y
                    destroy_piece.board_place_row = len(self.white_team_pieces_storage)
                    destroy_piece.board_place_column = 0

                    self.white_team_pieces_storage.append(move.piece)

    def exit_event(self):
        pass
