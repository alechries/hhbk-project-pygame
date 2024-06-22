import typing

import pygame
from pygame.event import Event

from utils.piece import Piece


class Cell:
    
    def __init__(self, board_row, board_column, board_x=0, board_y=0, block_width=0, block_height=0,
                 destroy_figures=None, piece: Piece = None, skip_next_team_change=False):

        self.rect = pygame.Rect(board_x + board_column * block_width, board_y + board_row * block_height, block_width, block_height)
        self.board_x = board_x
        self.board_y = board_y
        self.board_row = board_row
        self.board_column = board_column
        self.piece = piece
        if destroy_figures is None:
            destroy_figures: typing.List[Piece] = []
        self.destroy_figures = destroy_figures
        self.skip_next_team_change = skip_next_team_change

    def is_clicked(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False

