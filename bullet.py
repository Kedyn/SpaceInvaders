import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, screen, x, y, color=(0, 0, 200), speed_factor=-1):
        super().__init__()
        self.screen = screen
        self.color = color
        self.speed_factor = speed_factor

        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = x

        if speed_factor < 0:
            self.rect.top = y - 15
        else:
            self.rect.top = y + 15

        self.y = float(self.rect.y)

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
