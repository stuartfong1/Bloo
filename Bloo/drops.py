import pygame
import spriteSheet
import numpy as np

coinSS = None


def load():
    global coinSS
    coinSS = spriteSheet.SpriteSheet("spritesheet_complete.png")


class Coin(pygame.sprite.Sprite):
    def __init__(self, texture, x, y):
        super().__init__()
        global coinSS
        self.sprites = []

        self.sprites.append([2730, 130, 128, 128])  # Bronze
        self.sprites.append([2600, 1820, 128, 128])  # Silver
        self.sprites.append([2730, 0, 128, 128])  # Gold

        self.texture = {"bronze": 0, "silver": 1, "gold": 2}
        self.value = 10 ** self.texture[texture]
        self.image = coinSS.img(self.sprites[self.texture[texture]][0], self.sprites[self.texture[texture]][1],
                                self.sprites[self.texture[texture]][2], self.sprites[self.texture[texture]][3])
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.y = y
        self.rect.y = y
        self.shift = 0

    def update(self, screen):
        self.shift += 1
        self.rect.y = self.y + np.sin(self.shift / 3) * 2
