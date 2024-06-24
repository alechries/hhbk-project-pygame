import os.path
import pygame
import sys
import inspect
import importlib
from pathlib import Path

from models.user import UserModel
from utils.board import BaseBoardPage
from utils.config import Config
from utils.model import BaseModel
from utils.page import BasePage
from os import path

from pages.auth import AuthPage  # Import the AuthPage class

pygame.init()


def pages_initialize():
    models_path = Path(__file__).parent / "pages"

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

    # Initialize the AuthPage with the on_auth_success callback
    def on_auth_success(user: UserModel):
        BasePage.set_user_global(user)
        BasePage.set_as_current_page_by_page_name('menu')
    auth_page = AuthPage(on_auth_success=on_auth_success)
    BasePage.PAGES[auth_page.page_name] = auth_page


def start_app():
    config = Config()

    BaseModel.initialize_tables()
    pages_initialize()

    BasePage.set_as_current_page_by_page_name(config.start_page)

    clock = pygame.time.Clock()

    running = True
    CP: BasePage = BasePage.CURRENT_PAGE
    while running:
        current_pages_history_length = len(CP.PAGES_HISTORY)
        if CP.PAGE_COUNTER != current_pages_history_length:
            CP.PAGE_COUNTER = current_pages_history_length
            CP: BasePage = BasePage.CURRENT_PAGE

        events = pygame.event.get()
        for event in events:
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
