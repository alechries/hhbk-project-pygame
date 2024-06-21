
import pygame
import sys

from utils.config import Config
from utils.model import BaseModel
from utils.page import BasePage

pygame.init()


def start_app():
    config = Config()

    BaseModel.initialize_tables()
    BasePage.initialize_pages()

    pygame.display.set_caption(config.app_name)
    BasePage.set_as_current_page_by_page_name(config.start_page)

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

