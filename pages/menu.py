import typing
import pygame

from models.user import UserModel
from utils.config import Config
from utils.page import BasePage
from pygame.event import Event
from utils.button import Button
from utils.types import GameType, LevelType


class MenuPage(BasePage):

    def __init__(self):
        super().__init__()

        self.button_width = 300
        self.button_height = 50
        self.buttons_margin = 10
        self.buttons_x_margin = 3
        self.difficulty_button_width = self.button_width // 3 - (2 * self.buttons_x_margin // 3)
        self.button_x = self.SCREEN.get_width() // 2 - self.button_width // 2
        self.difficulty_button_x = self.SCREEN.get_width() // 2 - self.button_width // 2
        self.button_y = self.SCREEN.get_height() // 2.5 - (self.button_height * 1.5)

        self.game_type: GameType = GameType.UNKNOWN
        self.level_type: LevelType = LevelType.EASY

        self.page_name = 'menu'
        self.chess_game_button = Button(self.button_x, self.button_y, self.button_width, self.button_height, "Bauernschach",
                                        self.thema.text,
                                        background=self.thema.background)
        self.button_y += self.button_height + self.buttons_margin
        self.checkers_game_button = Button(self.button_x, self.button_y, self.button_width, self.button_height,
                                           "Dame", self.thema.text,
                                           background=self.thema.background)
        self.button_y += self.button_height + self.buttons_margin
        self.difficulty_easy_button = Button(self.difficulty_button_x, self.button_y, self.difficulty_button_width,
                                             self.button_height,
                                             "Easy", self.thema.text, background=self.thema.background)
        self.difficulty_button_x += self.difficulty_button_width + self.buttons_x_margin
        self.difficulty_medium_button = Button(self.difficulty_button_x, self.button_y, self.difficulty_button_width,
                                               self.button_height,
                                               "Medium", self.thema.text, background=self.thema.background)
        self.difficulty_button_x += self.difficulty_button_width + self.buttons_x_margin
        self.difficulty_hard_button = Button(self.difficulty_button_x, self.button_y, self.difficulty_button_width,
                                             self.button_height,
                                             "Hard", self.thema.text, background=self.thema.background)
        self.button_y += self.button_height + self.buttons_margin
        self.start_game_button = Button(self.button_x, self.button_y, self.button_width, self.button_height,
                                        "Spiel starten", self.thema.text,
                                        background=self.thema.background)
        self.log_out_button = Button(self.SCREEN.get_width() - self.difficulty_button_width - self.buttons_margin,
                                     self.buttons_margin, self.difficulty_button_width, self.button_height, "Logout",
                                     self.thema.text, background=self.thema.background)

        self.buttons: typing.List[Button] = [
            self.chess_game_button, self.checkers_game_button, self.difficulty_easy_button,
            self.difficulty_medium_button, self.difficulty_hard_button, self.start_game_button, self.log_out_button
        ]

    def draw(self):
        super().draw()

        if self.game_type == GameType.CHESS_GAME:
            self.chess_game_button.color = self.thema.button_pressed
            self.checkers_game_button.color = self.thema.text
        elif self.game_type == GameType.CHECKERS_GAME:
            self.chess_game_button.color = self.thema.text
            self.checkers_game_button.color = self.thema.button_pressed

        if self.level_type == LevelType.EASY:
            self.difficulty_easy_button.color = self.thema.button_pressed
            self.difficulty_medium_button.color = self.thema.text
            self.difficulty_hard_button.color = self.thema.text
        elif self.level_type == LevelType.MEDIUM:
            self.difficulty_easy_button.color = self.thema.text
            self.difficulty_medium_button.color = self.thema.button_pressed
            self.difficulty_hard_button.color = self.thema.text
        elif self.level_type == LevelType.HARD:
            self.difficulty_easy_button.color = self.thema.text
            self.difficulty_medium_button.color = self.thema.text
            self.difficulty_hard_button.color = self.thema.button_pressed

        pygame.draw.rect(self.SCREEN, self.thema.text, (self.button_x - 10, self.chess_game_button.rect.y - 10,
                                                        self.button_width + 20,
                                                        self.button_height * 4 + self.buttons_margin * 3 + 20),
                         border_radius=10)
        pygame.draw.rect(self.SCREEN, self.thema.scoreboard_cells,
                         (self.button_x - 5, self.chess_game_button.rect.y - 5,
                          self.button_width + 10,
                          self.button_height * 4 + self.buttons_margin * 3 + 10),
                         border_radius=10)

        for button in self.buttons:
            button.draw(self.SCREEN)

    def handle_event(self, event: Event):
        if self.chess_game_button.is_clicked(event):
            self.game_type = GameType.CHESS_GAME
        if self.checkers_game_button.is_clicked(event):
            self.game_type = GameType.CHECKERS_GAME
        if self.difficulty_easy_button.is_clicked(event):
            self.level_type = LevelType.EASY
            self.config.game_difficulty_level = LevelType.EASY
        if self.difficulty_medium_button.is_clicked(event):
            self.level_type = LevelType.MEDIUM
            self.config.game_difficulty_level = LevelType.MEDIUM
        if self.difficulty_hard_button.is_clicked(event):
            self.level_type = LevelType.HARD
            self.config.game_difficulty_level = LevelType.HARD
        if self.start_game_button.is_clicked(event) and self.level_type != LevelType.UNKNOWN:
            if self.game_type == GameType.CHESS_GAME:
                self.load_chess_game()
            elif self.game_type == GameType.CHECKERS_GAME:
                self.load_checkers_game()
        if self.log_out_button.is_clicked(event):
            self.log_out_button_handler()

    def choose_game_button_handler(self):
        print("Choose Game button handler")

    def load_chess_game(self):
        print("Loading Chess game...")
        self.set_as_current_page_by_page_name('chess')

    def load_checkers_game(self):
        print("Loading Checkers game...")
        self.set_as_current_page_by_page_name('checkers')

    def exit_event(self):
        print("Hello, Alex!")

    def log_out_button_handler(self):
        if self.current_user is not None:
            user: UserModel = self.current_user
            user.logged_in = False
            self.set_user_global(None)
        self.set_as_current_page_by_page_name('auth')
