import typing

import pygame

from models.user import UserModel
from utils.cell import Cell
from utils.page import BasePage
from utils.button import Button
import copy
import typing
import math
from pygame.event import Event
from utils.piece import Piece
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
        self.show_guide = False
        self.guide_message = ['Kein Text :(']
        self.current_difficulty_level = LevelType(self.config.game_difficulty_level)

        self.num_blocks_horizontal = 6
        self.num_blocks_vertical = self.num_blocks_horizontal
        self.block_border_width = 0
        self.outer_border_width = 2

        self.w = self.SCREEN.get_width()
        self.h = self.SCREEN.get_height()

        self.smaller_side_size = self.w if self.w < self.h else self.h
        self.smaller_num_blocks = self.num_blocks_vertical if self.num_blocks_vertical < self.num_blocks_horizontal else self.num_blocks_horizontal

        self.block_size = (self.smaller_side_size / 100 * self.config.board_size_percent) / self.smaller_num_blocks
        self.piece_size = self.block_size

        self.board_x = (self.SCREEN.get_width() - (self.num_blocks_horizontal * self.block_size)) // 2
        self.board_y = (self.SCREEN.get_height() - (self.num_blocks_vertical * self.block_size)) // 2
        self.board_width = self.num_blocks_horizontal * self.block_size + self.block_border_width
        self.board_height = self.num_blocks_vertical * self.block_size + self.block_border_width

        self.board_indent = self.SCREEN.get_width() // 100 * 5
        self.storage_left_x = self.board_x - self.board_indent - self.block_size
        self.storage_left_y = self.board_y
        self.storage_left_width = self.block_size
        self.storage_left_height = self.num_blocks_vertical * self.block_size
        self.storage_right_x = self.board_x + self.block_size * self.num_blocks_horizontal + self.board_indent
        self.storage_right_y = self.board_y
        self.storage_right_width = self.block_size
        self.storage_right_height = self.storage_left_height

        self.white_team_pieces = self.generate_pieces(TeamType.WHITE_TEAM, SpawnType.BOTTOM_SPAWN)
        self.white_team_pieces_storage: typing.List[Piece] = []
        self.black_team_pieces = self.generate_pieces(TeamType.BLACK_TEAM, SpawnType.TOP_SPAWN)
        self.black_team_pieces_storage: typing.List[Piece] = []

        self.winner_overlay = pygame.Surface((self.SCREEN.get_width(), self.SCREEN.get_height()), pygame.SRCALPHA)
        self.winner_overlay.fill(self.thema.winner_glow)

        self.loser_overlay = pygame.Surface((self.SCREEN.get_width(), self.SCREEN.get_height()), pygame.SRCALPHA)
        self.loser_overlay.fill(self.thema.loser_glow)

        self.guide_overlay = pygame.Surface((self.SCREEN.get_width(), self.SCREEN.get_height()), pygame.SRCALPHA)
        self.guide_overlay.fill(self.thema.guide_glow)

        self.guide_width = 600
        self.guide_height = 200
        self.guide_x = (self.SCREEN.get_width() - self.guide_width) // 2
        self.guide_y = (self.SCREEN.get_height() - self.guide_height) // 2

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
        self.toptable_button = Button(button_x, button_y, button_width, button_height, "Bestenliste",
                                      self.thema.button_text, background=self.thema.button_background, )

        self.end_button_list = (
            self.menu_button,
            self.repeat_button,
            self.toptable_button
        )

        button_width = 150
        button_height = 30
        button_margin = 20

        button_x = self.board_x
        button_y = self.board_y - button_height - button_margin

        self.back_button = Button(button_x, button_y, button_width, button_height, "Menu",
                                  self.thema.button_text, background=self.thema.button_background, )

        button_x = self.board_x + self.board_width - button_width
        self.help_button = Button(button_x, button_y, button_width, button_height, "Hilfe",
                                  self.thema.button_text, background=self.thema.button_background, )

        self.main_button_list = (
            self.back_button,
            self.help_button,
        )

        button_x = self.board_x + self.board_width - button_width
        self.guide_close_button = Button(button_x, button_y, button_width, button_height, "Verstanden",
                                         self.thema.button_text, background=self.thema.button_background, )

    def change_step_side(self):
        if self.won or self.check_winner():
            if not self.won and self.current_user is not None:
                user: UserModel = self.current_user
                if user.logged_in:

                    if self.current_step == TeamType.WHITE_TEAM:

                        if self.current_difficulty_level == LevelType.EASY:

                            if self.game_type == GameType.CHECKERS_GAME:
                                user.increment_checkers_wins_easy()
                            elif self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_easy()

                        elif self.current_difficulty_level == LevelType.MEDIUM:

                            if self.game_type == GameType.CHECKERS_GAME:
                                user.increment_checkers_wins_medium()
                            elif self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_medium()

                        elif self.current_difficulty_level == LevelType.HARD:

                            if self.game_type == GameType.CHECKERS_GAME:
                                user.increment_checkers_wins_hard()
                            elif self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_hard()

                    elif self.current_step == TeamType.BLACK_TEAM:

                        if self.current_difficulty_level == LevelType.EASY:

                            if self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_easy()
                            elif self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_easy()

                        elif self.current_difficulty_level == LevelType.MEDIUM:

                            if self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_medium()
                            elif self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_medium()

                        elif self.current_difficulty_level == LevelType.HARD:

                            if self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_hard()
                            elif self.game_type == GameType.CHESS_GAME:
                                user.increment_chess_wins_hard()

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
            self.board_width, self.board_height
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

        # INFO

        pygame.draw.rect(self.SCREEN, self.thema.notification_text,
                         [self.board_x, self.board_y + self.board_height + 20, self.board_width, 40
                          ], border_radius=2)

        game_name = 'UNKNOWN'
        level_name = 'UNKNOWN'

        if self.game_type == GameType.CHECKERS_GAME:
            game_name = 'Dame'
        elif self.game_type == GameType.CHESS_GAME:
            game_name = 'Bauernschach'

        if self.current_difficulty_level == LevelType.EASY:
            level_name = 'Easy'
        elif self.current_difficulty_level == LevelType.MEDIUM:
            level_name = 'Medium'
        elif self.current_difficulty_level == LevelType.HARD:
            level_name = 'Hard'

        text = self.MEDIUM_FONT.render(f'{game_name} - {level_name}', True, self.config.LIGHT_GRAY)
        text_rect = text.get_rect(
            center=((self.board_x + self.board_width // 2), self.board_y + self.board_height + 40))
        self.SCREEN.blit(text, text_rect)

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

            for button in self.end_button_list:
                button.draw(self.SCREEN)

        else:

            for button in self.main_button_list:
                button.draw(self.SCREEN)

        # Guide message
        if self.show_guide:

            self.SCREEN.blit(self.guide_overlay, (0, 0))

            guide_bg_color = self.thema.notification_background
            guide_text_color = self.thema.notification_text
            pygame.draw.rect(self.SCREEN, guide_bg_color,
                             (self.guide_x, self.guide_y, self.guide_width, self.guide_height),
                             border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.notification_border,
                             (self.guide_x, self.guide_y, self.guide_width, self.guide_height), 2,
                             border_radius=10)

            line_height = 18
            lines_height = len(self.guide_message) * line_height
            for i, text in enumerate(self.guide_message):
                guide_text = self.DEFAULT_FONT.render(text, True, guide_text_color)
                guide_text_rect = guide_text.get_rect(center=(self.SCREEN.get_width() // 2,
                                                              self.guide_y + self.guide_height // 2 - lines_height // 2 + line_height * i))
                self.SCREEN.blit(guide_text, guide_text_rect)

    def minimax(self, current_map: typing.List[typing.List], main_team: TeamType, current_team: TeamType,
                depth: int, skip_if_destroyed_figures=False, iteration=0) -> typing.Tuple[int, Cell or None]:

        print(f'Start iteration {iteration}')
        print(f'Depth {depth}')
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

        print(f'Moves {len(all_moves)}')

        best_move = None
        print('Main team', main_team, '; Current team: ', current_team)
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
                evaluation, _ = self.minimax(new_board, main_team, current_team, depth - 1, skip_if_destroyed_figures,
                                             iteration=iteration + 1)
                print('Minimax returned evaluation', evaluation)
                evaluation += len(move.destroy_figures)
                print('Minmax returned evaluation with destroy figures factor', evaluation)
                print('Max eval', max_eval)
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move

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
                evaluation, _ = self.minimax(new_board, main_team, current_team, depth - 1, skip_if_destroyed_figures)
                evaluation -= len(move.destroy_figures)

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
            return min_eval, best_move

    def handle_event(self, event: Event):

        if self.show_guide:

            pass

        elif self.won:

            if self.repeat_button.is_clicked(event):
                self.restart_game()
            elif self.menu_button.is_clicked(event):
                self.set_as_current_page_by_page_name('menu')
            elif self.toptable_button.is_clicked(event):
                self.set_as_current_page_by_page_name('toptable')

        elif event.type == EventType.ENEMY_MOVE_EVENT and self.current_step == TeamType.BLACK_TEAM:

            pygame.time.set_timer(EventType.ENEMY_MOVE_EVENT, 0)

            self.make_enemy_move()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.back_button.is_clicked(event):
                self.restart_game()
                self.set_as_current_page_by_page_name('menu')

            elif self.help_button.is_clicked(event):

                self.show_guide = True

            elif self.current_step == TeamType.WHITE_TEAM:
                for i, piece in enumerate(self.pieces_by_current_teams_step):
                    if piece.is_clicked(event):
                        self.selected_piece = piece

                if self.selected_piece is not None:

                    for move in self.current_moves:
                        if move.is_clicked(event):

                            self.selected_piece.board_place_column = move.board_column
                            self.selected_piece.board_place_row = move.board_row

                            skip_next_team_change = False
                            for destroy_piece in move.destroy_figures:

                                destroy_piece.board_x = self.storage_left_x
                                destroy_piece.board_y = self.storage_left_y
                                destroy_piece.board_place_row = len(self.enemy_pieces_storage_by_current_teams_step)
                                destroy_piece.board_place_column = 0

                                if destroy_piece in self.enemy_pieces_by_current_teams_step:
                                    self.enemy_pieces_storage_by_current_teams_step.append(destroy_piece)
                                    self.enemy_pieces_by_current_teams_step.remove(destroy_piece)

                            if len(move.destroy_figures) > 0 and move.skip_next_team_change:
                                moves = self.get_moves(
                                    piece_column=self.selected_piece.board_place_column,
                                    piece_row=self.selected_piece.board_place_row,
                                    team_type=self.selected_piece.team_type,
                                    current_map=self.get_current_map_with_pieces(BoardCellType.ALL_CELL),
                                    only_with_destroyed_pieces=True
                                )

                                self.__current_moves = moves
                                if len(moves) > 0:
                                    skip_next_team_change = True

                            self.selected_piece = None

                            if not skip_next_team_change:
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

    @property
    def enemy_pieces_storage_by_current_teams_step(self) -> typing.List[Piece]:
        if self.current_step == TeamType.WHITE_TEAM:
            return self.black_team_pieces_storage
        elif self.current_step == TeamType.BLACK_TEAM:
            return self.white_team_pieces_storage

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

    def set_as_current_page(self):
        self.restart_game()
        print(self.current_difficulty_level)
        super().set_as_current_page()

    def restart_game(self):

        self.__selected_piece = None
        self.__current_moves = []
        self.current_difficulty_level = self.config.game_difficulty_level

        self.white_team_pieces = self.generate_pieces(TeamType.WHITE_TEAM, SpawnType.BOTTOM_SPAWN)
        self.white_team_pieces_storage: typing.List[Piece] = []
        self.black_team_pieces = self.generate_pieces(TeamType.BLACK_TEAM, SpawnType.TOP_SPAWN)
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

    def generate_pieces(self, team_type: TeamType, spawn_type: SpawnType) -> typing.List[Piece]:
        raise NotImplementedError

    def check_winner(self):
        current_map = self.get_current_map_with_pieces(BoardCellType.ALL_CELL)
        if self.current_step == TeamType.BLACK_TEAM:

            return any((
                len(self.white_team_pieces) == 0,
                any([p.board_place_row == self.num_blocks_vertical - 1 for p in self.black_team_pieces]),
                not any(
                    [len(self.get_moves(p.board_place_column, p.board_place_row, p.team_type, current_map)) > 0 for p in
                     self.white_team_pieces])
            ))
        elif self.current_step == TeamType.WHITE_TEAM:
            return any((
                len(self.black_team_pieces) == 0,
                any([p.board_place_row == 0 for p in self.white_team_pieces]),
                not any(
                    [len(self.get_moves(p.board_place_column, p.board_place_row, p.team_type, current_map)) > 0 for p in
                     self.black_team_pieces])
            ))
        else:
            return False

    def make_enemy_move(self):

        if self.current_step == TeamType.BLACK_TEAM:
            depth = 0

            if self.config.game_difficulty_level == LevelType.MEDIUM:
                depth = 2
            elif self.config.game_difficulty_level == LevelType.HARD:
                depth = 5

            if depth > 0:
                _, cell = self.minimax(
                    current_map=self.get_current_map_with_pieces(BoardCellType.ALL_CELL),
                    main_team=TeamType.BLACK_TEAM,
                    current_team=TeamType.BLACK_TEAM,
                    depth=depth,
                )
                print(cell)
            else:
                current_map = self.get_current_map_with_pieces(BoardCellType.ALL_CELL)

                cells = []
                shuffle(self.black_team_pieces)
                for piece in self.black_team_pieces:
                    moves = self.get_moves(piece.board_place_column, piece.board_place_row, piece.team_type,
                                           current_map, only_with_destroyed_pieces=True)
                    if len(moves) > 0:
                        break

                if len(cells) == 0:
                    for piece in self.black_team_pieces:
                        moves = self.get_moves(piece.board_place_column, piece.board_place_row, piece.team_type,
                                               current_map, only_with_destroyed_pieces=False)
                        if len(moves) > 0:
                            cells.append(choice(moves))
                            break

                if len(cells) > 0:
                    cell = cells[-1]
                else:
                    return None

            move: Cell = cell
            self.selected_piece = move.piece
            self.selected_piece.board_place_column = move.board_column
            self.selected_piece.board_place_row = move.board_row

            for destroy_piece in move.destroy_figures:
                self.enemy_pieces_by_current_teams_step.remove(destroy_piece)

                destroy_piece.board_x = self.storage_right_x
                destroy_piece.board_y = self.storage_right_y
                destroy_piece.board_place_row = len(self.white_team_pieces_storage)
                destroy_piece.board_place_column = 0

                self.white_team_pieces_storage.append(destroy_piece)

            skip_next_team_change = False
            if len(move.destroy_figures) > 0 and move.skip_next_team_change:
                moves = self.get_moves(
                    piece_column=self.selected_piece.board_place_column,
                    piece_row=self.selected_piece.board_place_row,
                    team_type=self.selected_piece.team_type,
                    current_map=self.get_current_map_with_pieces(BoardCellType.ALL_CELL),
                    only_with_destroyed_pieces=True
                )
                self.__current_moves = moves
                if len(moves) > 0:
                    skip_next_team_change = True
                    pygame.time.set_timer(EventType.ENEMY_MOVE_EVENT, 1000)

            self.selected_piece = None
            if not skip_next_team_change:
                self.change_step_side()

    def exit_event(self):
        pass
