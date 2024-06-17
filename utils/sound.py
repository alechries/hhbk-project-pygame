from pygame.mixer import Sound
from os import path

from utils.config import Config


class SoundManager:

    def __init__(self):
        self.config = Config()
        self.last_sound = None

    def play(self, file_path=''):
        file_path = path.join(self.config.sound_dir, file_path)
        if path.exists(file_path):
            sound = Sound(file_path)
            self.last_sound = sound
            sound.set_volume(self.config.sound_volume)
            sound.play()

    def stop(self):
        if self.last_sound is not None:
            self.last_sound.stop()
