from utils.config import Config


class BaseThema:

    def __init__(self):
        self.config = Config()

        self.background = self.config.WHITE
        self.border = self.config.BLACK
        self.text = self.config.BLACK
        self.white_team = self.config.WHITE
        self.black_team = self.config.BLACK
        self.table_part_0 = self.config.WHITE
        self.table_part_1 = self.config.BLACK
        self.notification_border = self.config.BLACK
        self.notification_background = self.config.WHITE
        self.notification_text = self.config.BLACK
