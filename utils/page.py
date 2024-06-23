import os
import typing

import pygame
from pygame.surface import Surface
from pygame.display import set_mode
from pygame.event import Event
from pygame.font import SysFont, Font
from utils.config import Config
from utils.thema import BaseTheme
import inspect
import importlib
from pathlib import Path
from os import path

config = Config()
programIcon = pygame.image.load(os.path.join(config.images_dir, 'logo.png'))
pygame.display.set_icon(programIcon)
pygame.display.set_caption(config.app_name)
screen: Surface = set_mode((config.screen_width, config.screen_height))


class BasePage:
    SCREEN = screen
    CURRENT_PAGE = None
    PAGES_HISTORY = []
    PAGES = {}
    PAGE_COUNTER = 0

    def __init__(self, thema=BaseTheme()):
        self.page_name = ''
        self.thema = thema
        self.config = Config()
        self.DEFAULT_FONT = SysFont('Default font', 20)
        self.MEDIUM_FONT = SysFont('Medium font', 40)
        self.BIG_FONT = SysFont('Big font', 50)
        self.SCREEN.fill(self.thema.background)

        background_image = pygame.image.load(path.join(self.config.images_dir, 'background.png')).convert()
        self.background_image = pygame.transform.smoothscale(background_image, self.SCREEN.get_size())

    @staticmethod
    def initialize_pages():
        models_path = Path(__file__).parent.parent / "pages"
        for file in models_path.glob("*.py"):
            if file.name == "__init__.py":
                continue
            module_name = f"pages.{file.stem}"
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BasePage) and obj is not BasePage:
                    instance = obj()
                    if instance.page_name:
                        BasePage.PAGES[instance.page_name] = instance

    def set_as_current_page(self):
        BasePage.PAGES_HISTORY.append(BasePage.CURRENT_PAGE)
        BasePage.CURRENT_PAGE = self

    @staticmethod
    def set_as_current_page_by_page_name(page_name=''):
        if page_name:
            if page_name in BasePage.PAGES.keys():
                BasePage.PAGES[page_name].set_as_current_page()

    @staticmethod
    def return_to_last_page():
        if len(BasePage.PAGES_HISTORY) > 0:
            BasePage.PAGES_HISTORY[-1].set_as_current_page()

    def draw(self):
        self.SCREEN.blit(self.background_image, (0, 0))

    def handle_event(self, event: Event):
        pass

    def exit_event(self):
        pass
