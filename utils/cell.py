import typing

import pygame
from pygame.event import Event


class Cell:
    
    def __init__(self, board_row, board_column, board_x, board_y, block_width, block_height):
        self.rect = pygame.Rect(board_x + board_column * block_width, board_y + board_row * block_height, block_width, block_height)
        self.board_x = board_x
        self.board_y = board_y
        self.board_row = board_row
        self.board_column = board_column

    def is_clicked(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False

