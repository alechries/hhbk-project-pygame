from utils.config import Config


class BaseTheme:

    def __init__(self):
        self.config = Config()
        self.background = self.config.WHITE
        self.border = self.config.GRAY
        self.text = self.config.BLACK
        self.button = self.config.GREEN
        self.button_pressed = self.config.ORANGE_RED
        self.white_team = self.config.WHITE
        self.black_team = self.config.BLACK
        self.table_part_0 = self.config.WHITE
        self.table_part_1 = self.config.GRAY
        self.notification_border = self.config.BLACK
        self.notification_background = self.config.WHITE
        self.notification_text = self.config.BLACK
        self.winner_glow = self.config.GREEN_TRANSPARENT
        self.winner_notification_text = self.config.BLACK
        self.winner_notification_background = self.config.DARK_GREEN
        self.loser_glow = self.config.RED_TRANSPARENT
        self.loser_notification_text = self.config.WHITE
        self.loser_notification_background = self.config.DARK_RED
        self.guide_glow = self.config.BLUE_TRANSPARENT
        self.button_text = self.config.BLACK
        self.button_background = self.config.WHITE
        self.scoreboard_cells = self.config.LIGHT_GRAY
        self.close_button = self.config.RED
        self.button_yes = self.config.GREEN
        self.button_no = self.config.RED
        self.score_wins = self.config.DARKER_GREEN
        self.score_defeats = self.config.RED
        self.logout_button = self.config.RED
        self.start_game_button = self.config.FOREST_GREEN

