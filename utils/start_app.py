
import pygame
import sys

from utils.config import Config
from utils.page import BasePage

pygame.init()


def start_app(page: BasePage):

    config = Config()
    pygame.display.set_caption(config.app_name)

    clock = pygame.time.Clock()
    page.set_as_current_page()

    running = True
    while running:
        CP: BasePage = page.CURRENT_PAGE
        current_pages_history_length = len(CP.PAGES_HISTORY)
        if CP.PAGE_COUNTER != current_pages_history_length:
            CP.PAGE_COUNTER = current_pages_history_length
            page = CP.CURRENT_PAGE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                page.exit_event()
                running = False
            page.handle_event(event)

        page.draw()
        pygame.display.flip()
        clock.tick(config.frame_rate)

    pygame.quit()
    sys.exit()
