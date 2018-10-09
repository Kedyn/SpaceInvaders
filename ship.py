import pygame

from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, screen, speed_factor=1):
        super().__init__()

        self.screen = screen
        self.speed_factor = speed_factor

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)

        self.moving_right = False
        self.moving_left = False

    def reset(self):
        self.center = self.screen_rect.centerx

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.speed_factor

        self.rect.centerx = self.center

    def render(self):
        self.screen.blit(self.image, self.rect)
