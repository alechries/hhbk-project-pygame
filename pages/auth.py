from utils.page import BasePage
from pygame.event import Event
from pygame.mixer import Sound

from utils.sound import SoundManager
from utils.start_app import start_app
from time import sleep


class AuthPage(BasePage):

    def __init__(self):
        super().__init__()

        sound = SoundManager()
        sound.play('auth/app_shutdown.mp3')

    def draw(self):
        text = self.DEFAULT_FONT.render('Auth page', True, self.thema.text)
        text_rect = text.get_rect(center=(self.SCREEN.get_width() // 2, self.SCREEN.get_height() // 2))
        self.SCREEN.blit(text, text_rect)

    def handle_event(self, event: Event):
        pass

    def exit_event(self):
        sound = SoundManager()
        sound.play('auth/app_shutdown.mp3')
        sleep(1)


if __name__ == "__main__":
    start_app(AuthPage())
