import pygame
from utils.page import BasePage
from pygame.event import Event
from utils.sound import SoundManager
from models.user import UserModel
from time import sleep
from utils.thema import BaseTheme  # Import the BaseTheme class


class AuthPage(BasePage):
    def __init__(self, on_auth_success=None):
        super().__init__()
        self.page_name = 'auth'
        # self.sound = SoundManager()
        # self.sound.play('assets/sounds/auth/loaded.mp3')
        self.user_model = UserModel()
        # self.user_model.initialize_table()
        self.username = ''
        self.password = ''
        self.active_input = 'username'
        self.on_auth_success = on_auth_success
        self.message = ''
        self.show_confirmation = False
        self.confirmation_message = ''

        self.thema = BaseTheme()  # Create an instance of BaseTheme

        # Use predefined modern fonts
        self.DEFAULT_FONT = pygame.font.SysFont('Arial', 20)
        self.MEDIUM_FONT = pygame.font.SysFont('Arial', 40)
        self.BIG_FONT = pygame.font.SysFont('Arial', 50)

        # Button attributes
        self.login_button_rect = pygame.Rect(250, 300, 180, 40)
        self.guest_button_rect = pygame.Rect(440, 300, 180, 40)

        # Confirmation button attributes
        self.yes_button_rect = pygame.Rect(250, 250, 100, 40)
        self.no_button_rect = pygame.Rect(450, 250, 100, 40)

        # Load background image
        self.background_image = pygame.image.load('assets/images/background.png')

        # Caret properties
        self.caret_visible = True
        self.caret_timer = pygame.time.get_ticks()

    def draw(self):
        super().draw()

        # Get screen dimensions
        screen_width = self.SCREEN.get_width()
        screen_height = self.SCREEN.get_height()

        # Draw background image
        self.SCREEN.blit(self.background_image, (0, 0))
        self.update_caret()

        # Title
        title = self.BIG_FONT.render('Einloggen zum Spielen', True, self.thema.white_team)
        title_rect = title.get_rect(center=(screen_width // 2, 80))
        self.SCREEN.blit(title, title_rect)

        # Centered positions
        input_width = 600
        input_height = 40
        button_width = 180
        button_height = 40
        spacing = 10

        input_x = (screen_width - input_width) // 2
        username_y = 180
        password_y = username_y + input_height + spacing
        login_button_x = (screen_width - (button_width * 2 + spacing)) // 2
        guest_button_x = login_button_x + button_width + spacing
        button_y = password_y + input_height + spacing

        # Username field
        input_bg_color = self.thema.background
        username_border_color = self.thema.border if self.active_input != 'username' else self.thema.button_pressed
        pygame.draw.rect(self.SCREEN, input_bg_color, (input_x, username_y, input_width, input_height), border_radius=10)
        pygame.draw.rect(self.SCREEN, username_border_color, (input_x, username_y, input_width, input_height), 2, border_radius=10)
        username_text = self.DEFAULT_FONT.render(f'Nutzername: {self.username}', True, self.thema.text)
        self.SCREEN.blit(username_text, (input_x + 10, username_y + 10))

        # Draw caret for username field
        if self.active_input == 'username' and self.caret_visible:
            caret_pos = self.DEFAULT_FONT.size('Nutzername: ')[0] + self.DEFAULT_FONT.size(self.username)[0] + 10
            pygame.draw.line(self.SCREEN, self.thema.text, (input_x + caret_pos, username_y + 10), (input_x + caret_pos, username_y + 30))

        # Password field
        password_border_color = self.thema.border if self.active_input != 'password' else self.thema.button_pressed
        pygame.draw.rect(self.SCREEN, input_bg_color, (input_x, password_y, input_width, input_height), border_radius=10)
        pygame.draw.rect(self.SCREEN, password_border_color, (input_x, password_y, input_width, input_height), 2, border_radius=10)
        password_text = self.DEFAULT_FONT.render(f'Passwort: {"*" * len(self.password)}', True, self.thema.text)
        self.SCREEN.blit(password_text, (input_x + 10, password_y + 10))

        # Draw caret for password field
        if self.active_input == 'password' and self.caret_visible:
            caret_pos = self.DEFAULT_FONT.size('Passwort: ')[0] + self.DEFAULT_FONT.size('*' * len(self.password))[0] + 10
            pygame.draw.line(self.SCREEN, self.thema.text, (input_x + caret_pos, password_y + 10), (input_x + caret_pos, password_y + 30))

        # Login button
        self.login_button_rect = pygame.Rect(login_button_x, button_y, button_width, button_height)
        self.guest_button_rect = pygame.Rect(guest_button_x, button_y, button_width, button_height)

        # Draw login button (green background, black border, black text)
        pygame.draw.rect(self.SCREEN, self.thema.start_game_button, self.login_button_rect, border_radius=10)
        pygame.draw.rect(self.SCREEN, self.thema.black_team, self.login_button_rect, width=2, border_radius=10)
        login_text = self.DEFAULT_FONT.render('Einloggen', True, self.thema.button_background)
        login_text_rect = login_text.get_rect(center=self.login_button_rect.center)
        self.SCREEN.blit(login_text, login_text_rect)

        # Draw guest button (white background, black border, black text)
        pygame.draw.rect(self.SCREEN, self.thema.white_team, self.guest_button_rect, border_radius=10)
        pygame.draw.rect(self.SCREEN, self.thema.black_team, self.guest_button_rect, width=2, border_radius=10)
        guest_text = self.DEFAULT_FONT.render('Als Gast spielen', True, self.thema.black_team)
        guest_text_rect = guest_text.get_rect(center=self.guest_button_rect.center)
        self.SCREEN.blit(guest_text, guest_text_rect)

        # Prompt text
        prompt_text = 'Drücken Sie Tab, um die Felder zu wechseln'
        prompt = self.DEFAULT_FONT.render(prompt_text, True, self.thema.white_team)
        prompt_rect = prompt.get_rect(center=(screen_width // 2, button_y + button_height + 40))
        self.SCREEN.blit(prompt, prompt_rect)

        # Display message
        if self.message:
            message_text = self.DEFAULT_FONT.render(self.message, True, self.thema.white_team)
            message_rect = message_text.get_rect(center=(screen_width // 2, button_y + button_height + 70))
            self.SCREEN.blit(message_text, message_rect)

        # Confirmation message
        if self.show_confirmation:
            confirmation_width = 600
            confirmation_height = 200
            confirmation_x = (screen_width - confirmation_width) // 2
            confirmation_y = (screen_height - confirmation_height) // 2

            confirmation_bg_color = self.thema.notification_background
            confirmation_text_color = self.thema.notification_text
            pygame.draw.rect(self.SCREEN, confirmation_bg_color, (confirmation_x, confirmation_y, confirmation_width, confirmation_height), border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.notification_border, (confirmation_x, confirmation_y, confirmation_width, confirmation_height), 2, border_radius=10)
            confirmation_text = self.DEFAULT_FONT.render(self.confirmation_message, True, confirmation_text_color)
            confirmation_text_rect = confirmation_text.get_rect(center=(screen_width // 2, confirmation_y + 50))
            self.SCREEN.blit(confirmation_text, confirmation_text_rect)

            # Yes button
            self.yes_button_rect.center = (screen_width // 2 - 100, confirmation_y + 150)
            pygame.draw.rect(self.SCREEN, self.thema.button_yes, self.yes_button_rect, border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.button_text, self.yes_button_rect, 2, border_radius=10)
            yes_text = self.DEFAULT_FONT.render('Ja', True, self.thema.button_text)
            yes_text_rect = yes_text.get_rect(center=self.yes_button_rect.center)
            self.SCREEN.blit(yes_text, yes_text_rect)

            # No button
            self.no_button_rect.center = (screen_width // 2 + 100, confirmation_y + 150)
            pygame.draw.rect(self.SCREEN, self.thema.button_no, self.no_button_rect, border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.button_text, self.no_button_rect, 2, border_radius=10)
            no_text = self.DEFAULT_FONT.render('Nein', True, self.thema.button_text)
            no_text_rect = no_text.get_rect(center=self.no_button_rect.center)
            self.SCREEN.blit(no_text, no_text_rect)

        pygame.display.flip()

    def handle_event(self, event: Event):
        if event.type == pygame.KEYDOWN and not self.show_confirmation:
            self.caret_timer = pygame.time.get_ticks()  # Reset caret timer on key press
            self.caret_visible = True  # Ensure caret is visible immediately after typing

            if event.key == pygame.K_TAB:
                self.active_input = 'password' if self.active_input == 'username' else 'username'
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == 'username':
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            elif event.key == pygame.K_RETURN:  # Enter key pressed
                self.handle_login_attempt()
            else:
                if self.active_input == 'username':
                    self.username += event.unicode
                else:
                    self.password += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN and not self.show_confirmation:
            if self.login_button_rect.collidepoint(event.pos):
                self.handle_login_attempt()
            elif self.guest_button_rect.collidepoint(event.pos):
                self.handle_guest_login_attempt()
            elif pygame.Rect(100, 180, 600, 40).collidepoint(event.pos):
                self.active_input = 'username'
            elif pygame.Rect(100, 240, 600, 40).collidepoint(event.pos):
                self.active_input = 'password'

        elif event.type == pygame.MOUSEBUTTONDOWN and self.show_confirmation:
            if self.yes_button_rect.collidepoint(event.pos):
                if 'Als Gast spielen' in self.confirmation_message:
                    if self.on_auth_success:
                        self.on_auth_success(self.user_model)  # Move to menu
                    self.show_confirmation = False
                elif 'Willkommen zurück' in self.confirmation_message:
                    self.message = f'Willkommen zurück, {self.username}!'
                    self.show_confirmation = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Set timer for 1 second
                else:
                    self.user_model.add_user(self.username, self.password)
                    self.user_model.login(self.username, self.password)
                    self.message = f'Benutzer {self.username} erstellt und eingeloggt!'
                    self.show_confirmation = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Set timer for 1 second
            elif self.no_button_rect.collidepoint(event.pos):
                self.show_confirmation = False

        elif event.type == pygame.MOUSEMOTION and self.show_confirmation:
            if self.yes_button_rect.collidepoint(event.pos):
                self.yes_button_color = self.thema.button_pressed
            else:
                self.yes_button_color = self.thema.button
            if self.no_button_rect.collidepoint(event.pos):
                self.no_button_color = self.thema.button
            else:
                self.no_button_color = self.thema.button_pressed

        elif event.type == pygame.USEREVENT and not self.show_confirmation:  # Custom event triggered after 1 second
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
            if self.on_auth_success:
                self.on_auth_success(self.user_model)

    def update_caret(self):
        if pygame.time.get_ticks() - self.caret_timer > 1000:  # Blink interval in milliseconds
            self.caret_visible = not self.caret_visible
            self.caret_timer = pygame.time.get_ticks()

    def handle_login_attempt(self):
        user = self.user_model.get_user(self.username)
        if user:
            if self.user_model.login(self.username, self.password):
                self.confirmation_message = f'Benutzer existiert. Willkommen zurück, {self.username}! Einloggen?'
                self.show_confirmation = True
            else:
                self.message = 'Ungültiges Passwort. Bitte versuchen Sie es erneut.'
                self.show_confirmation = False
        else:
            self.confirmation_message = f'Benutzer existiert nicht. Neues Konto für {self.username} erstellen?'
            self.show_confirmation = True

        pygame.display.flip()

    def handle_guest_login_attempt(self):
        self.confirmation_message = f'Als Gast spielen?'
        self.show_confirmation = True
        pygame.display.flip()

    def exit_event(self):
        # self.sound.play('assets/sounds/auth/app_shutdown.mp3')
        sleep(1)