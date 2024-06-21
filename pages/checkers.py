from utils.board import BaseBoardPage
from utils.page import BasePage
from pygame.event import Event

from utils.types import GameType


class CheckersBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__(GameType.CHECKERS_GAME)
        self.page_name = 'checkers'

    def handle_event(self, event: Event):
        pass

    def exit_event(self):
        pass
