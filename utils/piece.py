import pygame
from pygame.event import Event


class Piece:

    IMAGE = pygame.image.load('assets/images/black_piece.png')

    def __init__(self, x, y, width, height, board_place_row=0, board_place_column=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.board_place_row = board_place_row
        self.board_place_column = board_place_column

        self.selected = False

    def draw(self, screen):
        piece_image = pygame.transform.scale(Piece.IMAGE, (self.width, self.height))
        screen.blit(piece_image, (self.x, self.y))

    def is_clicked(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False
