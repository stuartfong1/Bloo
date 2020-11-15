import pygame
import platforms
import enemies
import random

interactable = None


class Level:
    def __init__(self):
        self.buildingList = pygame.sprite.Group()
        self.platformList = pygame.sprite.Group()
        self.noCollideList = pygame.sprite.Group()
        self.portalList = pygame.sprite.Group()
        self.grassList = pygame.sprite.Group()
        self.enemyList = pygame.sprite.Group()
        self.weaponList = pygame.sprite.Group()
        self.dropList = pygame.sprite.Group()
        self.background = None
        self.shift = 0
        self.worldShift = 0
        self.progress = 0
        self.portalY = []

    def update(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.background, (self.worldShift / 3, -224))
        self.buildingList.draw(screen)
        self.platformList.draw(screen)
        self.noCollideList.draw(screen)
        self.portalList.draw(screen)
        self.grassList.draw(screen)
        self.enemyList.draw(screen)
        self.weaponList.draw(screen)
        self.dropList.draw(screen)
        self.platformList.update()
        self.enemyList.update(self, screen)
        self.weaponList.update(self)
        self.dropList.update(screen)
        if (-672 < self.worldShift < 0
                or self.shift < 0 and self.worldShift >= 0
                or self.shift > 0 and self.worldShift <= -672):
            self.worldShift += self.shift
        self.progress += self.shift
        for building in self.buildingList:
            building.rect.x += self.shift
        for platform in self.platformList:
            platform.rect.x += self.shift
        for noCollide in self.noCollideList:
            noCollide.rect.x += self.shift
        for portal in self.portalList:
            portal.rect.x += self.shift
        for grass in self.grassList:
            grass.rect.x += self.shift
        for enemy in self.enemyList:
            enemy.rect.x += self.shift
            enemy.update(self, screen)
        for weapon in self.weaponList:
            weapon.rect.x += self.shift
        for drop in self.dropList:
            drop.rect.x += self.shift


class Level1(Level):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("colored_land.png")
        pygame.mixer.music.load("Flowerville.ogg")
        pygame.mixer.music.play(-1)
        level = [
            "////////////////////////////////////////////////////////////////////////////////////",
            "/                                                                       /           ",
            "/                                                                       /           ",
            "/                                                                       /           ",
            "/                                                                       /           ",
            "/                                                         e           0 /           ",
            "/                                                        pmPL           /           ",
            "/                                       e                 e l     SbbBBBR/          ",
            "/                           e         SbbbR            SbbbbBR e Ssdddddrbbbbbbbbbb/",
            "/                        LpmmmP      SsdddrR       Sbbbsdddddrbbbsddddddddddddddddd/",
            "/       a  SbbbbbbbbR    l          SsdddddrR     Ssddddddddddddddddddddddddddddddd/",
            "SbbbbbbbBbbsddddddddrbbbbBbbbbbbbbbbsdddddddrbbbbbsdddddddddddddddddddddddddddddddd/"]

        for y, row in enumerate(level):
            for x, item in enumerate(row):
                # ------------------------------------- Regular blocks
                if item == 'b':
                    block = platforms.Platform("dirt", 1, 50)  # Cube dirt
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                    if random.randint(1, 4) == 1:
                        block = platforms.NoCollide("grass", 50)
                        block.rect.x = 50 * x
                        block.rect.y = 50 * (y - 1)
                        self.noCollideList.add(block)
                if item == 'B':
                    block = platforms.Platform("dirt", 1, 50)  # Cube dirt with 100% no grass
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'd':
                    block = platforms.Platform("dirt", 16, 50)  # Dirt with no grass
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == '/':
                    block = platforms.Platform("misc", 190, 50)  # Invisible block
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # ------------------------------------- Angled blocks
                elif item == 'S':
                    block = platforms.Platform("dirt", 3, 50)  # Incline
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 's':
                    block = platforms.Platform("dirt", 9, 50)  # Grass on top-right corner dirt (for inclines)
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'R':
                    block = platforms.Platform("dirt", 4, 50)  # Decline
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'r':
                    block = platforms.Platform("dirt", 10, 50)  # Grass on top-left corner dirt (for declines)
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # -------------------------------------- No-collide blocks
                
                elif item == 'l':
                    block = platforms.Platform("misc", 40, 50)  # Continuing ladder
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == 'L':
                    block = platforms.Platform("misc", 39, 50)  # Ending ladder
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == 'a':
                    block = platforms.Platform("misc", 21, 50)  # Arrow sign
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == '0':
                    block = platforms.Portal("Town")
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.portalList.add(block)
                    self.portalY.append(block.rect.y)
                
                # ------------------------------------- Platforms
                elif item == 'p':
                    block = platforms.Platform("dirt", 7, 50)  # Left platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'm':
                    block = platforms.Platform("dirt", 6, 50)  # Middle platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'P':
                    block = platforms.Platform("dirt", 5, 50)  # Right plaform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'M':
                    block = platforms.Platform("dirt", 8, 50)  # Single platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # -------------------------------------- Enemies
                elif item == 'e':
                    block = enemies.Enemy("worm", 100, 1, 50)  # Worm
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.enemyList.add(block)

    def update(self, screen):
        Level.update(self, screen)
        global interactable
        if -3310 <= self.progress <= -3245:
            interactable = "portal"
        else:
            interactable = None


class Town(Level):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("colored_land.png")

        level = [
            "////////////////////////////////",
            "/                              /",
            "/                              /",
            "/                              /",
            "/                              /",
            "/                              /",
            "/                              /",
            "/              aaa             /",
            "/              <k>    0        /",
            "/              $$$             /",
            "/           SbbbbbbbbbbbbbbbR  /",
            "SbbbbbbbbbbbsdddddddddddddddrbbR"]

        for y, row in enumerate(level):
            for x, item in enumerate(row):
                # ------------------------------------- Regular blocks
                if item == 'b':
                    block = platforms.Platform("stone", 1, 50)  # Cube stone
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'd':
                    block = platforms.Platform("stone", 16, 50)  # stone with no cement
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == '/':
                    block = platforms.Platform("misc", 190, 50)  # Invisible block
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == '0':
                    block = platforms.Portal("Desert")
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.portalList.add(block)
                    self.portalY.append(block.rect.y)
                # ------------------------------------- Angled blocks
                elif item == 'S':
                    block = platforms.Platform("stone", 3, 50)  # Incline
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 's':
                    block = platforms.Platform("stone", 9, 50)  # Cement on top-right corner stone (for inclines)
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'R':
                    block = platforms.Platform("stone", 4, 50)  # Decline
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'r':
                    block = platforms.Platform("stone", 10, 50)  # Cement on top-left corner stone (for declines)
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # ------------------------------------- Platforms
                elif item == 'p':
                    block = platforms.Platform("stone", 7, 50)  # Left platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'm':
                    block = platforms.Platform("stone", 6, 50)  # Middle platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'P':
                    block = platforms.Platform("stone", 5, 50)  # Right plaform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'M':
                    block = platforms.Platform("stone", 8, 50)  # Single platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # -------------------------------------- Shop parts
                elif item == 'a':
                    block = platforms.Building(2, 5, 50)  # Awning
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == '>':
                    block = platforms.Building(0, 3, 50)  # Left pole
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == '<':
                    block = platforms.Building(2, 3, 50)  # Right pole
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == 'k':
                    block = platforms.Shopkeeper(50)  # Shopkeeper
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == '$':
                    block = platforms.Platform("misc", 66, 50)  # Shop stand
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)

    def update(self, screen):
        Level.update(self, screen)
        global interactable
        if -650 <= self.progress <= -500:
            interactable = "shop"
        elif -910 <= self.progress <= -833:
            interactable = "portal"
        else:
            interactable = None


class Level2(Level):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("colored_desert.png")

        level = [
            "////////////////////////////////////////////////////////////////////////////////////////////////////",
            "/                                                                                                  /",
            "/                                                                                                  /",
            "/                                                                                                  /",
            "/                                                                                                  /",
            "/                                                                                                  /",
            "/                                                                                                  /",
            "/                                                                                                  /",
            "/                   e   e                                                                          /",
            "/                 SbbbbbbbR      e               eee  e                   e                        /",
            "/SbbbbbbR  e e SbbsdddddddrbbbbbbbbbR          SbbbbbbbbR   e   e   SbbbbbbbbR                     /",
            "SsddddddrbbbbbbsddddddddddddddddddddrbbbbbbbbbbsddddddddrbbbbbbbbbbbsddddddddrBBBBBBBBBBBBBBBBBBBBBR"]

        for y, row in enumerate(level):
            for x, item in enumerate(row):
                # ------------------------------------- Regular blocks
                if item == 'b':
                    block = platforms.Platform("sand", 1, 50)  # Cube sand with fluffy sand
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                    if random.randint(1, 10) == 1:
                        block = platforms.NoCollide("cactus", 50)
                        if random.randint(0, 1) == 0:
                            block.image = pygame.transform.flip(block.image, True, False)
                        block.rect.x = 50 * x
                        block.rect.y = 50 * (y - 1)
                        self.noCollideList.add(block)
                if item == 'B':
                    block = platforms.Platform("sand", 1, 50)  # 100% no cactus spawn fluffy sand
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'd':
                    block = platforms.Platform("sand", 16, 50)  # Sand with fluffy sand
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == '/':
                    block = platforms.Platform("misc", 190, 50)  # Invisible block
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # ------------------------------------- Angled blocks
                elif item == 'S':
                    block = platforms.Platform("sand", 3, 50)  # Incline
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 's':
                    block = platforms.Platform("sand", 9, 50)  # Fluffy sand on top-right corner sand (for inclines)
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'R':
                    block = platforms.Platform("sand", 4, 50)  # Decline
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'r':
                    block = platforms.Platform("sand", 10, 50)  # Fluffy sand on top-left corner sand (for declines)
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # -------------------------------------- No-collide blocks
                
                elif item == 'l':
                    block = platforms.Platform("misc", 40, 50)  # Continuing ladder
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == 'L':
                    block = platforms.Platform("misc", 39, 50)  # Ending ladder
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                elif item == 'a':
                    block = platforms.Platform("misc", 21, 50)  # Arrow sign
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.noCollideList.add(block)
                
                # ------------------------------------- Platforms
                elif item == 'p':
                    block = platforms.Platform("sand", 7, 50)  # Left platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'm':
                    block = platforms.Platform("sand", 6, 50)  # Middle platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'P':
                    block = platforms.Platform("sand", 5, 50)  # Right plaform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'M':
                    block = platforms.Platform("sand", 8, 50)  # Single platform
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # -------------------------------------- Enemies
                elif item == 'e':
                    block = enemies.Enemy("mouse", 150, 3, 50)  # Mouse
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.enemyList.add(block)

    def update(self, screen):
        Level.update(self, screen)


class PinchyBossArena(Level):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load("colored_desert.png")

        level = [
            "/////////////////",
            "/e             /",
            "/              /",
            "/              /",
            "/              /",
            "/              /",
            "/              /",
            "/              /",
            "/              /",
            "/              /",
            "BBBBBBBBBBBBBBBB",
            "dddddddddddddddd"]

        for y, row in enumerate(level):
            for x, item in enumerate(row):
                # ------------------------------------- Regular blocks
                if item == 'B':
                    block = platforms.Platform("sand", 1, 50)  # 100% no cactus fluffy sand
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == 'd':
                    block = platforms.Platform("sand", 16, 50)  # Sand without fluffy sand
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                elif item == '/':
                    block = platforms.Platform("misc", 190, 50)  # Invisible block
                    block.rect.x = 50 * x
                    block.rect.y = 50 * y
                    self.platformList.add(block)
                # -------------------------------------- Enemies
                elif item == 'e':
                    block = enemies.Pinchy()  # Boss
                    self.enemyList.add(block)

    def update(self, screen):
        Level.update(self, screen)
        if enemies.newSlime:
            # Spawn slime
            block = enemies.Enemy("pBlob", 200, 0, 50)
            block.rect.x = enemies.pinchyX
            block.rect.y = 450
            self.enemyList.add(block)
            enemies.newSlime = False
        if enemies.isDefeated:
            # Create portal
            block = platforms.Portal("Town")
            block.rect.x = 650
            block.rect.y = 400
            self.portalList.add(block)
            enemies.isDefeated = False
