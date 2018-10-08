import pygame.font
import copy


class Text:
    def __init__(self, rect, size, color, screen, text):
        self.screen = screen
        self.rect = copy.deepcopy(rect)
        self.text = text

        self.color = color
        self.font = pygame.font.SysFont(None, size)

        self.text_image = None
        self.text_image_rect = None

        self.prep_img()

    def prep_img(self):
        self.text_image = self.font.render(self.text, True,
                                           self.color)

        image_rect = self.text_image.get_rect()
        image_rect.center = self.rect.center

        self.rect.width = image_rect.width
        self.rect.height = image_rect.height
        self.rect.center = image_rect.center

    def render(self):
        self.screen.blit(self.text_image, self.rect)
