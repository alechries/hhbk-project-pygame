import typing
import pygame
from utils.page import BasePage
from pygame.event import Event
from utils.button import Button



class MenuPage(BasePage):

    def __init__(self):
        super().__init__()
        self.page_name = 'menu'
        self.chess_game_button = Button(300, 240, 200, 30, "Chess", self.thema.text, background=self.thema.background)
        self.checkers_game_button = Button(300, 280, 200, 30, "Checkers", self.thema.text, background=self.thema.background)
        self.buttons: typing.List[Button] = [
            self.chess_game_button, self.checkers_game_button
        ]

    def draw(self):
        super().draw()

        for button in self.buttons:
            button.draw(self.SCREEN)

    def handle_event(self, event: Event):
        if self.chess_game_button.is_clicked(event):
            print("Chess button was clicked")
            self.load_chess_game()
        elif self.checkers_game_button.is_clicked(event):
            print("Checkers button was clicked")
            self.load_checkers_game()

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
        self.set_as_current_page_by_page_name('auth')
