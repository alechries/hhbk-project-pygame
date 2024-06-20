import pygame
import sys

from utils.config import Config
from utils.page import BasePage
from pages.auth import AuthPage
from pages.menu import MenuPage

pygame.init()

def start_app():
    config = Config()

    BasePage.initialize_pages()

    def go_to_menu():
        BasePage.set_as_current_page(MenuPage())

    auth_page = AuthPage(on_auth_success=go_to_menu)
    BasePage.set_as_current_page(auth_page)

    pygame.display.set_caption(config.app_name)
    clock = pygame.time.Clock()

    running = True
    CP: BasePage = BasePage.CURRENT_PAGE
    while running:
        current_pages_history_length = len(CP.PAGES_HISTORY)
        if CP.PAGE_COUNTER != current_pages_history_length:
            CP.PAGE_COUNTER = current_pages_history_length
            CP: BasePage = BasePage.CURRENT_PAGE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                CP.exit_event()
                running = False
            CP.handle_event(event)

        CP.draw()
        pygame.display.flip()
        clock.tick(config.frame_rate)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_app()
