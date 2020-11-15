import pygame
import spriteSheet
import drops
import weapons
import random

enemySS = None
newSlime = False
pinchyX = 0
isDefeated = False


def load():
    global enemySS
    enemySS = spriteSheet.SpriteSheet("spritesheet_complete.png")


class Enemy(pygame.sprite.Sprite):
    def __init__(self, species, health, coinDrop, size):
        super().__init__()
        global enemySS
        self.coords = []
        self.images = []
        self.sprite = 0
        self.species = species
        self.size = size
        self.SS = enemySS
        self.isLeft = False
        self.detectLeft = 0
        self.detectRight = 0
        self.detectBottomLeft = 0
        self.detectBottomRight = 0
        self.turnCounterLeft = 0
        self.turnCounterRight = 0
        self.spriteOrder = [0] * 5 + [2] * 5
        self.enemySprites = []
        self.damage = 1
        self.health = health
        self.maxHealth = health
        self.coinDrop = coinDrop
        self.attackList = []
        self.isAlive = True

        # Get Sprites
        for i in range(7):
            self.enemySprites.append([2990, 130 * i + 1040, 128, 128])
        for i in range(15):
            self.enemySprites.append([3120, 130 * i, 128, 128])
        for i in range(4):
            self.enemySprites.append([3250, 130 * i, 128, 128])
        self.enemySprites.append([3250, 910, 128, 128])
        self.enemySprites.append([1950, 910, 128, 128])
        for i in range(3):
            self.enemySprites.append([3250, 130 * i + 520, 128, 128])
        self.enemySprites.append([2990, 780, 128, 128])
        self.enemySprites.append([3510, 390, 128, 128])
        for i in range(7):
            self.enemySprites.append([3250, 130 * i + 1040, 128, 128])
        for i in range(15):
            self.enemySprites.append([3380, 130 * i, 128, 128])
        for i in range(2):
            self.enemySprites.append([3510, 130 * i, 128, 128])

        # Species Selection
        self.speciesTypes = {
            "worm": 0, "caterpillar": 3, "snail": 6,
            "pBlob": 9, "gBlob": 13, "bBlob": 17,
            "cube": 21, "gear": 24, "pincher": 27,
            "halfGear": 30, "mouse": 33, "bug": 36,
            "frog": 39, "fly": 42, "rFish": 45,
            "gFish": 48, "bFish": 51, "bee": 54
        }
        if self.species == "rBlob" or self.species == "gBlob" or self.species == "bBlob":
            for i in range(4):
                self.coords.append(self.enemySprites[self.speciesTypes[self.species] + i])
        else:
            for i in range(3):
                self.coords.append(self.enemySprites[self.speciesTypes[self.species] + i])
        for i in range(len(self.coords)):
            self.images.append(self.SS.img(self.coords[i][0], self.coords[i][1],
                                           self.coords[i][2], self.coords[i][3]))
        self.image = pygame.transform.scale(self.images[self.spriteOrder[self.sprite]], (self.size, self.size))
        self.rect = self.image.get_rect()

    def update(self, level, screen):
        self.sprite = (self.sprite + 1) % len(self.spriteOrder)
        self.image = pygame.transform.scale(self.images[self.spriteOrder[self.sprite]], (self.size, self.size))

        # Horizontal Collision Detection
        self.detectLeft = 0
        self.detectRight = 0
        self.detectBottomLeft = 0
        self.detectBottomRight = 0
        for block in level.platformList:
            if (25 >= abs((self.rect.x - block.rect.width) - block.rect.x)
                    and 25 >= abs(block.rect.y - self.rect.y)):
                self.detectLeft += 1
            if (25 >= abs(block.rect.x - (self.rect.x + self.rect.width))
                    and 25 >= abs(block.rect.y - self.rect.y)):
                self.detectRight += 1

            # Cliff Detection
            if 25 >= abs((self.rect.x - 50) - block.rect.x) and 25 >= abs((self.rect.y + 50) - block.rect.y):
                self.detectBottomLeft += 1
            if 25 >= abs((self.rect.x + 50) - block.rect.x) and 25 >= abs((self.rect.y + 50) - block.rect.y):
                self.detectBottomRight += 1

        # Turn timer
        if self.detectLeft > 0 or self.detectBottomLeft == 0:
            self.turnCounterLeft -= 1
        else:
            self.turnCounterLeft = 25
        if self.detectRight > 0 or self.detectBottomRight == 0:
            self.turnCounterRight -= 1
        else:
            self.turnCounterRight = 25
        if self.turnCounterLeft == 0:
            self.isLeft = False
        elif self.turnCounterRight == 0:
            self.isLeft = True
        if self.isLeft:
            self.rect.x -= 1
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x += 1

        # Weapon detection
        self.attackList = pygame.sprite.spritecollide(self, level.weaponList, True)
        for weapon in self.attackList:
            self.health -= weapon.damage
            weapons.cooldown = False
        if self.health <= 0:
            self.kill()
            # Coin drops
            totalValue = random.randint(0,self.coinDrop)
            for i in range(totalValue // 100):
                coin = drops.Coin("gold", self.rect.x + random.randint(1,50), self.rect.y + random.randint(1,30))
                level.dropList.add(coin)
                totalValue -= (totalValue // 100) * 100
            for i in range(totalValue // 10):
                coin = drops.Coin("silver", self.rect.x + random.randint(1,50), self.rect.y + random.randint(1,30))
                level.dropList.add(coin)
                totalValue -= (totalValue // 10) * 10
            for i in range(totalValue):
                coin = drops.Coin("bronze", self.rect.x + random.randint(1,50), self.rect.y + random.randint(1,30))
                level.dropList.add(coin)
        else:
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 1, self.rect.y - 11, self.rect.width + 2, 7))
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * self.health/self.maxHealth, 5))


# Desert boss
class Pinchy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 1000
        self.maxHealth = self.health
        self.coinDrop = 50
        self.damage = 2
        self.attackList = []
        self.images = [[1950, 920, 92, 105], [3268, 673, 92, 105]]
        self.spriteNumber = 0
        self.image = enemySS.img(self.images[self.spriteNumber][0], self.images[self.spriteNumber][1],
                                 self.images[self.spriteNumber][2], self.images[self.spriteNumber][3])
        self.image = pygame.transform.scale(self.image, (50, 57))
        self.rect = self.image.get_rect()
        self.rect.y = 550
        self.counter = -1
        
    def update(self, level, screen):
        global newSlime
        global pinchyX
        global isDefeated
        self.counter += 1
        if not self.counter:
            # Choose position
            self.rect.x = 50 * random.randint(1, 14)
            pinchyX = self.rect.x
        elif self.counter == 36 or self.counter == 72:
            # Change sprite
            self.spriteNumber = 1 - self.spriteNumber
            self.image = enemySS.img(self.images[self.spriteNumber][0], self.images[self.spriteNumber][1],
                                     self.images[self.spriteNumber][2], self.images[self.spriteNumber][3])
        elif 73 <= self.counter <= 75:
            if self.counter == 73 and self.health <= 500:
                # Rage mode: spawn a slime
                newSlime = True
            # Rise up
            self.rect.y -= 180
            self.image = pygame.transform.scale(self.image, (50, 800 - self.rect.y))
        elif 145 <= self.counter <= 150:
            # Go back down
            self.rect.y += 90
            self.image = pygame.transform.scale(self.image, (50, 800 - self.rect.y))
        if self.counter == 150:
            self.counter = -1

        # Weapon detection
        self.attackList = pygame.sprite.spritecollide(self, level.weaponList, True)
        for weapon in self.attackList:
            self.health -= weapon.damage
            weapons.cooldown = False
        if self.health <= 0:
            self.kill()
            # Coin drops
            totalValue = random.randint(1, self.coinDrop)
            for i in range(totalValue // 100):
                coin = drops.Coin("gold", self.rect.x + random.randint(1, 50), 450 + random.randint(1, 30))
                level.dropList.add(coin)
                totalValue -= (totalValue // 100) * 100
            for i in range(totalValue // 10):
                coin = drops.Coin("silver", self.rect.x + random.randint(1, 50), 450 + random.randint(1, 30))
                level.dropList.add(coin)
                totalValue -= (totalValue // 10) * 10
            for i in range(totalValue):
                coin = drops.Coin("bronze", self.rect.x + random.randint(1, 50), 450 + random.randint(1, 30))
                level.dropList.add(coin)
            isDefeated = True
        else:
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 1, self.rect.y - 11, self.rect.width + 2, 7))
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width *
                                                   self.health/self.maxHealth, 5))
