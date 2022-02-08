import random
import sys

import pygame
import pygame_gui
from pygame import Rect
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine

import parser


class GameState:
    def __init__(self, name):
        self.debugMode = False
        self.name = name
        self.reset()

    def reset(self):
        self.alive = True
        self.count = 0
        self.gameSpeed = 4
        self.ran20 = False
        self.ran70 = False
        self.ran150 = False
        self.ran300 = False
        self.ran500 = False
        self.ran750 = False
        self.ran1000 = False
        self.ran1250 = False
        self.ran1500 = False
        self.ran1750 = False

    def Update(self):
        if 20 <= self.count <= 69 and not self.ran20:
            self.gameSpeed = 5
            self.ran20 = True
        if 70 <= self.count <= 149 and not self.ran70:
            self.gameSpeed = 6
            self.ran70 = True
        if 150 <= self.count <= 299 and not self.ran150:
            self.gameSpeed = 7
            self.ran150 = True
        if 300 <= self.count <= 499 and not self.ran300:
            self.gameSpeed = 8
            self.ran300 = True
        if 500 <= self.count <= 749 and not self.ran500:
            self.gameSpeed = 9
            self.ran500 = True
        if 750 <= self.count <= 999 and not self.ran750:
            self.gameSpeed = 10
            self.ran750 = True
        if 1000 <= self.count <= 1249 and not self.ran1000:
            self.gameSpeed = 11
            self.ran1000 = True
        if 1250 <= self.count <= 1499 and not self.ran1250:
            self.gameSpeed = 12
            self.ran1250 = True
        if 1500 <= self.count <= 1749 and not self.ran1500:
            self.gameSpeed = 13
            self.ran1500 = True
        if 1750 <= self.count <= 1999 and not self.ran1750:
            self.gameSpeed = 14
            self.ran1750 = True
        if self.count >= 2000:
            self.gameSpeed += 0.002


class Background:
    def __init__(self, texture):
        self.texture = pygame.image.load(texture)
        self.rect = self.texture.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = 0
        self.rect.y = 450

    def Update(self, events, gamestate):
        self.rect.x -= gamestate.gameSpeed
        if self.rect.x <= -self.rect.width + 885:
            self.reset()

    def Draw(self, screen):
        screen.blit(self.texture, self.rect)


class Cloud:
    def __init__(self, texture):
        self.texture = pygame.image.load(texture)
        self.rect = self.texture.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(1000, 2700)
        self.rect.y = random.randint(60, 100)

    def Update(self, events, gamestate):
        self.rect.x -= gamestate.gameSpeed / 2
        if self.rect.x < -100:
            self.reset()

    def Draw(self, screen):
        screen.blit(self.texture, self.rect)


class Cactus:
    def __init__(self, texture):
        self.texture = pygame.image.load(texture)
        self.rect = self.texture.get_rect()
        self.afterhalf = False
        self.reset()

    def reset(self):
        self.rect.x = random.randint(850, 2600)
        self.rect.y = 470 - self.rect.height
        self.afterhalf = False

    def Update(self, events, gamestate, hero):
        self.rect.x -= gamestate.gameSpeed
        if self.rect.x < -120:
            self.reset()
        if (200 < self.rect.x < 225) and (self.afterhalf is False) and (not self.Intersects(hero)):
            self.afterhalf = True
            gamestate.count += 5

    def Draw(self, screen):
        screen.blit(self.texture, self.rect)

    def Intersects(self, Gobject):
        return Gobject.Intersects(self)


class Pterodactyl:
    def __init__(self, texture):
        self.texture = pygame.image.load(texture)
        self.images = list()
        for x in range(2):
            self.images.append(pygame.image.load(f"img\\bird_anim\\bird{x}.png"))
        self.rect = self.texture.get_rect()
        self.currentFrame = 0
        self.updates = 0
        self.afterhalf = False
        self.reset()

    def reset(self):
        self.rect.x = random.randint(3700, 5700)
        self.rect.y = random.randint(350, 440 - self.rect.height)
        self.afterhalf = False

    def Update(self, events, gamestate, hero):
        self.updates += 1
        if self.updates == 40:
            self.updates = 0
            self.currentFrame += 1
        if self.currentFrame > 1:
            self.currentFrame = 0
        self.rect.x -= gamestate.gameSpeed * 1.08
        if self.rect.x < -120:
            self.reset()
        if (200 < self.rect.x < 225) and (self.afterhalf is False) and (not self.Intersects(hero)):
            self.afterhalf = True
            gamestate.count += 5

    def Draw(self, screen):
        screen.blit(self.images[self.currentFrame], self.rect)

    def Intersects(self, Gobject):
        return Gobject.Intersects(self)


class Hero:
    def __init__(self, texture):
        self.texture = pygame.image.load(texture)
        self.images = list()
        for x in range(4):
            self.images.append(pygame.image.load(f"img\\anim\\frame_{x}.png"))
        self.images.append(pygame.image.load(f"img\\dino_jump.png"))
        self.images.append(pygame.image.load(f"img\\dino_dead.png"))
        self.images.append(pygame.image.load(f"img\\dino_godmode.png"))
        self.rect = self.texture.get_rect()
        self.currentFrame = 0
        self.updates = 0
        self.godmode = False
        self.last = pygame.time.get_ticks()
        self.cooldown = 2250
        self.reset()

    def reset(self):
        self.rect.x = 200
        self.hp = 100
        self.jumping = False
        self.godmode = False
        self.velocity = 8
        self.rect.y = 470 - self.rect.height

    def Update(self, events, cacti, gameState, pterodactyl, bonuses):
        self.debug_currentFrame = font.render(f"Fr {self.currentFrame} upd {self.updates}", True, [255, 0, 0])
        self.debug_godmode = font.render(f"gm {self.godmode}", True, [255, 0, 0])

        keys = pygame.key.get_pressed()

        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            self.currentFrame = 0
            self.godmode = False

        for i in events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_F3:
                    if gameState.debugMode:
                        gameState.debugMode = False
                    else:
                        gameState.debugMode = True

        if keys[pygame.K_SPACE] and not self.jumping and not keys[pygame.K_DOWN]:
            self.jumping = True
        if self.jumping:
            if not self.godmode:
                self.currentFrame = 4
            self.rect.y -= self.velocity
            if keys[pygame.K_SPACE]:
                self.velocity -= 0.2
            else:
                self.velocity -= 0.5
            if self.rect.y > 470 - self.rect.height:
                self.jumping = False
                self.rect.y = 470 - self.rect.height
                self.velocity = 8
                self.updates = 0
        elif self.godmode:
            self.currentFrame = 6
        else:
            self.updates += 1
            if self.updates == 20:
                self.updates = 0
                self.currentFrame += 1
            if self.currentFrame > 1:
                self.currentFrame = 0

            if keys[pygame.K_DOWN]:
                self.currentFrame = 2
                self.rect.y = 495 - self.rect.height
            else:
                self.rect.y = 470 - self.rect.height

        for cactus in cacti:
            if self.Intersects(cactus) and not self.godmode:
                self.hp -= 2
                if self.hp <= 0:
                    self.hp = 0
                    self.rect.y = 470 - self.rect.height
                    self.currentFrame = 5
                    gameState.alive = False
                    parser.save_score(name, gameState)

        if self.Intersects(pterodactyl) and not self.godmode:
            self.hp -= 3
            if self.hp <= 0:
                self.hp = 0
                self.rect.y = 470 - self.rect.height
                self.currentFrame = 5
                gameState.alive = False
                parser.save_score(name, gameState)

        for bonus in bonuses:
            if isinstance(bonus, HealBonus) and self.Intersects(bonus):
                if self.hp <= 79:
                    self.hp += 20
                else:
                    self.hp = 100
            if isinstance(bonus, TimeBonus) and self.Intersects(bonus):
                if gameState.gameSpeed >= 5:
                    gameState.gameSpeed = round(gameState.gameSpeed - 0.4, 1)
                else:
                    gameState.gameSpeed = 4
            if isinstance(bonus, GodModeBonus) and self.Intersects(bonus):
                self.last = pygame.time.get_ticks()
                self.godmode = True

    def Draw(self, screen):
        screen.blit(self.images[self.currentFrame], self.rect)
        if gameState.debugMode:
            screen.blit(self.debug_currentFrame, (660, 100))
            screen.blit(self.debug_godmode, (660, 130))
        pygame.draw.rect(screen, (88, 88, 88), Rect(48, 18, 404, 34))
        pygame.draw.rect(screen,
                         (255 - (self.hp // 100) * 255,
                          (((self.hp * 3) // 100) * 255) % 256, 0),
                         Rect(50, 20, 4 * self.hp, 30))
        if hero.hp == 100:
            pygame.draw.rect(screen, (88, 88, 88), Rect(459, 25, 33, 20))
        elif 10 <= hero.hp <= 99:
            pygame.draw.rect(screen, (88, 88, 88), Rect(459, 25, 26, 20))
        else:
            pygame.draw.rect(screen, (88, 88, 88), Rect(459, 25, 14, 20))
        screen.blit(text_hp, (52, 22))
        screen.blit(text_hp_value, (460, 22))

    def Intersects(self, Gobject):
        a = self.rect
        b = Gobject.rect
        xInter = a.x <= b.x <= a.x + a.width
        if isinstance(Gobject, Pterodactyl):
            yInter = a.y <= b.y <= a.y + a.height
        else:
            yInter = b.y <= a.y + a.height
        res = xInter and yInter
        return res


class Bonus:
    def __init__(self, texture):
        self.texture = pygame.image.load(texture)
        self.rect = self.texture.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(7000, 12000)
        self.rect.y = 470 - self.rect.height

    def Update(self, events, gamestate, cacti):
        self.rect.x -= gamestate.gameSpeed
        for cactus in cacti:
            if self.rect.x < -100 or cactus.rect.x - 15 <= self.rect.x <= cactus.rect.x + 15:
                self.reset()

    def Draw(self, screen, hero):
        screen.blit(self.texture, self.rect)
        if self.Intersects(hero):
            self.reset()

    def Intersects(self, Gobject):
        a = self.rect
        b = Gobject.rect
        xInter = a.x - a.width <= b.x <= a.x + a.width
        yInter = a.y - a.height <= b.y <= a.y + a.height
        res = xInter and yInter
        return res


class HealBonus(Bonus):
    def reset(self):
        self.rect.x = random.randint(7000, 12000)
        self.rect.y = 470 - self.rect.height


class TimeBonus(Bonus):
    def reset(self):
        self.rect.x = random.randint(15000, 17000)
        self.rect.y = 470 - self.rect.height


class GodModeBonus(Bonus):
    def reset(self):
        self.rect.x = random.randint(18000, 22000)
        self.rect.y = 470 - self.rect.height


def draw(screen, gamestate):
    global text_hp_value
    if not gamestate.alive:
        text = fontdead.render("Game Over! Press R", True, [230, 10, 10])
        screen.blit(text, (400 - text.get_rect().width // 2, 250 - text.get_rect().height // 2))
    counter = fontdead.render(f"SC {gamestate.count}", True, [88, 88, 88])
    if hero.hp > 99:
        text_hp_value = font.render(f"{hero.hp}", True, [10, 230, 10])
    elif 33 < hero.hp <= 98:
        text_hp_value = font.render(f"{hero.hp}", True, [255, 255, 0])
    else:
        text_hp_value = font.render(f"{hero.hp}", True, [230, 10, 10])
    if 0 <= gamestate.count <= 9:
        screen.blit(counter, (680, 5))
    elif 10 <= gamestate.count <= 99:
        screen.blit(counter, (655, 5))
    elif 100 <= gamestate.count <= 999:
        screen.blit(counter, (630, 5))
    elif 1000 <= gamestate.count <= 9999:
        screen.blit(counter, (605, 5))
    background.Draw(screen)
    for cactus in cacti:
        cactus.Draw(screen)
    pterodactyl.Draw(screen)
    hero.Draw(screen)
    cloud.Draw(screen)
    for bonus in bonuses:
        bonus.Draw(screen, hero)
    debug_gameSpeed = font.render(f"sp {gamestate.gameSpeed}", True, [255, 0, 0])
    if gameState.debugMode:
        screen.blit(debug_gameSpeed, (660, 115))


def update(gameState):
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_ESCAPE:
                menu()
        elif i.type == pygame.QUIT:
            sys.exit()

    if not gameState.alive:
        for i in events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_r:
                    gameState.reset()
                    hero.reset()
                    for cactus in cacti:
                        cactus.reset()
                    pterodactyl.reset()
                    for bonus in bonuses:
                        bonus.reset()
                    cloud.reset()
                    background.reset()
    else:
        background.Update(events, gameState)
        for cactus in cacti:
            cactus.Update(events, gameState, hero)
        pterodactyl.Update(events, gameState, hero)
        hero.Update(events, cacti, gameState, pterodactyl, bonuses)
        cloud.Update(events, gameState)
        for bonus in bonuses:
            bonus.Update(events, gameState, cacti)
        gameState.Update()


def mainloop():
    while True:
        clock.tick(120)
        screen.fill((248, 248, 248))
        update(gameState)
        draw(screen, gameState)
        pygame.display.update()


def button(screen, position, text):
    font = pygame.font.Font("Hardpixel.ttf", 30)
    text_render = font.render(text, True, (83, 83, 83))
    text_rect = text_render.get_rect()
    text_rect.x, text_rect.y = position
    pygame.draw.line(screen, (150, 150, 150), (text_rect.x, text_rect.y), (text_rect.x + 125, text_rect.y), 5)
    pygame.draw.line(screen, (150, 150, 150), (text_rect.x, text_rect.y - 2), (text_rect.x, text_rect.y + text_rect.h),
                     5)
    pygame.draw.line(screen, (50, 50, 50), (text_rect.x, text_rect.y + text_rect.h),
                     (text_rect.x + 125, text_rect.y + text_rect.h), 5)
    pygame.draw.line(screen, (50, 50, 50), (text_rect.x + 125, text_rect.y + text_rect.h),
                     [text_rect.x + 125, text_rect.y], 5)
    pygame.draw.rect(screen, (170, 170, 170), (text_rect.x, text_rect.y, 125, text_rect.h))
    return screen.blit(text_render, (text_rect.x, text_rect.y))


def scoreboard_menu():
    global screen, clock, cacti, pterodactyl, hero, gameState, cloud, background, bonuses, font, fontdead, text_hp, scoreboard_bg_img
    screen.blit(scoreboard_bg_img, (0, 0))
    b1 = button(screen, (10, 120), "Back")
    data = parser.get_scores_from_file('score.txt')
    top5 = font.render(f"Top 5 best players", True, [60, 60, 60])
    players = []
    has_records = False
    if 0 < len(data) < 5:
        for i in range(len(data)):
            players.append(
                font.render(f"{i + 1}. {data[i]['name']} — {data[i]['score']} ({data[i]['date']} {data[i]['time']})",
                            True, [83, 83, 83]))
            has_records = True
    elif len(data) <= 0:
        players.append(font.render(f"So far, no one has set a record. Be the first!", True, [83, 83, 83]))
    else:
        for i in range(5):
            players.append(
                font.render(f"{i + 1}. {data[i]['name']} — {data[i]['score']} ({data[i]['date']} {data[i]['time']})",
                            True, [83, 83, 83]))
            has_records = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    menu()
        screen.blit(top5, (305, 130))
        y_pos = 175
        for player in players:
            if has_records:
                screen.blit(player, (230, y_pos))
            else:
                screen.blit(player, (165, y_pos))
            y_pos += 50
        pygame.display.update()


def menu():
    global screen, clock, cacti, pterodactyl, hero, gameState, cloud, background, bonuses, font, fontdead, text_hp, menu_bg_img, name
    screen.blit(menu_bg_img, (0, 0))
    b1 = button(screen, (350, 400), "Quit")
    b2 = button(screen, (350, 200), "Start")
    b3 = button(screen, (350, 300), "Score")
    enter_name = font.render(f"Enter your name and press Enter key", True, [83, 83, 83])
    manager = pygame_gui.UIManager((800, 500))
    text_input = UITextEntryLine(relative_rect=Rect(310, 160, 200, 30), manager=manager)
    while True:
        screen.blit(enter_name, (210, 135))
        time_delta = clock.tick(60) / 1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not gameState.alive:
                    pygame.quit()
                if event.key == pygame.K_ESCAPE and gameState.alive:
                    mainloop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    mainloop()
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    scoreboard_menu()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == text_input:
                        name = text_input.get_text()
                        name_successful = font.render(f"Have a good game, {name}!", True, [130, 130, 130])
                        screen.blit(name_successful, (10, 470))
            manager.process_events(event)
        manager.update(time_delta)
        screen.blit(screen, (0, 0))
        manager.draw_ui(screen)
        pygame.display.update()


pygame.init()
pygame.display.set_caption('Chrome Dino')
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()

programIcon = pygame.image.load('dino.ico')
menu_bg_img = pygame.image.load("img\\menu_bg.png")
scoreboard_bg_img = pygame.image.load("img\\scoreboard_bg.png")

pygame.display.set_icon(programIcon)

cacti = list()

cacti.append(Cactus("img\\cactus1.png"))
cacti.append(Cactus("img\\cactus2.png"))
cacti.append(Cactus("img\\cactus3.png"))
cacti.append(Cactus("img\\cactus4.png"))
cacti.append(Cactus("img\\cactus5.png"))

pterodactyl = Pterodactyl("img\\bird_anim\\bird0.png")

hero = Hero("img\\dino_jump.png")
name = "Player"
gameState = GameState(name)

cloud = Cloud("img\\cloud.png")
background = Background('img\\bg.png')

bonuses = list()

bonuses.append(HealBonus("img\\heart.png"))
bonuses.append(TimeBonus("img\\hourglass.png"))
bonuses.append(GodModeBonus("img\\wing.png"))

font = pygame.font.Font("Hardpixel.ttf", 20)
fontdead = pygame.font.Font("Hardpixel.ttf", 50)
text_hp = font.render("Health", True, [161, 155, 155])
text_hp_value = font.render("", True, [0, 0, 0])

if __name__ == '__main__':
    menu()
