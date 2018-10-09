import pygame

from scene import Scene
from text import Text
from alien import Alien
from ufo import UFO


class MenuScene(Scene):
    def __init__(self, director, background=(0, 0, 0)):
        super().__init__(director)

        self.background = background

        text_rect = pygame.Rect(0, 20, 300, 140)
        text_rect.centerx = director.screen.get_rect().centerx

        self.logo = Text(text_rect, 140, (255, 255, 255), director.screen,
                         "SPACE")

        text_rect.centery += 60

        self.header = Text(text_rect, 90, (0, 180, 0), director.screen,
                           "INVADERS")

        self.alien_one = Alien(director.screen)
        self.alien_two = Alien(screen=director.screen, alien_type=2)
        self.alien_three = Alien(screen=director.screen, alien_type=3)
        self.alien_four = Alien(screen=director.screen, alien_type=4)
        self.ufo = UFO(director.screen)

        self.alien_one.rect.center = self.alien_two.rect.center = \
            self.alien_three.rect.center = self.alien_four.rect.center = \
            self.ufo.rect.center = director.screen.get_rect().center

        self.alien_one.rect.centerx -= self.ufo.rect.width + 20
        self.alien_two.rect.centerx -= self.ufo.rect.width + 20
        self.alien_three.rect.centerx -= self.ufo.rect.width + 20
        self.alien_four.rect.centerx -= self.ufo.rect.width + 20
        self.ufo.rect.centerx -= self.ufo.rect.width + 20

        self.alien_one.rect.centery -= self.alien_one.rect.height * 2 + 40
        self.alien_two.rect.centery -= self.alien_two.rect.height + 20
        self.alien_four.rect.centery += self.alien_four.rect.height + 20
        self.ufo.rect.centery += self.alien_four.rect.height + \
            self.ufo.rect.height + 40

        self.score_one = Text(self.alien_one.rect, 30, (150, 150, 150),
                              director.screen, "= 10")
        self.score_two = Text(self.alien_two.rect, 30, (150, 150, 150),
                              director.screen, "= 20")
        self.score_three = Text(self.alien_three.rect, 30, (150, 150, 150),
                                director.screen, "= 30")
        self.score_four = Text(self.alien_four.rect, 30, (150, 150, 150),
                               director.screen, "= 40")
        self.score_five = Text(self.ufo.rect, 30, (150, 150, 150),
                               director.screen, "= ???")

        self.score_one.rect.centerx = self.score_two.rect.centerx = \
            self.score_three.rect.centerx = self.score_four.rect.centerx = \
            self.score_five.rect.centerx = self.ufo.rect.centerx + \
            self.ufo.rect.width + 20

        self.score_five.rect.centerx += 8

        self.score_one.prep_img()
        self.score_two.prep_img()
        self.score_three.prep_img()
        self.score_four.prep_img()
        self.score_five.prep_img()

        menu_rect = pygame.Rect(0, 0, 100, 30)

        menu_rect.center = director.screen.get_rect().center
        menu_rect.y = director.screen.get_rect().bottom - 150

        self.play = Text(menu_rect, 50, (255, 255, 255), director.screen,
                         "PLAY GAME")

        menu_rect.y += 60

        self.high_score = Text(menu_rect, 50, (255, 255, 255), director.screen,
                               "HIGH SCORES")

        self.mouse_on = None

    def mousebuttondown(self, button, point):
        self.mouse_on = None

        if self.play.rect.collidepoint(point):
            self.director.set_scene("game")
        elif self.high_score.rect.collidepoint(point):
            self.director.set_scene("scores")

    def update(self):
        point = pygame.mouse.get_pos()

        if self.mouse_on is not None:
            self.mouse_on.color = (255, 255, 255)
            self.mouse_on.prep_img()
            self.mouse_on = None

        if self.play.rect.collidepoint(point):
            self.mouse_on = self.play
        elif self.high_score.rect.collidepoint(point):
            self.mouse_on = self.high_score

    def render(self):
        self.director.screen.fill(self.background)

        self.logo.render()
        self.header.render()

        self.alien_one.render()
        self.alien_two.render()
        self.alien_three.render()
        self.alien_four.render()
        self.ufo.render()

        self.score_one.render()
        self.score_two.render()
        self.score_three.render()
        self.score_four.render()
        self.score_five.render()

        if self.mouse_on is not None:
            self.mouse_on.color = (0, 180, 0)
            self.mouse_on.prep_img()

        self.play.render()
        self.high_score.render()
