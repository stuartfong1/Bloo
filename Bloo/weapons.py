import pygame
import spriteSheet
import numpy as np

cooldown = False
inventory = []
genericSS = None
fishSS = None


def load():
    global inventory
    global genericSS
    global fishSS
    genericSS = spriteSheet.SpriteSheet("genericItems.png")
    fishSS = spriteSheet.SpriteSheet("fishSpritesheet.png")
    inventory.append(
        ["Spatula", 0, pygame.transform.scale(genericSS.img(462, 1132, 88, 140)
                                              , (22, 35)), "Melee", 50, True, "Order up!"])
    inventory.append(
        ["Rock", 0, pygame.transform.scale(fishSS.img(320, 359, 53, 32)
                                           , (25, 15)), "Ranged", 50, True, "It's just a rock."])


class Melee(pygame.sprite.Sprite):
    def __init__(self, startX, startY, mousePosX, item):
        super().__init__()
        self.image = item[2]
        self.originalImage = self.image
        self.pos = pygame.math.Vector2(startX, startY)
        self.angle = 20
        self.isLeft = False
        self.offset = pygame.math.Vector2(22, -35)
        self.rotatedOffset = self.offset.rotate(-self.angle)
        self.rect = self.image.get_rect(center=self.pos + self.rotatedOffset)
        self.rect.x += 20
        self.collisionList = []
        self.damage = item[4]
        if mousePosX < startX:
            self.isLeft = True

    def update(self, level):
        global cooldown
        if -90 <= self.angle <= 130:
            cooldown = True
            if self.isLeft:
                self.image = pygame.transform.rotozoom(self.originalImage, self.angle, 1)
                self.rotatedOffset = self.offset.rotate(-self.angle)
                self.angle += 10
            else:
                self.image = pygame.transform.rotozoom(self.originalImage, self.angle, 1)
                self.rotatedOffset = self.offset.rotate(-self.angle)
                self.angle -= 10
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(center=self.pos + self.rotatedOffset)
            self.rect.x += 20
        else:
            self.kill()
            cooldown = False


class Ranged(pygame.sprite.Sprite):
    def __init__(self, startX, startY, mousePosX, mousePosY, item):
        super().__init__()
        self.image = item[2]
        self.rect = self.image.get_rect()
        self.startX = startX
        self.startY = startY
        self.rect.x = startX
        self.rect.y = startY
        self.directionX = mousePosX
        self.directionY = mousePosY
        self.travelCounter = 10
        self.collisionList = []
        self.damage = item[4]

    def update(self, level):
        global cooldown
        if self.travelCounter > 0 and self.directionX - self.startX != 0:
            cooldown = True
            if (self.directionX - self.startX) >= 0:
                self.rect.y += 10 * np.sin(
                    np.arctan((self.directionY - self.startY) / (self.directionX - self.startX)))
                self.rect.x += 10 * np.cos(
                    np.arctan((self.directionY - self.startY) / (self.directionX - self.startX)))
            else:
                self.rect.y -= 10 * np.sin(
                    np.arctan((self.directionY - self.startY) / (self.directionX - self.startX)))
                self.rect.x -= 10 * np.cos(
                    np.arctan((self.directionY - self.startY) / (self.directionX - self.startX)))
            self.travelCounter -= 1
        else:
            self.kill()
            cooldown = False

        self.collisionList = pygame.sprite.spritecollide(self, level.platformList, False)
        if len(self.collisionList) > 0:
            self.kill()
            cooldown = False
