import pygame

from scene import Scene
from text import Text


class ScoresScene(Scene):
    def __init__(self, director, background=(0, 0, 0)):
        super().__init__(director)

        self.background = background

        text_rect = pygame.Rect(0, 20, 300, 140)
        text_rect.centerx = director.screen.get_rect().centerx

        self.logo = Text(text_rect, 140, director.regular_text_color,
                         director.screen, "PACMAN")

        text_rect.centery += 60

        self.header = Text(text_rect, 90, director.special_text_color,
                           director.screen, "PORTAL")

        menu_rect = pygame.Rect(0, 0, 100, 30)

        menu_rect.center = director.screen.get_rect().center
        menu_rect.y = director.screen.get_rect().bottom - 90

        self.menu = Text(menu_rect, 50, director.regular_text_color,
                         director.screen, "RETURN TO MENU")

        self.mouse_on = None

    def reset(self):
        high_scores = open('assets/high_scores.txt',
                           'r').read().split('\n')

        self.high_scores = []

        score_rect = pygame.Rect(0, 200, 100, 30)

        score_rect.centerx = self.director.screen.get_rect().centerx

        for score in high_scores:
            if score:
                score_text = Text(score_rect, 50,
                                  self.director.special_text_color,
                                  self.director.screen, score)
                self.high_scores.append(score_text)
                score_rect.y += 50

    def mousebuttondown(self, button, point):
        self.mouse_on = None

        if self.menu.rect.collidepoint(point):
            self.director.set_scene("menu")

    def update(self):
        point = pygame.mouse.get_pos()

        if self.mouse_on is not None:
            self.mouse_on.color = self.director.regular_text_color
            self.mouse_on.prep_img()
            self.mouse_on = None

        if self.menu.rect.collidepoint(point):
            self.mouse_on = self.menu

    def render(self):
        self.director.screen.fill(self.background)

        self.logo.render()
        self.header.render()

        if self.mouse_on is not None:
            self.mouse_on.color = self.director.special_text_color
            self.mouse_on.prep_img()

        for score in self.high_scores:
            score.render()

        self.menu.render()