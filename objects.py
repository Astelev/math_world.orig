import pygame
from imagefunk import load_image, Anim


class Number:
    def __init__(self, count, x, y, size=50, name=""):
        self.c = count
        self.name = str(count)
        self.x = x
        self.y = y
        self.sizex = size
        self.sizey = size
        self.do = ["", 0]
        self.movable = True
        self.damageble = False
        self.usable = False

    def display(self, x, y, screen, colis, fps):
        font = pygame.font.Font(None, self.sizex)
        text = font.render(str(self.c), True, (255, 255, 255))
        screen.blit(text, (self.x - x, self.y - y))

    def display_into_inventar(self, screen, x, y, sizex, sizey):
        font = pygame.font.Font(None, sizex - 2)
        text = font.render(str(self.c), True, (255, 255, 255))
        screen.blit(text, (x, y))

    def moveing(self, x, y, camx, camy):
        self.x = camx + x - self.sizex // 2
        self.y = camy + y - self.sizey // 2
        self.status_set("move", True)

    def status_set(self, do, status=True):
        # задать статус для анимаций
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def data_return(self):
        if self.c == "×":
            return "Number" + " " + "*" + " " + str(self.x) + " " + str(self.y)
        else:
            return "Number" + " " + str(self.c) + " " + str(self.x) + " " + str(self.y)

class Example_sword:
    def __init__(self, x, y, size=60, name="sword"):
        self.name = name
        self.image = pygame.transform.scale(load_image("sword.png"), (size//3, size))
        self.x = x
        self.y = y
        self.sizex = size//3
        self.sizey = size
        self.do = ["", 0]
        self.movable = True
        self.damageble = False
        self.usable = True
        self.Ranged = False
        self.damage = 40
        self.rollback = 50
        self.dist = 250

    def display(self, x, y, screen, colis, fps):
        screen.blit(self.image, (self.x - x, self.y - y))

    def display_weapon(self, xcam, ycam, x, y, screen, angle, revers):
        if revers:
            screen.blit(pygame.transform.flip(pygame.transform.rotate(self.image, angle), True, False), (x - xcam, y - ycam))
        else:
            screen.blit(pygame.transform.rotate(self.image, angle), (x - xcam, y - ycam))

    def display_into_inventar(self, screen, x, y, sizex, sizey):
        screen.blit(pygame.transform.scale(self.image, (sizex - 10, sizey - 10)), (x, y))

    def moveing(self, x, y, camx, camy):
        self.x = camx + x - self.sizex // 2
        self.y = camy + y - self.sizey // 2
        self.status_set("move", True)

    def status_set(self, do, status=True):
        # задать статус для анимаций
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def data_return(self):
        return "Sword" + " " + str(self.x) + " " + str(self.y)
class Projectile:
    def __init__(self, x, y, speed):
        self.image = pygame.transform.scale(load_image("Projectile.png"), (30, 30))
        self.name = "Projectile"
        self.x = x
        self.y = y
        self.speed = speed
        self.vx = speed
        self.vy = 0
        self.sizex = 30
        self.sizey = 30
        self.movable = False
        self.damageble = False
        self.usable = False
        self.do = ["", 0]
        self.drop = ["number", 10]

    def display(self, x, y, screen, collisions, fps):
        screen.blit(self.image, (self.x - x, self.y - y))
        for i in collisions:
            col = i.collision_chek(self.x, self.y, self.sizex, self.sizey)
            if "x+" in col and self.vx >= 0:
                self.status_set("dead", True)
            elif "x-" in col and self.vx <= 0:
                self.status_set("dead", True)
            if "y+" in col and self.vy >= 0:
                self.status_set("dead", True)
            elif "y-" in col and self.vy <= 0:
                self.status_set("dead", True)
        self.move()


    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.vy = self.vy + 0.5

    def set_direction(self, cos, sin):
        speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        self.vx = speed * cos
        self.vy = speed * sin

    def status_set(self, do, status=True):
        # задать статус для анимаций
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0
    def data_return(self):
        return "progectile f"


# Создание класса дальнобойного оружия
class RangedWeapon:
    def __init__(self, x, y, size=60, name="ranged_weapon"):
        self.name = name
        self.image = pygame.transform.scale(load_image("bow.png"), (size, size))
        self.x = x
        self.y = y
        self.sizex = size
        self.sizey = size
        self.do = ["", 0]
        self.movable = True
        self.damageble = False
        self.usable = True
        self.Ranged = True
        self.damage = 40
        self.rollback = 50

    def display(self, x, y, screen, colis, fps):
        screen.blit(self.image, (self.x - x, self.y - y))

    def display_weapon(self, xcam, ycam, x, y, screen, angle, revers):
        if revers:
            screen.blit(pygame.transform.flip(pygame.transform.rotate(self.image, angle), True, False),
                        (x - xcam, y - ycam))
        else:
            screen.blit(pygame.transform.rotate(self.image, angle), (x - xcam, y - ycam))

    def display_into_inventar(self, screen, x, y, sizex, sizey):
        screen.blit(pygame.transform.scale(self.image, (sizex - 10, sizey - 10)), (x, y))

    def moveing(self, x, y, camx, camy):
        self.x = camx + x - self.sizex // 2
        self.y = camy + y - self.sizey // 2
        self.status_set("move", True)

    def status_set(self, do, status=True):
        # Задать статус для анимаций
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def returnProjectile(self):
        return Projectile(0, 0, self.damage)

    def data_return(self):
        return "ranged_weapon" + " " + str(self.x) + " " + str(self.y)

    def Projectileret(self, x, y):
        return Projectile(x, y, self.damage)

class Expression:
    def __init__(self, x, y, size=50, name="="):
        self.name = name
        self.left = []
        self.right = []
        self.x = x
        self.y = y
        self.sizex = size//2 * (len(self.right) + len(self.left)) + 50
        self.sizey = size
        self.do = ["", 0]
        self.movable = True
        self.damageble = False
        self.usable = False

    def display(self, x, y, screen, colis, fps):
        font = pygame.font.Font(None, self.sizey)
        text = font.render(" ".join([i.name for i in self.left]) + " = " + " ".join([i.name for i in self.right]), True, (255, 255, 255))
        screen.blit(text, (self.x - x, self.y - y))

    def display_into_inventar(self, screen, x, y, sizex, sizey):
        font = pygame.font.Font(None, sizex - 2)
        text = font.render("=", True, (255, 255, 255))
        screen.blit(text, (x, y))

    def moveing(self, x, y, camx, camy):
        self.x = camx + x - self.sizex // 2
        self.y = camy + y - self.sizey // 2
        self.status_set("move", True)

    def status_set(self, do, status=True):
        # задать статус для анимаций
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def add(self, obj, x, y):
        if x < self.x + 25 + len(self.left)*(self.sizey//2):
            i = (x - self.x) // (self.sizey//2)
            self.left.insert(int(i), obj)
        else:
            i = (x - (self.x + 25 + len(self.left)*(self.sizey//2))) // (self.sizey//2)
            self.right.insert(int(i), obj)
        self.sizex = (self.sizey // 2) * (len(self.right) + len(self.left)) + 50
    def take(self, x, y, world):
        x = x + world.camx
        y = y + world.camy
        result = False
        if x < self.x + len(self.left)*(self.sizey//2):
            i = (x - self.x) // (self.sizey//2)
            result = self.left[int(i)]
            del self.left[int(i)]
        elif x > self.x + len(self.left)*(self.sizey//2) + 30:
            i = (x - (self.x + 50 + len(self.left)*(self.sizey//2))) // (self.sizey//2)
            result = self.right[int(i)]
            del self.right[int(i)]
        else:
            self.right = [Number(int(eval("".join([i.name for i in self.left]))), self.x, self.y)]
        self.sizex = (self.sizey // 2) * (len(self.right) + len(self.left)) + 50
        return result

    def data_return(self):
        return "Expression" + " " + str(self.x) + " " + str(self.y)