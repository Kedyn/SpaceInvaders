import pygame

from pygame.sprite import Sprite


class Explosion(Sprite):

    def __init__(self, screen, center, speed=200):
        super().__init__()

        self.screen = screen
        self.speed = speed

        self.explosion_one = pygame.image.load('images/explosion_1.png')
        self.explosion_two = pygame.image.load('images/explosion_2.png')
        self.explosion_three = pygame.image.load('images/explosion_3.png')
        self.explosion_four = pygame.image.load('images/explosion_4.png')
        self.explosion_five = pygame.image.load('images/explosion_5.png')
        self.explosion_six = pygame.image.load('images/explosion_6.png')
        self.explosion_seven = pygame.image.load('images/explosion_7.png')

        self.image = self.explosion_one
        self.rect = self.image.get_rect()

        self.rect.center = center

        self.explosion = 1
        self.old_ticks = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.old_ticks >= self.speed:
            if self.explosion is 2:
                self.image = self.explosion_two
            elif self.explosion is 3:
                self.image = self.explosion_three
            elif self.explosion is 4:
                self.image = self.explosion_four
            elif self.explosion is 5:
                self.image = self.explosion_five
            elif self.explosion is 6:
                self.image = self.explosion_six
            else:
                self.image = self.explosion_seven
            self.explosion += 1

    def render(self):
        self.screen.blit(self.image, self.rect)
