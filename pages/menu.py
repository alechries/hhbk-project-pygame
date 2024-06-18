import typing
import pygame
from utils.page import BasePage
from pygame.event import Event
from utils.button import Button
import pygame_menu
from utils.start_app import start_app
from pages.auth import AuthPage


class MenuPage(BasePage):

    def __init__(self):
        super().__init__()
        self.page_name = 'menu'

        self.choose_game_button = Button(300, 200, 200, 30, "Choose Game", self.thema.text, background=self.thema.background)
        self.chess_game_button = Button(300, 220, 200, 30, "Chess", self.thema.text, background=self.thema.background)
        self.checkers_game_button = Button(300, 300, 200, 30, "Dame", self.thema.text, background=self.thema.background)
        self.buttons: typing.List[Button] = [
            self.choose_game_button, self.chess_game_button, self.checkers_game_button
        ]

    def draw(self):
        for button in self.buttons:
            button.draw(self.SCREEN)

    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.choose_game_button.is_clicked(event.pos):
                print("Button was clicked")
                self.log_out_button_handler()

    def exit_event(self):
        print("Hello, Alex!")

    def log_out_button_handler(self):
        self.set_as_current_page_by_page_name('auth')


if __name__ == "__main__":
    start_app(MenuPage())
