import pygame


class SpriteSheet(object):
    def __init__(self, filename):
        self.spriteSheet = pygame.image.load(filename).convert()

    def img(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.set_colorkey((0, 0, 0))
        image.blit(self.spriteSheet, (0, 0), (x, y, width, height))
        return image
