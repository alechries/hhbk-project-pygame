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
        self.buttons: typing.List[Button] = [
            Button(100, 100, 100, 20, "Welcome!", self.thema.text, background=self.thema.background)
        ]
    def draw(self):
        for button in self.buttons:
            button.draw(self.SCREEN)
    def handle_event(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Button was clicked")
            self.log_out_button_handler()
    def exit_event(self):
        print("Hello, Alex!")

    def log_out_button_handler(self):
        authPage = AuthPage()
        authPage.set_as_current_page()

if __name__ == "__main__":
    start_app(MenuPage())
