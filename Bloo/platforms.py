import pygame
import spriteSheet

blockSS = None
townSS = None
grass = None
cactus = None


def load():
    global blockSS
    global townSS
    global grass
    global cactus
    blockSS = spriteSheet.SpriteSheet("spritesheet_complete.png")
    townSS = spriteSheet.SpriteSheet("town_spritesheet.png")
    grass = pygame.image.load("grass.png").convert_alpha()
    cactus = pygame.image.load("cactus.png").convert_alpha()


class Platform(pygame.sprite.Sprite):
    def __init__(self, texture, index, size):
        super().__init__()
        self.blocks = []
        self.block = 0
        self.index = index

        # Get Sprites
        for i in range(7):
            self.blocks.append([130 * i, 1805, 128, 128])
        for i in range(3):
            self.blocks.append([910, 130 * i + 1545, 128, 128])
        for column in range(19):
            for row in range(15):
                self.blocks.append([130 * column + 1040, 130 * row, 128, 128])
        for i in range(4):
            self.blocks.append([3510, 130 * i, 128, 128])

        # Set Image
        self.texture = {
            "stone": 0, "snow": 18, "sand": 36,
            "purple": 54, "dirt": 72, "mud": 90,
            "misc": 108
        }
        self.block = self.texture[texture] + index
        self.image = blockSS.img(
            self.blocks[self.block][0], self.blocks[self.block][1],
            self.blocks[self.block][2], self.blocks[self.block][3])
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


# Blocks that the player can pass through
class NoCollide(pygame.sprite.Sprite):
    def __init__(self, img, size):
        super().__init__()
        global grass
        global cactus
        if img == "grass":
            self.image = pygame.transform.scale(grass, (size, size))
        elif img == "cactus":
            self.image = pygame.transform.scale(cactus, (size, size))
        self.rect = self.image.get_rect()


# Town buildings
class Building(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = townSS.img(70 * x, 70 * y, 70, 70)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()


# Shop guy
class Shopkeeper(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.image = blockSS.img(921, 622, 105, 151)
        self.image = pygame.transform.scale(self.image, (size, int(151 * size/105)))
        self.rect = self.image.get_rect()


# Portals to other levels
class Portal(pygame.sprite.Sprite):
    def __init__(self, destination):
        super().__init__()
        self.destination = destination
        self.image = pygame.image.load("portal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
