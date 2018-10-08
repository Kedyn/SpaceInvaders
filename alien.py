import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, screen, speed_factor=1, direction=1, type=1):
        super().__init__()
        self.screen = screen

        self.speed_factor = speed_factor
        self.direction = direction

        self.normal = pygame.image.load('images/alien_' + str(type) + '.png')
        self.step = pygame.image.load('images/alien_' + str(type) +
                                      '_step.png')

        self.image = self.normal

        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

        self.old_ticks = pygame.time.get_ticks()

    def check_edges(self):
        screen_rect = self.screen.get_rect()

        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.speed_factor * self.direction)
        self.rect.x = self.x

        if (pygame.time.get_ticks() - self.old_ticks) >= 400:
            self.old_ticks = pygame.time.get_ticks()

            if self.image is self.normal:
                self.image = self.step
            else:
                self.image = self.normal

    def render(self):
        self.screen.blit(self.image, self.rect)
