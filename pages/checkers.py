from utils.board import BaseBoardPage
from utils.page import BasePage
from pygame.event import Event

from utils.types import GameType


class CheckersBoardPage(BaseBoardPage):

    def __init__(self):
        super().__init__(GameType.CHECKERS_GAME)
        self.page_name = 'checkers'

    def draw(self):
        super().draw()

        text = self.DEFAULT_FONT.render('"Bauernschach" page', True, self.thema.text)
        text_rect = text.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2))
        self.SCREEN.blit(text, text_rect)

    def handle_event(self, event: Event):
        pass

    def exit_event(self):
        pass
