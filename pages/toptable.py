from utils.button import Button
from utils.page import BasePage
from pygame.event import Event
from utils.config import Config
from models.user import UserModel
import pygame
import sys

from utils.types import GameType


class TopTablePage(BasePage):

    def __init__(self):
        super().__init__()
        self.user_list = UserModel().get_data()
        self.game_type: GameType = GameType.UNKNOWN
        self.page_name = 'toptable'
        self.difficulty_easy_button = Button(5, 20, 120, 30, "Easy", self.thema.text, background=self.thema.background)
        self.difficulty_medium_button = Button(130, 20, 120, 30, "Medium", self.thema.text,
                                               background=self.thema.background)
        self.difficulty_hard_button = Button(255, 20, 120, 30, "Hard", self.thema.text,
                                             background=self.thema.background)
        self.gamemode_chess_button = Button(545, 20, 120, 30, "Chess", self.thema.text,
                                            background=self.thema.background)
        self.gamemode_checkers_button = Button(670, 20, 120, 30, "Checkers", self.thema.text,
                                               background=self.thema.background)

    def draw(self):

        MARGIN = 5
        COLUMNS = 4
        ROWS = 7
        PADDING_TABLE_PERCENT = 5
        PADDING_TABLE_WIDTH = self.SCREEN.get_width() // 100 * PADDING_TABLE_PERCENT
        PADDING_TABLE_HEIGHT = PADDING_TABLE_WIDTH
        CELL_WIDTH = (self.SCREEN.get_width() - PADDING_TABLE_WIDTH * 2 - (COLUMNS - 1) * MARGIN) // COLUMNS
        CELL_HEIGHT = (self.SCREEN.get_height() - PADDING_TABLE_HEIGHT * 2 - (ROWS - 1) * MARGIN) // ROWS

        pygame.display.set_caption('Scoreboard')

        font = pygame.font.SysFont(None, 30)

        table_data = [['' for _ in range(COLUMNS)] for _ in range(ROWS)]
        table_data[1] = ['#', 'Username', 'Wins', 'Defeats']

        self.SCREEN.fill(Config.WHITE)

        self.difficulty_easy_button.draw(self.SCREEN)
        self.difficulty_medium_button.draw(self.SCREEN)
        self.difficulty_hard_button.draw(self.SCREEN)
        self.gamemode_chess_button.draw(self.SCREEN)
        self.gamemode_checkers_button.draw(self.SCREEN)
        for row in range(ROWS):
            for col in range(COLUMNS):
                if row > 0:
                    x = PADDING_TABLE_WIDTH + MARGIN + col * (CELL_WIDTH + MARGIN)
                    y = PADDING_TABLE_HEIGHT + MARGIN + row * (CELL_HEIGHT + MARGIN)

                    pygame.draw.rect(self.SCREEN, Config.GRAY, (x, y, CELL_WIDTH, CELL_HEIGHT))

                    text_surface = font.render(table_data[row][col], True, Config.BLACK)
                    text_rect = text_surface.get_rect(center=(x + CELL_WIDTH // 2, y + CELL_HEIGHT // 2))
                    self.SCREEN.blit(text_surface, text_rect)

    def handle_event(self, event: Event):
        if self.difficulty_easy_button.is_clicked(event):
            self.difficulty_easy_button.color = Config.BLUE
            print("test")

    def exit_event(self):
        pass
