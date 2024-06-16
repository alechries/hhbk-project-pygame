import pygame
from modules.auth import AuthPage
from utils.start_app import start_app
from models.user import UserModel

pygame.init()

if __name__ == "__main__":
    user = UserModel()
    start_app(AuthPage())
