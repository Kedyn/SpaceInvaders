import pygame

from ship import Ship
from text import Text
from pygame.sprite import Group


class GameStats():
    def __init__(self, director):
        self.director = director

        self.game_active = False

        rect = pygame.Rect(director.screen.get_rect().centerx, 4, 100, 40)
        self.high_score_text = Text(rect, 30, (0, 180, 0), director.screen,
                                    "HIGH SCORE: 0")

        rect.right = director.screen.get_rect().right - 10
        self.score_text = Text(rect, 30, (0, 180, 0), director.screen,
                               "SCORE: 0")

        high_scores = open('assets/high_scores.txt',
                           'r').read().split('\n')

        self.high_scores = []

        for score in high_scores:
            if score:
                self.high_scores.append(int(score))

        self.high_scores.sort(reverse=True)

        self.reset()

    def save_scores(self):
        if self.high_score == self.score:
            if len(self.high_scores) is 10:
                self.high_scores[9] = self.score
            else:
                self.high_scores.append(self.score)

        self.high_scores.sort(reverse=True)

        with open('assets/high_scores.txt', 'w') as f:
            for score in self.high_scores:
                f.write(str(score) + '\n')

    def reset(self):
        self.ships_left = 3
        self.high_score = self.high_scores[0]
        self.score = 0
        self.level = 1

        self.update()

    def update(self):
        if self.high_score < self.score:
            self.high_score = self.score

        self.ships = Group()

        for ship_number in range(self.ships_left):
            ship = Ship(self.director.screen, 0)

            ship.rect.x = 10 + ((10 + ship.rect.width) * ship_number)
            ship.rect.y = 10

            self.ships.add(ship)

        self.high_score_text.text = "HIGH SCORE: " + str(self.high_score)
        self.score_text.text = "SCORE: " + str(self.score)

        self.high_score_text.prep_img()
        self.score_text.prep_img()

        self.score_text.rect.right = self.director.screen.get_rect().right - 10

    def render(self):
        for ship_number in range(self.ships_left):
            self.ships.sprites()[ship_number].render()

        self.high_score_text.render()
        self.score_text.render()
