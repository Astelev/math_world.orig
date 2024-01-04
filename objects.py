import pygame
from utilits import load_image, Anim


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

    def display(self, x, y, screen, colis):
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
        return "Number" + " " + str(self.c) + " " + str(self.x) + " " + str(self.y)


class Example_sword:
    def __init__(self, x, y, size=40, name="sword"):
        self.name = name
        self.image = pygame.transform.scale(load_image("sword.png"), (size, size))
        self.x = x
        self.y = y
        self.sizex = size
        self.sizey = size
        self.do = ["", 0]
        self.movable = True
        self.damageble = False
        self.usable = True
        self.damage = 40

    def display(self, x, y, screen, colis):
        screen.blit(self.image, (self.x - x, self.y - y))

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
