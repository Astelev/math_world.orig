import pygame
from imagefunk import load_image, Anim
import random


class Enemy:
    def __init__(self, x, y, person, size=50, name="enemy"):
        # загрузка анимаций
        self.image = load_image("enemy.png")
        self.left = load_image("enemyl.png")
        self.runright = Anim("runright_enemy", 1)
        self.runleft = Anim("runlefte_enemy", 1)
        self.atak = Anim("enemy_atak", 1)
        self.atakl = Anim("runlefte_enemy", 1)
        self.person = person
        self.name = name
        self.x = x
        self.vx = 0
        self.vy = 0
        self.y = y
        self.sizey = size
        self.sizex = 50
        self.do = ["", 0]
        self.hp = 100
        self.movable = False
        self.damageble = True
        self.drop = ["number", 10]

    def status_set(self, do, status=True):
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def display(self, x, y, screen, collision):
        if self.do[0] != "dead":
            if abs(self.person.x - self.x) < 1400 and abs(self.person.y - self.y) < 500:
              self.agr()
        if self.do[0] == "attack":
            if self.do[1] < 50:
                self.do[1] = self.do[1] + 1
            else:
                self.person.damag(50)
                self.do[1] = 0
        c = True
        chek = True
        for i in collision:
            col = i.collision_chek(self.x, self.y, self.sizex, self.sizey)
            if "x+" in col and self.vx >= 0:
                self.vx = 0
                if self.do[0] != "jump":
                    self.vy = -13.5
            elif "x-" in col and self.vx <= 0:
                self.vx = 0
                if self.do[0] != "jump":
                    self.vy = -13.5
            if "y+" in col and self.vy >= 0:
                self.vy = 0
                c = False
                if self.do[0] != "moveright" and self.do[0] != "moveleft":
                    self.vx = 0
            elif "y-" in col and self.vy <= 0:
                self.vy = 0
            if self.do[0] != "jump":
                colleft = i.collision_chek(self.x - 20, self.y, 0, self.sizey)
                colright = i.collision_chek(self.x + 20, self.y, self.sizex, self.sizey)
                if ("y+" in colleft and self.person.x < self.x) or (
                      "y+" in colright and self.person.x > self.x):
                    chek = False
            else:
                chek = False
        if chek:
            self.vx = 0
        if c:
            self.status_set("jump", True)
        else:
            self.status_set("jump", False)
        self.x = self.x + self.vx
        if self.do[0] == "jump":
            self.y = self.y + self.vy
            self.vy = self.vy + 0.5
            if self.person.x < self.x:
                screen.blit(self.left, (self.x - x, self.y - y))
            else:
                screen.blit(self.image, (self.x - x, self.y - y))
        elif self.do[0] == "moveright":
            self.runright.framedraw(screen, self.x - x, self.y - y)
        elif self.do[0] == "moveleft":
            self.runleft.framedraw(screen, self.x - x, self.y - y)
        elif self.do[0] == "attack":
            if self.person.x < self.x:
                self.atakl.framedraw(screen, self.x - x, self.y - y)
            else:
                self.atak.framedraw(screen, self.x - x, self.y - y)
        else:
            screen.blit(self.image, (self.x - x, self.y - y))
        pygame.draw.rect(screen, (255, 255, 255), (self.x - x, self.y - y - 20, self.hp // 2, 10))
        pygame.draw.rect(screen, (0, 100, 100), (self.x - x - 3, self.y - y - 23, 56, 16), 1)

    def agr(self):
        if abs(self.person.x - self.x) > 60:
            if self.person.x < self.x:
                  self.vx = -3
                  if self.do[0] != "jump":
                        self.status_set("moveleft")
            elif self.person.x > self.x:
                  self.vx = 3
                  if self.do[0] != "jump":
                        self.status_set("moveright")
        elif abs(self.person.y - self.y) < 100:
            self.status_set("attack", True)

    def damag(self, level):
        self.hp -= level
        if self.hp <= 0:
            self.status_set("dead", True)
    def data_return(self):
        return "Enemy" + " " + str(self.x) + " " + \
          str(self.y) + " " + str(self.hp)


class Enemystr:
    def __init__(self, x, y, person, count, size=50, name=""):
        # загрузка анимаций
        self.c = count
        self.image = load_image("enemy.png")
        self.left = load_image("enemyl.png")
        self.runright = Anim("runright_enemy", 1)
        self.runleft = Anim("runlefte_enemy", 1)
        self.atak = Anim("enemy_atak", 1)
        self.atakl = Anim("runlefte_enemy", 1)
        self.person = person
        self.name = str(count)
        self.x = x
        self.vx = 0
        self.vy = 0
        self.y = y
        self.sizey = size
        self.sizex = 50
        self.speed = random.randint(3,5)
        self.do = ["", 0]
        self.hp = 80
        self.hpmax = 80
        self.damage = 50
        if self.name == "/":
            self.hp = 150
            self.hpmax = 150
            self.damage = 100
        self.movable = False
        self.damageble = True
        self.drop = ["Number", str(self.c)]

    def status_set(self, do, status=True):
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def display(self, x, y, screen, collision):
        if self.do[0] != "dead":
            if abs(self.person.x - self.x) < 1000 and abs(self.person.y - self.y) < 500:
              self.agr()
        if self.do[0] == "attack":
            if self.do[1] < 50:
                self.do[1] = self.do[1] + 1
            else:
                self.person.damag(50)
                self.do[1] = 0
        c = True
        chek = True
        for i in collision:
            if abs(i.x - self.x) < i.sizex + self.sizex and abs(i.y - self.y) < i.sizey + self.sizey:
                col = i.collision_chek(self.x, self.y, self.sizex, self.sizey)
                if "x+" in col and self.vx >= 0:
                    self.vx = 0
                    if self.do[0] != "jump":
                        self.vy = -13.5
                elif "x-" in col and self.vx <= 0:
                    self.vx = 0
                    if self.do[0] != "jump":
                        self.vy = -13.5
                if "y+" in col and self.vy >= 0:
                    self.vy = 0
                    c = False
                    if self.do[0] != "moveright" and self.do[0] != "moveleft":
                        self.vx = 0
                elif "y-" in col and self.vy <= 0:
                    self.vy = 0
                if self.do[0] != "jump":
                    colleft = i.collision_chek(self.x - 20, self.y, 0, self.sizey + 150)
                    colright = i.collision_chek(self.x + 20, self.y, self.sizex, self.sizey + 150)
                    if ("y+" in colleft and self.person.x < self.x) or (
                          "y+" in colright and self.person.x > self.x):
                        chek = False
                else:
                    chek = False
        if chek:
            self.vx = 0
        if c:
            self.status_set("jump", True)
        else:
            self.status_set("jump", False)
        self.x = self.x + self.vx
        if self.do[0] == "jump":
            self.y = self.y + self.vy
            self.vy = self.vy + 0.5
        font = pygame.font.Font(None, self.sizex)
        text = font.render(str(self.c), True, (255, 255, 255))
        screen.blit(text, (self.x - x, self.y - y))
        pygame.draw.rect(screen, (255, 255, 255), (self.x - x, self.y - y - 20, self.hp // 2, 10))
        pygame.draw.rect(screen, (0, 100, 100), (self.x - x - 3, self.y - y - 23, self.hpmax // 2 + 6, 16), 1)

    def agr(self):
        if abs(self.person.x - self.x) > 60:
            if self.person.x < self.x:
                  self.vx = -self.speed
                  if self.do[0] != "jump":
                        self.status_set("moveleft")
            elif self.person.x > self.x:
                  self.vx = self.speed
                  if self.do[0] != "jump":
                        self.status_set("moveright")
        elif abs(self.person.y - self.y) < 100:
            self.status_set("attack", True)

    def damag(self, level):
        self.hp -= level
        if self.hp <= 0:
            self.status_set("dead", True)
    def data_return(self):
        if self.c == "×":
            return "Enemystr" + " " + str(self.x) + " " + \
              str(self.y) + " " + str(self.hp) + " " + "*"
        else:
            return "Enemystr" + " " + str(self.x) + " " + \
                str(self.y) + " " + str(self.hp) + " " + str(self.c)
