from utils.page import BasePage
from pygame.event import Event
from pygame.mixer import Sound

from utils.sound import SoundManager
from time import sleep


class AuthPage(BasePage):

    def __init__(self):
        super().__init__()
        self.page_name = 'auth'

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
