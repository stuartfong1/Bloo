import sys
import pygame
import player
import platforms
import levels
import weapons
import gui
import cutscenes
import spriteSheet
import drops
import enemies

# Setup
pygame.init()
pygame.display.set_caption("Bloo")
Screen = pygame.display.set_mode((800, 600), 0, 32)
# Load spritesheets
platforms.load()
weapons.load()
drops.load()
enemies.load()
# Current level
lvl = levels.Level1()
currentLvl = "Level1"
mc = player.Player()
# GUI
digit1 = gui.Number(1, 1)
digit2 = gui.Number(2, 2)
digit3 = gui.Number(3, 3)
digit4 = gui.Number(4, 4)
value, value1, value2, value3, value4 = [0, 0, 0, 0, 0]
coinIcon = gui.Coin()
bg = pygame.image.load("colored_land.png").convert()
bg = pygame.transform.scale(bg, (800, 600))
menuButton = gui.MenuButton()
# Title screen
title = True
titleLogo = pygame.image.load("Bloo.png").convert_alpha()
titleScroll = -200
titleAcceleration = 5
titleBounce = 10
titleHeight = -titleBounce
titlePhase = False
menu = False
cutscene = True
# Shop
shop = False
purchased = False
ableAfford = False
purchasedItem = None
equipped = 0
preview = -1
equipButton = pygame.image.load("Equip.png").convert_alpha()
blockSS = spriteSheet.SpriteSheet("spritesheet_complete.png")
weaponSS = spriteSheet.SpriteSheet("genericItems.png")
storeInventory = [  # [Name, Price, Image, Weapon type, Damage, isBought, tip]
    ["Spare limb", 1, pygame.image.load("tint1_arm.png").convert_alpha(), "Melee", 60, False,
     "Hopefully it can lend you a hand!"],
    ["Money", 2, weaponSS.img(268, 650, 101, 106), "Ranged", 70, False,
     "The exchange rate is high these days..."],
    ["Toothbrush", 5, weaponSS.img(552, 507, 74, 106), "Melee", 90, False,
     "Recommended by 9/10 dentists!"],
    ["Steering wheel", 10, weaponSS.img(0, 1709, 130, 130), "Ranged", 100, False,
     "Oh, the places you'll go!"],
    ["Rolling pin", 15, weaponSS.img(276, 278, 100, 158), "Melee", 110, False,
     "Just roll with it."]]
itemSelected = -1
font = pygame.font.Font("freesansbold.ttf", 32)
font1 = pygame.font.Font("freesansbold.ttf", 24)
startButton = pygame.image.load("start.png").convert_alpha()
shopkeeper = pygame.image.load("shopkeeper_icon.png").convert_alpha()
shopkeeper = pygame.transform.scale(shopkeeper, (300, 300))
sword = pygame.image.load("sword.png").convert_alpha()
sword = pygame.transform.scale(sword, (25, 25))
buyButton = pygame.image.load("Buy.png").convert_alpha()
xButton = pygame.image.load("brownX.png").convert_alpha()
deathScreen = pygame.image.load("dead.png").convert()


# Calculate coins
def calcValue(amount):
    global value1, value2, value3, value4

    value1 = amount // 1000 % 10
    value2 = amount // 100 % 10
    value3 = amount // 10 % 10
    value4 = amount % 10


# Update
while True:
    if title:
        # Title Screen
        Screen.blit(bg, (0, 0))
        # Animation
        if not titlePhase and titleScroll < 100:
            titleScroll += titleAcceleration
            titleAcceleration += 0.2
        elif not titlePhase:
            titleScroll = 100
            titlePhase = True
        if titlePhase:
            if titleBounce > titleHeight:
                titleScroll -= titleBounce
                titleBounce -= 1
            else:
                titleScroll = 100
                titleBounce = int(titleBounce * -0.5)
                titleHeight = -titleBounce

        Screen.blit(titleLogo, (255, titleScroll))
        Screen.blit(startButton, (300, 275))
    elif not mc.isAlive:
        # Death Screen
        Screen.blit(deathScreen, (0, 0))
        Screen.blit(pygame.transform.scale(blockSS.img(2730, 0, 128, 128), (25, 25)), (200, 350))
        text = font1.render(str(value // 10), True, (255, 255, 255))
        Screen.blit(text, (225, 350))
    elif menu:
        # Inventory
        pygame.draw.rect(Screen, (102, 72, 36), (20, 20, 760, 560))
        pygame.draw.rect(Screen, (211, 147, 79), (30, 30, 740, 540))
        pygame.draw.rect(Screen, (159, 104, 57), (760, 10, 30, 30))
        Screen.blit(xButton, (762, 12))
        for i in range(4):
            for j in range(8):
                pygame.draw.rect(Screen, (159, 104, 57), (70 * j + 50, 70 * i + 50, 50, 50))
                pygame.draw.rect(Screen, (189, 138, 75), (70 * j + 55, 70 * i + 55, 40, 40))
        # Weapons
        for i in range(len(weapons.inventory)):
            Screen.blit(weapons.inventory[i][2], (70 * (i % 8) + 60, 70 * (i // 8) + 60))
        Screen.blit(mc.rightImages[0], (650, 200))
        if len(weapons.inventory) > 0:
            if weapons.inventory[equipped][3] == "Melee":
                Screen.blit(weapons.inventory[equipped][2], (650, 240))
            else:
                Screen.blit(weapons.inventory[equipped][2], (640, 270))
        if preview >= 0:
            # Item preview
            pygame.draw.rect(Screen, (159, 104, 57), (50, 400, 120, 120))
            pygame.draw.rect(Screen, (189, 138, 75), (55, 405, 110, 110))
            Screen.blit(pygame.transform.scale(weapons.inventory[preview][2], (75, 75)), (73, 421))
            # Name
            text = font.render(weapons.inventory[preview][0], True, (102, 72, 36))
            Screen.blit(text, (50, 360))
            # Damage
            Screen.blit(sword, (200, 420))
            text = font1.render(str(weapons.inventory[preview][4]), True, (102, 72, 36))
            Screen.blit(text, (240, 420))
            # Weapon Type
            text = font1.render(weapons.inventory[preview][3], True, (102, 72, 36))
            Screen.blit(text, (200, 460))
            # Tip
            text = font1.render(weapons.inventory[preview][6], True, (102, 72, 36))
            Screen.blit(text, (50, 530))
            # Equip Button
            Screen.blit(equipButton, (320, 420))
    elif cutscene:
        # Intro Cutscene
        if cutscenes.isOver:
            cutscene = False
        else:
            cutscenes.Cutscene.intro(Screen)
    elif shop:
        # Load Shop
        Screen.blit(shopkeeper, (10, 280))
        pygame.draw.rect(Screen, (102, 72, 36), (320, 20, 400, 560))
        pygame.draw.rect(Screen, (211, 147, 79), (330, 30, 380, 540))
        pygame.draw.rect(Screen, (159, 104, 57), (700, 10, 30, 30))
        Screen.blit(xButton, (702, 12))
        pygame.draw.rect(Screen, (102, 72, 36), (10, 20, 300, 250))
        pygame.draw.rect(Screen, (211, 147, 79), (20, 30, 280, 230))
        for i in range(7):
            for j in range(5):
                pygame.draw.rect(Screen, (159, 104, 57), (70 * j + 355, 70 * i + 50, 50, 50))
                pygame.draw.rect(Screen, (189, 138, 75), (70 * j + 360, 70 * i + 55, 40, 40))
        # Display Items
        for i in range(len(storeInventory)):
            storeImage = storeInventory[i][2].get_rect()
            storeInventory[i][2] = pygame.transform.scale(storeInventory[i][2], (40, 40))
            Screen.blit(storeInventory[i][2], (70 * (i % 7) + 360, 70 * (i // 5) + 55))
        # Item Info
        if itemSelected != -1 and itemSelected < len(storeInventory):
            pygame.draw.rect(Screen, (159, 104, 57), (40, 80, 100, 100))
            pygame.draw.rect(Screen, (189, 138, 75), (50, 90, 80, 80))
            Screen.blit(pygame.transform.scale2x(storeInventory[itemSelected][2]), (50, 90))
            text = font.render(storeInventory[itemSelected][0], True, (102, 72, 36))
            Screen.blit(text, (40, 40))
            # Damage
            Screen.blit(sword, (150, 100))
            text = font1.render(str(storeInventory[itemSelected][4]), True, (102, 72, 36))
            Screen.blit(text, (180, 102))
            # Cost
            Screen.blit(pygame.transform.scale(blockSS.img(2730, 0, 128, 128), (25, 25)), (150, 140))
            text = font1.render(str(storeInventory[itemSelected][1]), True, (102, 72, 36))
            Screen.blit(text, (180, 142))
            if storeInventory[itemSelected][5]:
                # Item sold out
                ableAfford = False
                text = font1.render("Sold Out", True, (102, 72, 36))
                Screen.blit(text, (30, 200))
            elif value >= storeInventory[itemSelected][1]:
                # item available
                ableAfford = True
                Screen.blit(buyButton, (30, 200))
            else:
                # Not enough $$$
                text = font1.render("Not enough $$$", True, (102, 72, 36))
                Screen.blit(text, (30, 200))
        else:
            if purchased:
                # Text when item is purchased
                text = font1.render("Purchased " + purchasedItem[0] + ".", True, (102, 72, 36))
                Screen.blit(text, (30, 40))
                text = font1.render("You have " + str(value) + " coins left.", True, (102, 72, 36))
                Screen.blit(text, (30, 70))
            else:
                # Shop open text
                text = font1.render("Welcome to the shop!", True, (102, 72, 36))
                Screen.blit(text, (30, 40))
                text = font1.render("Click on an item that", True, (102, 72, 36))
                Screen.blit(text, (30, 70))
                text = font1.render("you would like to buy.", True, (102, 72, 36))
                Screen.blit(text, (30, 100))
    else:
        # Coin collection
        collectList = pygame.sprite.spritecollide(mc, lvl.dropList, True)
        for i in collectList:
            value += i.value
        calcValue(value)

        lvl.update(Screen)
        if currentLvl == "Level2" and lvl.progress <= -3906:
            # Boss battle teleport
            lvl = levels.PinchyBossArena()
            currentLvl = "pinchyBossArena"
            weapons.cooldown = False
            mc.rect.x = 234
            mc.rect.y = 410
        # Update screen
        if mc.isAlive:
            mc.update(lvl, Screen)
        digit1.update(Screen, value1)
        digit2.update(Screen, value2)
        digit3.update(Screen, value3)
        digit4.update(Screen, value4)
        coinIcon.update(Screen)
        menuButton.update(Screen)
        portalCollideList = pygame.sprite.spritecollide(mc, lvl.portalList, False)
        if len(portalCollideList) > 0:
            text = font.render(portalCollideList[0].destination, True, (102, 72, 36))
            Screen.blit(text, (portalCollideList[0].rect.x, portalCollideList[0].rect.y - 50))
            levels.interactable = "portal"

        # Movement
        mc.moveY = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and mc.jumpHeight >= 0:
            mc.ableJump = False
            mc.moveY = -mc.jumpArc[mc.jumpHeight]
            mc.jumpHeight -= 1
        elif mc.case == 0:
            mc.moveY = 10
        if currentLvl == "pinchyBossArena":
            # Boss Arena
            if keys[pygame.K_LEFT] and mc.ableLeft:
                mc.isWalking = True
                mc.isLeft = True
                mc.rect.x -= 7
                if mc.case == 3:
                    mc.case = 0
                    mc.moveY = 7
                elif mc.case == 4:
                    mc.case = 0
                    mc.moveY = -7
            if keys[pygame.K_RIGHT] and mc.ableRight:
                mc.isWalking = True
                mc.isLeft = False
                mc.rect.x += 7
                if mc.case == 3:
                    mc.case = 0
                    mc.moveY = -7
                if mc.case == 4:
                    mc.case = 0
                    mc.moveY = 7
        else:
            # Regular Movement
            if keys[pygame.K_LEFT] and mc.ableLeft:
                mc.isWalking = True
                mc.isLeft = True
                lvl.shift = 7
                if mc.case == 3:
                    mc.case = 0
                    mc.moveY = 7
                elif mc.case == 4:
                    mc.case = 0
                    mc.moveY = -7
            if keys[pygame.K_RIGHT] and mc.ableRight:
                mc.isWalking = True
                mc.isLeft = False
                lvl.shift = -7
                if mc.case == 3:
                    mc.case = 0
                    mc.moveY = -7
                if mc.case == 4:
                    mc.case = 0
                    mc.moveY = 7
        if keys[pygame.K_SPACE] and not weapons.cooldown:
            if weapons.inventory[equipped][3] == "Melee":
                if mc.isLeft:
                    weapon = weapons.Melee(mc.rect.x, mc.rect.y + 25, mc.rect.x - 1, weapons.inventory[equipped])
                else:
                    weapon = weapons.Melee(mc.rect.x, mc.rect.y + 25, mc.rect.x + 1, weapons.inventory[equipped])
            else:
                if mc.isLeft:
                    weapon = weapons.Ranged(mc.rect.x, mc.rect.y, mc.rect.x - 1, mc.rect.y,
                                            weapons.inventory[equipped])
                else:
                    weapon = weapons.Ranged(mc.rect.x, mc.rect.y, mc.rect.x + 1, mc.rect.y,
                                            weapons.inventory[equipped])
            lvl.weaponList.add(weapon)
        if not (keys[pygame.K_LEFT] and mc.ableLeft) and not (keys[pygame.K_RIGHT] and mc.ableRight):
            mc.isWalking = False
            lvl.shift = 0
            if mc.isLeft:
                mc.image = mc.leftImages[0]
            else:
                mc.image = mc.rightImages[0]

        # Interactables
        if keys[pygame.K_DOWN]:
            if levels.interactable == "shop":
                shop = True
                menuBg = pygame.Surface((800, 600))
                menuBg.set_alpha(128)
                menuBg.fill((0, 0, 0))
                Screen.blit(menuBg, (0, 0))
            elif levels.interactable == "portal":
                if len(portalCollideList) > 0:
                    weapons.cooldown = False
                    if portalCollideList[0].destination == "Town":
                        lvl = levels.Town()
                        currentLvl = "Town"
                        mc.rect.x = 234
                        mc.rect.y = 460
                    if portalCollideList[0].destination == "Desert":
                        lvl = levels.Level2()
                        currentLvl = "Level2"
                        mc.rect.x = 234
                        mc.rect.y = 460

    # Events
    for event in pygame.event.get():
        mousePress = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # When mouse button is clicked
            if title:
                # Start Game
                if 300 <= mousePos[0] <= 500 and 275 <= mousePos[1] <= 325:
                    title = False
            elif not mc.isAlive:
                # Respawn
                if 200 <= mousePos[0] <= 600 and 374 <= mousePos[1] <= 479:
                    value -= int(value * 0.1)
                    mc.isAlive = True
                    mc.health = 100
                    weapons.cooldown = False
                    if currentLvl == "Level1":
                        lvl = levels.Level1()
                    elif currentLvl == "Level2" or currentLvl == "pinchyBossArena":
                        lvl = levels.Level2()
                        currentLvl = "Level2"
                        mc.rect.x = 234
                        mc.rect.y = 410
                    else:
                        lvl = levels.Town()
            elif menu:
                # Inventory
                if 760 <= mousePos[0] <= 790 and 10 <= mousePos[1] <= 40:
                    # Close menu
                    menu = False
                    preview = -1
                elif (50 <= mousePos[0] <= 590 and (mousePos[0] - 50) % 70 <= 50
                      and 50 <= mousePos[1] <= 520 and (mousePos[1] - 50) % 70 <= 50
                      and len(weapons.inventory) >= (mousePos[1] - 50) // 70 * 8 + (mousePos[0] - 50) // 70 + 1):
                    # Preview Item
                    preview = (mousePos[1] - 50) // 70 * 8 + (mousePos[0] - 50) // 70
                elif 320 <= mousePos[0] <= 420 and 420 <= mousePos[1] <= 480 and preview >= 0:
                    equipped = preview
            elif shop:
                if 700 <= mousePos[0] <= 730 and 10 <= mousePos[1] <= 40:
                    # Close shop
                    shop = False
                    itemSelected = -1
                    purchased = False
                elif 360 <= mousePos[0] <= 690 and 50 <= mousePos[1] <= 520:
                    # Select item
                    itemSelected = (mousePos[0] - 360) // 70 + 5 * ((mousePos[1] - 50) // 70)
                    purchased = False
                elif (-1 < itemSelected < len(storeInventory) and ableAfford
                      and 30 <= mousePos[0] <= 80 and 200 <= mousePos[1] <= 230):
                    # Buy item
                    value -= storeInventory[itemSelected][1]
                    purchasedItem = storeInventory[itemSelected]
                    weapons.inventory.append(storeInventory[itemSelected])
                    storeInventory[itemSelected][5] = True
                    purchased = True
                    itemSelected = -1
            else:
                if (menuButton.rect.x <= mousePos[0] <= menuButton.rect.x + menuButton.rect.width
                        and menuButton.rect.y <= mousePos[1] <= menuButton.rect.y + menuButton.rect.height
                        and not shop and not cutscene):
                    # Open menu
                    menu = True
                    menuBg = pygame.Surface((800, 600))
                    menuBg.set_alpha(128)
                    menuBg.fill((0, 0, 0))
                    Screen.blit(menuBg, (0, 0))
                if not weapons.cooldown:
                    # Attack
                    if mousePos[0] - mc.rect.x < 0:
                        mc.isLeft = True
                    else:
                        mc.isLeft = False
                    if weapons.inventory[equipped][3] == "Melee":
                        weapon = weapons.Melee(mc.rect.x, mc.rect.y + 25, mousePos[0], weapons.inventory[equipped])
                    else:
                        weapon = weapons.Ranged(mc.rect.x, mc.rect.y, mousePos[0], mousePos[1],
                                                weapons.inventory[equipped])
                    lvl.weaponList.add(weapon)
        if event.type == pygame.QUIT:
            # Exit game on close
            pygame.quit()
            sys.exit()
    # Update Screen
    pygame.time.Clock().tick(30)
    pygame.display.update()
