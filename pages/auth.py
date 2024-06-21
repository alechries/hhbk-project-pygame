import pygame
from utils.page import BasePage
from pygame.event import Event
from utils.sound import SoundManager
from models.user import UserModel
from time import sleep

class AuthPage(BasePage):
    def __init__(self, on_auth_success=None):
        super().__init__()
        self.page_name = 'auth'
        self.sound = SoundManager()
        self.sound.play('assets/sounds/auth/loaded.mp3')
        self.user_model = UserModel()
        self.user_model.initialize_table()
        self.username = ''
        self.password = ''
        self.active_input = 'username'
        self.on_auth_success = on_auth_success
        self.message = ''

        # Use predefined modern fonts
        self.DEFAULT_FONT = pygame.font.SysFont('Arial', 20)
        self.MEDIUM_FONT = pygame.font.SysFont('Arial', 40)
        self.BIG_FONT = pygame.font.SysFont('Arial', 50)

    def draw(self):
        super().draw()
        
        # Background color (light blue)
        self.SCREEN.fill((173, 216, 230))

        # Title
        title = self.BIG_FONT.render('Login to Play', True, self.thema.text)
        title_rect = title.get_rect(center=(self.SCREEN.get_width() // 2, 80))
        self.SCREEN.blit(title, title_rect)

        # Username field
        input_bg_color = (255, 255, 255)
        pygame.draw.rect(self.SCREEN, input_bg_color, (100, 180, 600, 40), border_radius=10)
        username_text = self.DEFAULT_FONT.render(f'Username: {self.username}', True, self.thema.text)
        self.SCREEN.blit(username_text, (110, 190))

        # Password field
        pygame.draw.rect(self.SCREEN, input_bg_color, (100, 240, 600, 40), border_radius=10)
        password_text = self.DEFAULT_FONT.render(f'Password: {"*" * len(self.password)}', True, self.thema.text)
        self.SCREEN.blit(password_text, (110, 250))

        # Prompt text
        prompt_text = 'Press Enter to submit' if self.active_input == 'password' else 'Press Tab to switch to password'
        prompt = self.DEFAULT_FONT.render(prompt_text, True, self.thema.text)
        prompt_rect = prompt.get_rect(center=(self.SCREEN.get_width() // 2, 320))
        self.SCREEN.blit(prompt, prompt_rect)

        # Display message
        if self.message:
            message_text = self.DEFAULT_FONT.render(self.message, True, self.thema.text)
            message_rect = message_text.get_rect(center=(self.SCREEN.get_width() // 2, 380))
            self.SCREEN.blit(message_text, message_rect)

        pygame.display.flip()

    def handle_event(self, event: Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.active_input = 'password' if self.active_input == 'username' else 'username'
            elif event.key == pygame.K_RETURN:
                if self.active_input == 'password':
                    user = self.user_model.get_user(self.username)
                    if user:
                        if self.user_model.check_password(self.username, self.password):
                            self.message = f'Welcome back, {self.username}!'
                            print(self.message)
                            pygame.time.set_timer(pygame.USEREVENT, 1000)  # Set timer for 1 second
                        else:
                            self.message = 'Invalid password. Please try again.'
                            print(self.message)
                    else:
                        self.user_model.add_user(self.username, self.password)
                        self.message = f'User {self.username} created and logged in!'
                        print(self.message)
                        pygame.time.set_timer(pygame.USEREVENT, 1000)  # Set timer for 1 second
            elif event.key == pygame.K_BACKSPACE:
                if self.active_input == 'username':
                    self.username = self.username[:-1]
                else:
                    self.password = self.password[:-1]
            else:
                if self.active_input == 'username':
                    self.username += event.unicode
                else:
                    self.password += event.unicode

        elif event.type == pygame.USEREVENT:  # Custom event triggered after 1 second
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer
            if self.on_auth_success:
                self.on_auth_success()

    def exit_event(self):
        self.sound.play('assets/sounds/auth/app_shutdown.mp3')
        sleep(1)
