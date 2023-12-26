import pygame
import os
import sys


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Anim:
    def __init__(self, filename, frames):
        self.images = []
        for i in range(frames):
            name = os.path.join('anime', filename, (str(i) + ".png"))
            self.images.append(load_image(name))
        self.nowframe = 0

    def framedraw(self, screen, x, y):
        screen.blit(self.images[self.nowframe], (x, y))
        if self.nowframe < len(self.images) - 1:
            self.nowframe += 1
        else:
            self.nowframe = 0


class World:
    def __init__(self, camerax, cameray, screen, objects=[], florcol=(100, 100, 100), backcol=(0, 0, 0)):
        self.florcol = florcol
        self.backcol = backcol
        self.camx = camerax
        self.camy = cameray
        self.col = objects
        self.scr = screen
        self.camera_binding = "person"

    def create_object(self, object):
        self.col.append(object)

    def display(self):
        self.scr.fill(self.backcol)
        self.camx = self.return_obj(self.camera_binding).x - 400
        self.camy = self.return_obj(self.camera_binding).y - 510
        for i in self.col:
            i.display(int(self.camx), int(self.camy), self.scr)
        pygame.draw.rect(self.scr, self.florcol, (0, 10 - self.camy, 1000, 1000))

    def return_obj(self, name="", number=-1):
        if name != "":
            for i in self.col:
                if i.name == name:
                    return i
                elif i > -1:
                    return self.col[number]
                else:
                    return self.col

    def click(self, x, y):
        for i in self.col:
            if i.x < x + self.camx < i.x + i.size and i.y < y + self.camy < i.y + i.size:
                return i
        return False


class Number:
    def __init__(self, count, x, y, size=50, name=""):
        self.c = count
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.do = ["", 0]

    def display(self, x, y, screen):
        font = pygame.font.Font(None, self.size)
        text = font.render(str(self.c), True, (255, 255, 255))
        screen.blit(text, (self.x - x, self.y - y))

    def move(self, x, y, camx, camy):
        self.x = camx + x - self.size // 2
        self.y = camy + y - self.size // 2
        self.do[0] = "move"


class Person:
    def __init__(self, size=200, name=""):
        self.image = load_image("person.png")
        self.runright = Anim("runright", 2)
        self.runleft = Anim("runleft", 2)
        self.name = name
        self.x = 0
        self.y = 0
        self.size = size
        self.do = ["", 0]

    def status_set(self, do, status=True):
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def display(self, x, y, screen):
        if self.do[0] == "jump":
            self.jump()
            screen.blit(self.image, (self.x - x, self.y - y - self.size))
        elif self.do[0] == "moveright":
            self.runright.framedraw(screen, self.x - x, self.y - y - self.size)
        elif self.do[0] == "moveleft":
            self.runleft.framedraw(screen, self.x - x, self.y - y - self.size)
        else:
            screen.blit(self.image, (self.x - x, self.y - y - self.size))

    def move(self, side):
        if side:
            self.x = self.x + 5
        else:
            self.x = self.x - 5

    def jump(self):
        if self.do[1] <= 120:
            self.y = self.y + (self.do[1] - 60) / 10
            self.do[1] = self.do[1] + 1
        elif self.do[1] > 120:
            self.do[0] = ""
            self.do[1] = 0


