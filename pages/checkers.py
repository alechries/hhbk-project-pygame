import typing

from utils.board import BaseBoardPage
from utils.page import BasePage
from pygame.event import Event
import pygame

from utils.piece import Piece


class CheckersBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__()
        self.page_name = 'checkers'
        self.turn_step = 0
        self.pieces_map = [
            ['P', 'P', 'P', 'P', 'P', 'P',],
            ['P', 'P', 'P', 'P', 'P', 'P',],
            ['', '', '', '', '', '',],
            ['', '', '', '', '', '',],
            ['P', 'P', 'P', 'P', 'P', 'P',],
            ['P', 'P', 'P', 'P', 'P', 'P',],
        ]
        self.active_pieces: typing.List[Piece] = []

        self.num_blocks_horizontal = 6
        self.num_blocks_vertical = self.num_blocks_horizontal
        self.block_border_width = 0
        self.outer_border_width = 2

        self.w = self.SCREEN.get_width()
        self.h = self.SCREEN.get_height()

        self.smaller_side_size = self.w if self.w < self.h else self.h
        self.smaller_num_blocks = self.num_blocks_vertical if self.num_blocks_vertical < self.num_blocks_horizontal else self.num_blocks_horizontal

        self.block_size = (self.smaller_side_size / 100 * self.config.board_size_percent) / self.smaller_num_blocks
        self.piece_size = self.block_size / 100 * 90

        self.start_x = (self.SCREEN.get_width() - (self.num_blocks_horizontal * self.block_size)) // 2
        self.start_y = (self.SCREEN.get_height() - (self.num_blocks_vertical * self.block_size)) // 2

        for row in range(self.num_blocks_vertical):
            for column in range(self.num_blocks_horizontal):
                x = self.start_x + (column * self.block_size)
                y = self.start_y + (row * self.block_size)

                if self.pieces_map[row][column]:
                    piece = Piece(x, y, self.block_size, self.block_size, row, column)
                    self.active_pieces.append(piece)

    def draw(self):

        # BOARD GENERATING

        for row in range(self.num_blocks_vertical):
            for column in range(self.num_blocks_horizontal):
                x = self.start_x + (column * self.block_size)
                y = self.start_y + (row * self.block_size)
                color = self.thema.table_part_0 if (row + column) % 2 == 0 else self.thema.table_part_1
                pygame.draw.rect(self.SCREEN, color, [x, y, self.block_size, self.block_size])
                if self.block_border_width > 0:
                    pygame.draw.rect(self.SCREEN, self.thema.border, [x, y, self.block_size, self.block_size], self.block_border_width)

        if self.outer_border_width > 0:
            outer_rect = [
                self.start_x - self.block_border_width // 2,
                self.start_y - self.block_border_width // 2,
                self.num_blocks_horizontal * self.block_size + self.block_border_width,
                self.num_blocks_vertical * self.block_size + self.block_border_width
            ]
            pygame.draw.rect(self.SCREEN, self.thema.border, outer_rect, self.outer_border_width)

        # PIECES GENERATING

        for piece in self.active_pieces:
            piece.draw(self.SCREEN)
            if piece.selected:
                pygame.draw.rect(self.SCREEN, self.config.RED, [piece.x, piece.y, piece.width, piece.height], 3)

                # SEARCH STEP

                steps = []
                for step_x, step_y in [
                    (piece.board_place_column - 1, piece.board_place_row - 1),
                    (piece.board_place_column + 1, piece.board_place_row + 1),
                    (piece.board_place_column - 1, piece.board_place_row + 1),
                    (piece.board_place_column + 1, piece.board_place_row - 1),
                ]:
                    if 0 <= step_x < self.num_blocks_horizontal and 0 <= step_y < self.num_blocks_vertical:
                        if not any([piece_on_way.board_place_column == step_x and piece_on_way.board_place_row == step_y for piece_on_way in self.active_pieces]):
                            steps.append((step_x, step_y))

                for step_x, step_y in steps:
                    x = self.start_x + (step_x * self.block_size)
                    y = self.start_y + (step_y * self.block_size)
                    pygame.draw.rect(self.SCREEN, self.config.RED, [x, y, self.block_size, self.block_size], 3)

    def handle_event(self, event: Event):

        for i, piece in enumerate(self.active_pieces):
            if piece.is_clicked(event):
                if piece.selected:
                    self.active_pieces.pop(i)
                else:
                    for j, active_piece in enumerate(self.active_pieces):
                        if active_piece.selected:
                            active_piece.selected = False
                    piece.selected = True

    def exit_event(self):
        pass
