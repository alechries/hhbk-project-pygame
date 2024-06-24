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
        self.user_model.initialize_table()
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
        self.login_button_rect = pygame.Rect(350, 300, 100, 40)

        # Confirmation button attributes
        self.yes_button_rect = pygame.Rect(250, 250, 100, 40)
        self.no_button_rect = pygame.Rect(450, 250, 100, 40)

        # Load background image
        self.background_image = pygame.image.load(
            'assets/images/background.png')

        # Caret properties
        self.caret_visible = True
        self.caret_timer = pygame.time.get_ticks()

    def draw(self):
        super().draw()

        # Draw background image
        self.SCREEN.blit(self.background_image, (0, 0))
        self.update_caret()
    # Title
        title = self.BIG_FONT.render('Login to Play', True, self.thema.white_team)
        title_rect = title.get_rect(center=(self.SCREEN.get_width() // 2, 80))
        self.SCREEN.blit(title, title_rect)

        # Username field
        input_bg_color = self.thema.background
        username_border_color = self.thema.border if self.active_input != 'username' else self.thema.button_pressed
        pygame.draw.rect(self.SCREEN, input_bg_color, (100, 180, 600, 40), border_radius=10)
        pygame.draw.rect(self.SCREEN, username_border_color, (100, 180, 600, 40), 2, border_radius=10)
        username_text = self.DEFAULT_FONT.render(f'Username: {self.username}', True, self.thema.text)
        self.SCREEN.blit(username_text, (110, 190))

        # Draw caret for username field
        if self.active_input == 'username' and self.caret_visible:
            caret_pos = self.DEFAULT_FONT.size(self.username)[0] + 215
            pygame.draw.line(self.SCREEN, self.thema.text, (caret_pos, 190), (caret_pos, 210))

        # Password field
        password_border_color = self.thema.border if self.active_input != 'password' else self.thema.button_pressed
        pygame.draw.rect(self.SCREEN, input_bg_color, (100, 240, 600, 40), border_radius=10)
        pygame.draw.rect(self.SCREEN, password_border_color, (100, 240, 600, 40), 2, border_radius=10)
        password_text = self.DEFAULT_FONT.render(f'Password: {"*" * len(self.password)}', True, self.thema.text)
        self.SCREEN.blit(password_text, (110, 250))

        # Draw caret for password field
        if self.active_input == 'password' and self.caret_visible:
            caret_pos = self.DEFAULT_FONT.size('*' * len(self.password))[0] + 212
            pygame.draw.line(self.SCREEN, self.thema.text, (caret_pos, 250), (caret_pos, 270))

        # Login button
        pygame.draw.rect(self.SCREEN, self.thema.button, self.login_button_rect, border_radius=10)
        pygame.draw.rect(self.SCREEN, self.thema.button_text, self.login_button_rect, width=2, border_radius=10)
        login_text = self.DEFAULT_FONT.render('Login', True, self.thema.button_text)
        login_text_rect = login_text.get_rect(center=self.login_button_rect.center)
        self.SCREEN.blit(login_text, login_text_rect)

        # Prompt text
        prompt_text = 'Press Tab to switch fields'
        prompt = self.DEFAULT_FONT.render(prompt_text, True, self.thema.white_team)
        prompt_rect = prompt.get_rect(center=(self.SCREEN.get_width() // 2, 400))  # Added top margin
        self.SCREEN.blit(prompt, prompt_rect)

        # Display message
        if self.message:
            message_text = self.DEFAULT_FONT.render(self.message, True, self.thema.white_team)
            message_rect = message_text.get_rect(center=(self.SCREEN.get_width() // 2, 430))
            self.SCREEN.blit(message_text, message_rect)

        # Confirmation message
        if self.show_confirmation:
            confirmation_bg_color = self.thema.notification_background
            confirmation_text_color = self.thema.notification_text
            pygame.draw.rect(self.SCREEN, confirmation_bg_color, (150, 150, 500, 200), border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.notification_border, (150, 150, 500, 200), 2, border_radius=10)
            confirmation_text = self.DEFAULT_FONT.render(self.confirmation_message, True, confirmation_text_color)
            confirmation_text_rect = confirmation_text.get_rect(center=(self.SCREEN.get_width() // 2, 200))
            self.SCREEN.blit(confirmation_text, confirmation_text_rect)

            # Yes button
            pygame.draw.rect(self.SCREEN, self.thema.button_yes, self.yes_button_rect, border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.button_text, self.yes_button_rect, 2, border_radius=10)
            yes_text = self.DEFAULT_FONT.render('Yes', True, self.thema.button_text)
            yes_text_rect = yes_text.get_rect(center=self.yes_button_rect.center)
            self.SCREEN.blit(yes_text, yes_text_rect)

            # No button
            pygame.draw.rect(self.SCREEN, self.thema.button_no, self.no_button_rect, border_radius=10)
            pygame.draw.rect(self.SCREEN, self.thema.button_text, self.no_button_rect, 2, border_radius=10)
            no_text = self.DEFAULT_FONT.render('No', True, self.thema.button_text)
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

        elif event.type == pygame.MOUSEBUTTONDOWN and self.show_confirmation:
            if self.yes_button_rect.collidepoint(event.pos):
                if 'Welcome back' in self.confirmation_message:
                    self.message = f'Welcome back, {self.username}!'
                    self.show_confirmation = False
                    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Set timer for 1 second
                else:
                    self.user_model.add_user(self.username, self.password)
                    self.message = f'User {self.username} created and logged in!'
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
                self.confirmation_message = f'User exists. Welcome back, {self.username}! Log in?'
                self.show_confirmation = True
            else:
                self.message = 'Invalid password. Please try again.'
                self.show_confirmation = False
        else:
            self.confirmation_message = f'User does not exist. Create new account for {self.username}?'
            self.show_confirmation = True
        pygame.display.flip()

    def exit_event(self):
        # self.sound.play('assets/sounds/auth/app_shutdown.mp3')
        sleep(1)
