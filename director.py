import pygame
import sys


class Director:
    def __init__(self, resolution, title):
        pygame.init()

        self.screen = pygame.display.set_mode(resolution)

        pygame.display.set_caption(title)

        self.scene_list = None
        self.scene = None
        self.quit = False

    def loop(self):
        if self.scene is not None:
            while not self.quit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit = True
                    elif event.type == pygame.KEYDOWN:
                        self.scene.keydown(event.key)
                    elif event.type == pygame.KEYUP:
                        self.scene.keyup(event.key)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.scene.mousebuttondown(event.button, event.pos)

                self.scene.update()
                self.scene.render()

                pygame.display.flip()

            if self.quit:
                sys.exit()

    def set_scene(self, scene_name):
        self.scene = self.scene_list.get(scene_name)
        self.scene.reset()
