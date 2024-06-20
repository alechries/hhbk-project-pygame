
import pygame
import sys
import inspect
import importlib
from pathlib import Path

from utils.board import BaseBoardPage
from utils.config import Config
from utils.model import BaseModel
from utils.page import BasePage

pygame.init()


def pages_initialize():

    models_path = Path(__file__).parent / "pages"
    print(models_path)

    for file in models_path.glob("*.py"):
        if file.name == "__init__.py":
            continue

        module_name = f"pages.{file.stem}"
        module = importlib.import_module(module_name)

        for name, obj in inspect.getmembers(module, inspect.isclass):

            if issubclass(obj, BasePage) and obj is not BasePage and obj is not BaseBoardPage:
                instance = obj()
                if instance.page_name:
                    BasePage.PAGES[instance.page_name] = instance


def start_app():
    config = Config()

    BaseModel.initialize_tables()
    pages_initialize()

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

