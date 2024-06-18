import pygame
from pages.auth import AuthPage
from utils.start_app import start_app
from utils.model import BaseModel

pygame.init()

if __name__ == "__main__":
    BaseModel.initialize_tables()
    start_app(AuthPage())
