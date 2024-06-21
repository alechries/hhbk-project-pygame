import pygame
from pygame.event import Event


class Button:
    def __init__(self, x, y, width, height, text, color, background):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.text_surf = self.font.render(self.text, True, background)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event: Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False
