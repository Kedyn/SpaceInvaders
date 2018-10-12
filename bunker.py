import pygame

from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, screen, centerx):
        super().__init__()

        self.screen = screen

        centery = screen.get_rect().bottom - 80

        self.top_left_triangle = [
                                  [centerx - 32, centery - 8],
                                  [centerx - 16, centery - 24],
                                  [centerx - 16, centery - 8]
                                ]
        self.top_left = pygame.Rect(centerx - 16, centery - 24, 16, 16)
        self.top_right = pygame.Rect(centerx, centery - 24, 16, 16)
        self.top_right_triangle = [
                                   [centerx + 16, centery - 24],
                                   [centerx + 32, centery - 8],
                                   [centerx + 16, centery - 8]
                                  ]

        self.mid_left = pygame.Rect(centerx - 32, centery - 8, 16, 16)
        self.mid_right = pygame.Rect(centerx + 16, centery - 8, 16, 16)

        self.bottom_left = pygame.Rect(centerx - 32, centery + 8, 16, 16)
        self.bottom_right = pygame.Rect(centerx + 16, centery + 8, 16, 16)

        self.color = (0, 180, 0)

    def render(self):
        pygame.draw.polygon(self.screen, self.color, self.top_left_triangle)
        pygame.draw.rect(self.screen, self.color, self.top_left)
        pygame.draw.rect(self.screen, self.color, self.top_right)
        pygame.draw.polygon(self.screen, self.color, self.top_right_triangle)

        pygame.draw.rect(self.screen, self.color, self.mid_left)
        pygame.draw.rect(self.screen, self.color, self.mid_right)

        pygame.draw.rect(self.screen, self.color, self.bottom_left)
        pygame.draw.rect(self.screen, self.color, self.bottom_right)
