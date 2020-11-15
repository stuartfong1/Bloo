import pygame
import spriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite = 0
        self.SS = spriteSheet.SpriteSheet("p1_walk.png")
        self.leftImages = []
        self.rightImages = []
        self.isWalking = False
        self.isLeft = False
        self.detectLeft = 0
        self.detectRight = 0
        self.ableLeft = True
        self.ableRight = True
        self.collisionList = []
        self.case = 0
        self.moveY = 0
        self.ableJump = True
        self.jumpHeight = 3
        self.jumpArc = [int(height) * 10 for height in range(1, 5)]
        self.health = 100
        self.hitList = []
        self.isAlive = True
        self.collectList = []

        # Get Sprites
        coords = (
            (0, 0, 66, 90),
            (66, 0, 66, 90),
            (133, 0, 66, 90),
            (0, 93, 66, 90),
            (67, 93, 65, 90),
            (132, 93, 72, 90),
            (0, 186, 70, 90),
            (71, 186, 70, 90),
            (142, 186, 72, 90),
            (0, 279, 71, 90),
            (71, 279, 66, 90))
        for i in range(len(coords)):
            self.leftImages.append(pygame.transform.flip(self.SS.img(
                coords[i][0], coords[i][1],
                coords[i][2], coords[i][3]),
                True, False))
            self.rightImages.append(self.SS.img(
                coords[i][0], coords[i][1],
                coords[i][2], coords[i][3]))

        # Default Position
        self.image = self.rightImages[0]
        self.image = pygame.transform.scale(self.image, (36, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 234
        self.rect.y = 460
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()

    def update(self, level, screen):

        # Vertical Collision Detection
        self.rect.y += self.moveY
        self.collisionList = pygame.sprite.spritecollide(self, level.platformList, False)
        for block in self.collisionList:
            if block.index != 3 and block.index != 4:
                if self.moveY > 0 and self.rect.y - block.rect.y < 0:
                    self.rect.bottom = block.rect.top
                    self.ableJump = True
                    self.jumpHeight = 3
                elif self.moveY < 0 and self.rect.y - block.rect.y > 0:
                    self.rect.top = block.rect.bottom

        # Horizontal Collision Detection
        self.detectLeft = 0
        self.detectRight = 0
        self.case = 0
        for block in level.platformList:
            if block.index == 3:
                if (7 >= abs((self.rect.x - block.rect.width) - block.rect.x)
                        and 25 >= abs(block.rect.y - self.rect.y)):
                    self.detectLeft += 1
                if (-block.rect.width < block.rect.x - self.rect.x < self.rect.width
                        and 0 <= block.rect.y - self.rect.y <= self.rect.height):
                    if pygame.sprite.collide_mask(self, block) is not None:
                        self.case = 3
                        self.ableJump = True
                        self.jumpHeight = 3
            elif block.index == 4:
                if (-block.rect.width < block.rect.x - self.rect.x < self.rect.width
                        and 0 <= block.rect.y - self.rect.y <= self.rect.height):
                    if pygame.sprite.collide_mask(self, block) is not None:
                        self.case = 4
                        self.ableJump = True
                        self.jumpHeight = 3
                if (7 >= abs(block.rect.x - (self.rect.x + self.rect.width))
                        and 25 >= abs(block.rect.y - self.rect.y)):
                    self.detectRight += 1
            else:
                if (7 >= abs((self.rect.x - block.rect.width) - block.rect.x)
                        and 25 >= abs(block.rect.y - self.rect.y)):
                    self.detectLeft += 1
                if (7 >= abs(block.rect.x - (self.rect.x + self.rect.width))
                        and 25 >= abs(block.rect.y - self.rect.y)):
                    self.detectRight += 1

        # Movement Restriction
        if self.detectLeft > 0:
            self.ableLeft = False
        else:
            self.ableLeft = True
        if self.detectRight > 0:
            self.ableRight = False
        else:
            self.ableRight = True

        # Moving Animation
        if self.isWalking:
            if self.isLeft:
                self.image = self.leftImages[0]
                if self.sprite == (len(self.leftImages) - 1):
                    self.sprite = 0
                else:
                    self.sprite += 1
                self.image = self.leftImages[self.sprite]
            else:
                self.image = self.rightImages[0]
                if self.sprite == (len(self.rightImages) - 1):
                    self.sprite = 0
                else:
                    self.sprite += 1
                self.image = self.rightImages[self.sprite]

        # Enemy Detection
        self.hitList = pygame.sprite.spritecollide(self, level.enemyList, False)
        for enemy in self.hitList:
            self.health -= enemy.damage
        if self.health <= 0:
            self.isAlive = False
        else:
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 1, self.rect.y - 11, self.rect.width + 2, 7))
            pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rect.width, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rect.width * self.health/100, 5))

        # Update Image
        self.image = pygame.transform.scale(self.image, (36, 50))
        screen.blit(self.image, (self.rect.x, self.rect.y))
