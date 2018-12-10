import pygame

from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, screen, centerx):
        super().__init__()

        self.screen = screen

        centery = screen.get_rect().bottom - 80

        self.top_left_triangle_rect = pygame.Rect(centerx - 32,
                                                  centery - 24, 16, 16)
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
        self.top_right_triangle_rect = pygame.Rect(centerx + 16,
                                                   centery - 24, 16, 16)

        self.mid_left = pygame.Rect(centerx - 32, centery - 8, 16, 16)
        self.mid_right = pygame.Rect(centerx + 16, centery - 8, 16, 16)

        self.bottom_left = pygame.Rect(centerx - 32, centery + 8, 16, 16)
        self.bottom_right = pygame.Rect(centerx + 16, centery + 8, 16, 16)

        self.color = (0, 180, 0)

    def standing(self):
        if self.top_left_triangle is not None and \
                self.top_left is not None and \
                self.top_right is not None and \
                self.top_right_triangle is not None and \
                self.mid_left is not None and \
                self.mid_right is not None and \
                self.bottom_left is not None and \
                self.bottom_right is not None:
            return False
        else:
            return True

    def collide(self, rect):
        if self.top_left_triangle is not None:
            if rect.colliderect(self.top_left_triangle_rect):
                self.top_left_triangle = None
                return True
        if self.top_left is not None:
            if rect.colliderect(self.top_left):
                self.top_left = None
                return True
        if self.top_right is not None:
            if rect.colliderect(self.top_right):
                self.top_right = None
                return True
        if self.top_right_triangle is not None:
            if rect.colliderect(self.top_right_triangle_rect):
                self.top_right_triangle = None
                return True
        if self.mid_left is not None:
            if rect.colliderect(self.mid_left):
                self.mid_left = None
                return True
        if self.mid_right is not None:
            if rect.colliderect(self.mid_right):
                self.mid_right = None
                return True
        if self.bottom_left is not None:
            if rect.colliderect(self.bottom_left):
                self.bottom_left = None
                return True
        if self.bottom_right is not None:
            if rect.colliderect(self.bottom_right):
                self.bottom_right = None
                return True
        return False

    def render(self):
        if self.top_left_triangle is not None:
            pygame.draw.polygon(self.screen, self.color,
                                self.top_left_triangle)
        if self.top_left is not None:
            pygame.draw.rect(self.screen, self.color, self.top_left)
        if self.top_right is not None:
            pygame.draw.rect(self.screen, self.color, self.top_right)
        if self.top_right_triangle is not None:
            pygame.draw.polygon(self.screen, self.color,
                                self.top_right_triangle)

        if self.mid_left is not None:
            pygame.draw.rect(self.screen, self.color, self.mid_left)
        if self.mid_right is not None:
            pygame.draw.rect(self.screen, self.color, self.mid_right)

        if self.bottom_left is not None:
            pygame.draw.rect(self.screen, self.color, self.bottom_left)
        if self.bottom_right is not None:
            pygame.draw.rect(self.screen, self.color, self.bottom_right)
