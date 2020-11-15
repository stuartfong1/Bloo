import pygame
import spriteSheet
import numpy as np

counter = 0
isOver = False
blackBg = pygame.Surface((800, 600))
blackBg.fill((0, 0, 0))


class Cutscene:
    def intro(screen):
        # Intro cutscene
        global counter
        global isOver
        bg = pygame.image.load("planets.png").convert()
        bg2 = pygame.image.load("space2.png").convert()
        rocket = pygame.image.load("rocket.png").convert_alpha()
        rocket = pygame.transform.scale(rocket, (312, 158))
        shipInterior = pygame.image.load("shipInterior.png").convert()
        warningScreen = pygame.image.load("warningScreen.png").convert()
        exclamationMark = pygame.image.load("!.png").convert_alpha()
        sky = pygame.Surface((800, 600))
        sky.fill((0, 175, 175))
        rocketSS = spriteSheet.SpriteSheet("space_spritesheet.png")
        rocketPart1 = rocketSS.img(1555, 512, 136, 156).convert_alpha()  # Tip
        rocketPart2 = rocketSS.img(1519, 0, 136, 512).convert_alpha()  # Body
        rocketPart3 = rocketSS.img(1763, 0, 93, 169).convert_alpha()  # Wings
        bloo = pygame.transform.scale(spriteSheet.SpriteSheet("p1_walk.png").img(0, 0, 66, 90), (33, 45))
        ground = pygame.Surface((800, 600))
        ground.fill((0, 175, 0))

        if counter <= 200:
            # Rocket floats in space 
            screen.blit(bg, (0, 0))
            screen.blit(rocket, (800 - 3 * counter, 221 + 0.1 * np.rad2deg(np.sin(counter / 10))))
            counter += 1
            if counter >= 150:
                # SCREEN FADE
                blackBg.set_alpha(10 * (counter - 150))
                screen.blit(blackBg, (0, 0))
        elif counter <= 360:
            # Inside rocket
            screen.blit(shipInterior, (0, 0))
            if counter <= 250:
                # NEXT SCENE
                blackBg.set_alpha(5 * (250 - counter))
                screen.blit(blackBg, (0, 0))
            elif counter >= 275 and counter % 10 <= 5:
                # Panel flashes
                screen.blit(warningScreen, (480, 284))
            if counter >= 300:
                # Exclamation mark appears over head
                screen.blit(exclamationMark, (170,300))
        elif counter <= 430:
            # Back in space
            if counter <= 400:
                screen.blit(bg2, (0, 0))
                screen.blit(rocket, (400 - 3 * (counter - 360), 300))
            elif counter >= 410:
                screen.blit(bg2, (0, 0))
                screen.blit(rocket, (277, 300 + 20 * (counter - 410)))
                # Top: 1555, 512, 136, 156
                # Body: 1519, 0, 136, 512
                # Wings: 1763, 0, 93, 169
        elif counter <= 600:
            if counter <= 450:
                screen.blit(sky, (0, 0))
                screen.blit(pygame.transform.rotozoom(rocketPart1, 180, 0.5), (336, 256))
                screen.blit(pygame.transform.rotozoom(rocketPart2, 180, 0.5), (336, 0))
                screen.blit(pygame.transform.rotozoom(rocketPart3, 180, 0.5), (290, 43))
                screen.blit(pygame.transform.rotozoom(pygame.transform.flip(rocketPart3, True, False), 180, 0.5),
                            (405, 43))
            elif counter <= 470:
                screen.blit(sky, (0, 0))
                screen.blit(pygame.transform.rotozoom(rocketPart1, 180, 0.5), (336, 256))
                screen.blit(pygame.transform.rotozoom(rocketPart2, 180, 0.5), (336, 0))
                screen.blit(pygame.transform.rotozoom(rocketPart3, 180, 0.5),
                            (290 - 10 * (counter - 450), 43 - 10 * (counter - 450)))
                screen.blit(pygame.transform.rotozoom(pygame.transform.flip(rocketPart3, True, False), 180, 0.5),
                            (405 + 10 * (counter - 450), 43 - 10 * (counter - 450)))

            elif counter <= 500:
                screen.blit(sky, (0, 0))
                screen.blit(pygame.transform.rotozoom(rocketPart1, 180, 0.5), (336, 256))
                screen.blit(bloo, (360, 200))
                screen.blit(pygame.transform.rotozoom(rocketPart2, 180, 0.5),
                            (336, 0 - 10 * (counter - 470)))
            elif counter <= 550:
                screen.blit(sky, (0, 0))
                screen.blit(pygame.transform.rotozoom(rocketPart1, 180, 0.5), (336, 256 - 10 * (counter - 500)))
                screen.blit(bloo, (360, 200))
            elif counter <= 575:
                screen.blit(sky, (0, 0))
                screen.blit(bloo, (360, 200))
                screen.blit(ground, (0, 600 - 10 * (counter - 550)))
            else:
                isOver = True

        counter += 1
