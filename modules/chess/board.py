from utils.page import BasePage
from pygame.event import Event

from utils.start_app import start_app


class ChessBoardPage(BasePage):

    def __init__(self):
        super().__init__()

    def draw(self):
        text = self.DEFAULT_FONT.render('"Bauernschach" page', True, self.thema.text)
        text_rect = text.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2))
        self.SCREEN.blit(text, text_rect)

    def handle_event(self, event: Event):
        pass

    def exit_event(self):
        pass


if __name__ == "__main__":
    start_app(ChessBoardPage())
