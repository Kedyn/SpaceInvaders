import pygame

from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, screen, speed_factor=1, direction=1):
        super().__init__()

        self.screen = screen

        self.speed_factor = speed_factor
        self.direction = direction

        self.image = pygame.image.load('assets/images/ufo.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right + self.rect.width:
            return True
        elif self.rect.left <= 0 - self.rect.width:
            return True
        return False

    def update(self):
        self.x += (self.speed_factor * self.direction)
        self.rect.x = self.x

    def render(self):
        self.screen.blit(self.image, self.rect)
