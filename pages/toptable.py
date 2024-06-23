from utils.button import Button
from utils.page import BasePage
from pygame.event import Event
from utils.config import Config
from models.user import UserModel
import pygame
import sys

from utils.types import GameType, LevelType


class TopTablePage(BasePage):

    def __init__(self):
        super().__init__()
        self.MARGIN = 5
        self.COLUMNS = 4
        self.ROWS = 13
        self.PADDING_TABLE_PERCENT = 5
        self.PADDING_TABLE_WIDTH = self.SCREEN.get_width() // 100 * self.PADDING_TABLE_PERCENT
        self.PADDING_TABLE_HEIGHT = self.PADDING_TABLE_WIDTH
        self.CELL_WIDTH = (self.SCREEN.get_width() - self.PADDING_TABLE_WIDTH * 2 - (self.COLUMNS - 1) * self.MARGIN) // self.COLUMNS
        self.CELL_HEIGHT = (self.SCREEN.get_height() - self.PADDING_TABLE_HEIGHT * 2 - (self.ROWS - 1) * self.MARGIN) // self.ROWS
        self.user_data_list = UserModel().get_data()
        self.game_type: GameType = GameType.CHESS_GAME
        self.level_type: LevelType = LevelType.EASY
        self.page_name = 'toptable'
        self.difficulty_easy_button = Button(self.PADDING_TABLE_WIDTH + 5, self.PADDING_TABLE_HEIGHT, 120, 30, "Easy", self.thema.text, background=self.thema.background)
        self.difficulty_medium_button = Button(self.PADDING_TABLE_WIDTH + 130, self.PADDING_TABLE_HEIGHT, 120, 30, "Medium", self.thema.text,
                                               background=self.thema.background)
        self.difficulty_hard_button = Button(self.PADDING_TABLE_WIDTH + 255, self.PADDING_TABLE_HEIGHT, 120, 30, "Hard", self.thema.text,
                                             background=self.thema.background)
        self.gamemode_chess_button = Button(self.SCREEN.get_width() - self.PADDING_TABLE_WIDTH -245, self.PADDING_TABLE_HEIGHT, 120, 30, "Chess", self.thema.text,
                                            background=self.thema.background)
        self.gamemode_checkers_button = Button(self.SCREEN.get_width() - self.PADDING_TABLE_WIDTH -120, self.PADDING_TABLE_HEIGHT, 120, 30, "Checkers", self.thema.text,
                                               background=self.thema.background)
        self.menu_button = Button(self.SCREEN.get_width() // 2 - 60, self.SCREEN.get_height() - self.PADDING_TABLE_HEIGHT * 2 + self.MARGIN, 120, 30, "Back", self.thema.text, background=self.thema.background)

        self.user_list = []
        for user_data in self.user_data_list:
            user = UserModel()
            user.init_by_data(user_data)
            self.user_list.append(user)

    def draw(self):
        super().draw()

        pygame.display.set_caption('Scoreboard')

        font = pygame.font.SysFont(None, 30)

        table_data = [['' for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        table_data[1] = ['#', 'Username', 'Wins', 'Defeats']
        table_data_index = 2
        scoreboard_position = 1
        scoreboard_list = []
        if self.game_type == GameType.CHESS_GAME:
            if self.level_type == LevelType.EASY:
                scoreboard_list = sorted(self.user_list, key=lambda x: x._chess_wins_easy, reverse=True)[:10]
                for score in scoreboard_list:
                    table_data[table_data_index] = [str(scoreboard_position), str(score._username), str(score._chess_wins_easy), str(score._chess_defeats_easy)]
                    table_data_index += 1
                    scoreboard_position += 1
            elif self.level_type == LevelType.MEDIUM:
                scoreboard_list = sorted(self.user_list, key=lambda x: x._chess_wins_medium, reverse=True)[:10]
                for score in scoreboard_list:
                    table_data[table_data_index] = [str(scoreboard_position), str(score._username), str(score._chess_wins_medium), str(score._chess_defeats_medium)]
                    table_data_index += 1
                    scoreboard_position += 1
            elif self.level_type == LevelType.HARD:
                scoreboard_list = sorted(self.user_list, key=lambda x: x._chess_wins_hard, reverse=True)[:10]
                for score in scoreboard_list:
                    table_data[table_data_index] = [str(scoreboard_position), str(score._username), str(score._chess_wins_hard), str(score._chess_defeats_hard)]
                    table_data_index += 1
                    scoreboard_position += 1
        elif self.game_type == GameType.CHECKERS_GAME:
            if self.level_type == LevelType.EASY:
                scoreboard_list = sorted(self.user_list, key=lambda x: x._checkers_wins_easy, reverse=True)[:10]
                for score in scoreboard_list:
                    table_data[table_data_index] = [str(scoreboard_position), str(score._username), str(score._checkers_wins_easy), str(score._checkers_defeats_easy)]
                    table_data_index += 1
                    scoreboard_position += 1
            elif self.level_type == LevelType.MEDIUM:
                scoreboard_list = sorted(self.user_list, key=lambda x: x._checkers_wins_medium, reverse=True)[:10]
                for score in scoreboard_list:
                    table_data[table_data_index] = [str(scoreboard_position), str(score._username), str(score._checkers_wins_medium), str(score._checkers_defeats_medium)]
                    table_data_index += 1
                    scoreboard_position += 1
            elif self.level_type == LevelType.HARD:
                scoreboard_list = sorted(self.user_list, key=lambda x: x._checkers_wins_hard, reverse=True)[:10]
                for score in scoreboard_list:
                    table_data[table_data_index] = [str(scoreboard_position), str(score._username), str(score._checkers_wins_hard), str(score._checkers_defeats_hard)]
                    table_data_index += 1
                    scoreboard_position += 1

        if self.game_type == GameType.CHESS_GAME:
            self.gamemode_chess_button.color = self.thema.button_pressed
            self.gamemode_checkers_button.color = self.thema.text
        elif self.game_type == GameType.CHECKERS_GAME:
            self.gamemode_chess_button.color = self.thema.text
            self.gamemode_checkers_button.color = self.thema.button_pressed

        if self.level_type == LevelType.EASY:
            self.difficulty_easy_button.color = self.thema.button_pressed
            self.difficulty_medium_button.color = self.thema.text
            self.difficulty_hard_button.color = self.thema.text
        elif self.level_type == LevelType.MEDIUM:
            self.difficulty_easy_button.color = self.thema.text
            self.difficulty_medium_button.color = self.thema.button_pressed
            self.difficulty_hard_button.color = self.thema.text
        elif self.level_type == LevelType.HARD:
            self.difficulty_easy_button.color = self.thema.text
            self.difficulty_medium_button.color = self.thema.text
            self.difficulty_hard_button.color = self.thema.button_pressed

        self.difficulty_easy_button.draw(self.SCREEN)
        self.difficulty_medium_button.draw(self.SCREEN)
        self.difficulty_hard_button.draw(self.SCREEN)
        self.gamemode_chess_button.draw(self.SCREEN)
        self.gamemode_checkers_button.draw(self.SCREEN)
        self.menu_button.draw(self.SCREEN)

        for row in range(self.ROWS - 1):
            for col in range(self.COLUMNS):
                if row > 0:
                    x = self.PADDING_TABLE_WIDTH + self.MARGIN + col * (self.CELL_WIDTH + self.MARGIN)
                    y = self.PADDING_TABLE_HEIGHT + self.MARGIN + row * (self.CELL_HEIGHT + self.MARGIN)

                    pygame.draw.rect(self.SCREEN, self.thema.text, (x, y, self.CELL_WIDTH, self.CELL_HEIGHT), border_radius=3)
                    pygame.draw.rect(self.SCREEN, self.thema.scoreboard_cells,
                                     (x + 2, y + 2, self.CELL_WIDTH - 4, self.CELL_HEIGHT - 4), border_radius=3)

                    text_surface = font.render(table_data[row][col], True, self.thema.text)
                    text_rect = text_surface.get_rect(center=(x + self.CELL_WIDTH // 2, y + self.CELL_HEIGHT // 2))
                    self.SCREEN.blit(text_surface, text_rect)

    def handle_event(self, event: Event):
        if self.difficulty_easy_button.is_clicked(event):
            self.level_type = LevelType.EASY
        if self.difficulty_medium_button.is_clicked(event):
            self.level_type = LevelType.MEDIUM
        if self.difficulty_hard_button.is_clicked(event):
            self.level_type = LevelType.HARD
        if self.gamemode_checkers_button.is_clicked(event):
            self.game_type = GameType.CHECKERS_GAME
        if self.gamemode_chess_button.is_clicked(event):
            self.game_type = GameType.CHESS_GAME
        if self.menu_button.is_clicked(event):
            self.set_as_current_page_by_page_name("menu")


    def exit_event(self):
        pass


