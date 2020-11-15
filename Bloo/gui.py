import pygame
import spriteSheet


# Coin Icon
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.SS = spriteSheet.SpriteSheet("spritesheet_complete.png")
        self.image = self.SS.img(2882, 1582, 86, 86)
        self.image = pygame.transform.scale(self.image, (43, 43))
        self.rect = self.image.get_rect()

    def update(self, screen):
        screen.blit(self.image, (10, 15))


# Coin numbers
class Number(pygame.sprite.Sprite):
    def __init__(self, digit, order):
        super().__init__()
        self.SS = spriteSheet.SpriteSheet("spritesheet_complete.png")
        self.order = order
        self.sprites = []

        self.sprites.append([2990, 910, 128, 128])
        self.sprites.append([2990, 650, 128, 128])
        self.sprites.append([2470, 910, 128, 128])
        for i in range(5):
            self.sprites.append([2990, 520 - 130 * i, 128, 128])
        for i in range(2):
            self.sprites.append([2860, 1820 - 130 * i, 128, 128])
        self.sprites.append([2730, 260, 128, 128])

        self.image = self.SS.img(self.sprites[digit][0], self.sprites[digit][1],
                                 self.sprites[digit][2], self.sprites[digit][3])
        self.rect = self.image.get_rect()

    def update(self, screen, digit):
        self.image = self.SS.img(self.sprites[digit][0], self.sprites[digit][1],
                                 self.sprites[digit][2], self.sprites[digit][3])
        self.image = pygame.transform.scale(self.image, (self.rect.width // 2, self.rect.height // 2))
        screen.blit(self.image, (self.order * self.rect.width // 3, 0))


# Menu
class MenuButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("backpack.png").convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 747
        self.rect.y = 15
        self.image = pygame.transform.scale(self.image, (43, 43))

    def update(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
