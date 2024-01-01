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
        self.collisions = []
        self.scr = screen
        # обьект к которому будет прикреплена камера
        self.camera_binding = "person"

    def create_object(self, object):
        self.col.append(object)

    def create_collision(self, object):
        self.collisions.append(object)

    def display(self):
        #отображение обьектов и колизий
        self.scr.fill(self.backcol)
        self.camx = self.return_obj(self.camera_binding).x - 400
        self.camy = self.return_obj(self.camera_binding).y - 510
        for i in self.col:
            i.display(int(self.camx), int(self.camy), self.scr, self.collisions)
        for i in self.collisions:
            i.display(int(self.camx), int(self.camy), self.scr, self.florcol)

    def return_obj(self, name="", number=-1):
        #возвращает обьект с именем или с индексом
        if name != "":
            for i in self.col:
                if i.name == name:
                    return i

    def del_object(self, i):
        self.col.pop(i)

    def click(self, x, y):
        #возвращает обьект на координатах x, y, eсли обьекта нет то возвращает False
        for i in self.col:
            if i.x < x + self.camx < i.x + i.sizex and i.y < y + self.camy < i.y + i.sizey:
                return i
        return False


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

    def status_set(self, do, status=True):
        # задать статус для анимаций
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0



class Person:
    def __init__(self, row, col, size=109, name=""):
        # загрузка анимаций
        self.image = load_image("person.png")
        self.runright = Anim("runright", 2)
        self.runleft = Anim("runleft", 2)
        self.name = name
        self.x = 0
        self.vx = 0
        self.vy = 0
        self.y = -200
        self.sizey = size
        self.sizex = 50
        self.do = ["", 0]
        self.inventar = [["" for j in range(col)] for i in range(row)]
        self.sizeinventarx = 400
        self.sizeinventary = 100
        self.movable = False

    def status_set(self, do, status=True):
        # задать статус для анимаций, во время полёта статус автоматически "Jump"
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def display(self, x, y, screen, collision):
        #отображение и просчёт движения
        c = True
        for i in collision:
            col = i.collision_chek(self.x, self.y, self.sizex, self.sizey)
            if "x+" in col and self.vx >= 0:
                self.vx = 0
            elif "x-" in col and self.vx <= 0:
                self.vx = 0
            if "y+" in col and self.vy >= 0:
                self.vy = 0
                c = False
                if self.do[0] != "moveright" and self.do[0] != "moveleft":
                    self.vx = 0
            elif "y-" in col and self.vy <= 0:
                self.vy = 0
        if c:
            self.status_set("jump", True)
        else:
            self.status_set("jump", False)
        self.x = self.x + self.vx
        if self.do[0] == "jump":
            self.y = self.y + self.vy
            self.vy = self.vy + 0.5
            screen.blit(self.image, (self.x - x, self.y - y))
        elif self.do[0] == "moveright":
            self.runright.framedraw(screen, self.x - x, self.y - y)
        elif self.do[0] == "moveleft":
            self.runleft.framedraw(screen, self.x - x, self.y - y)
        else:
            screen.blit(self.image, (self.x - x, self.y - y))
        pygame.draw.rect(screen, (150, 150, 150), (0, 0, self.sizeinventarx, self.sizeinventary))
        sizey = self.sizeinventary // len(self.inventar)
        sizex = self.sizeinventarx // len(self.inventar[0])
        for i in range(len(self.inventar)):
            for j in range(len(self.inventar[0])):
                pygame.draw.rect(screen, (0, 0, 0), (j * sizex + 1, i * sizey + 1, sizex - 2, sizey - 2))
                if self.inventar[i][j] == "":
                    pass
                else:
                    self.inventar[i][j].display_into_inventar(screen, j * sizex + 1, i * sizey + 1, sizex , sizey)

    def move(self, side):
        if side:
            self.vx = 5
        else:
            self.vx = -5

    def jump(self):
        if self.do[0] != "jump":
            self.vy = self.vy - 15

    def put(self, xmous, ymous, object):
        sizey = self.sizeinventary // len(self.inventar)
        sizex = self.sizeinventarx // len(self.inventar[0])
        row = ymous // sizey
        col = xmous // sizex
        if self.inventar[row][col] == "":
            self.inventar[row][col] = object
            return True
        else:
            return False

    def get_it(self, xmous, ymous):
        sizey = self.sizeinventary // len(self.inventar)
        sizex = self.sizeinventarx // len(self.inventar[0])
        row = ymous // sizey
        col = xmous // sizex
        if self.inventar[row][col] != "":
            returnd = self.inventar[row][col]
            returnd.x = self.x - 400 + self.sizeinventarx
            returnd.y = self.y - 510 + self.sizeinventary
            self.inventar[row][col] = ""
            return returnd
        else:
            return False

class Collision_reactangle:
    def __init__(self, x, y, sizex, sizey):
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey

    def collision_chek(self, x, y, sizex, sizey):
        #проверка на столкновение с колизией
        #возвращает тип столкновение y+ - столкновение по y с верху
        #y- столкновение по y с низу
        #x+ столкновение по x слева
        #x- столкновение по x cправа
        result = []
        if self.x + self.sizex > x and self.x < x + sizex and self.y + self.sizey + 20 > y and self.y - 20 < y + sizey:
            if self.y >= y:
                result.append("y+")
            elif self.y <= y:
                result.append("y-")
        if self.x + self.sizex + 10 > x and self.x - 10 < x + sizex and self.y + self.sizey > y and self.y < y + sizey:
            if self.x >= x:
                result.append("x+")
            elif self.x <= x:
                result.append("x-")
        if len(result) == 0:
            return "None"
        return result

    def display(self, x, y, screen, color):
        #отображение
        pygame.draw.rect(screen, color, (self.x - x, self.y - y, self.sizex, self.sizey))

class Physical_object:
    def __init__(self, size=109, name=""):
        # загрузка анимаций
        self.image = load_image("person.png")
        self.runright = Anim("runright", 2)
        self.runleft = Anim("runleft", 2)
        self.name = name
        self.x = 0
        self.vx = 0
        self.vy = 0
        self.y = -200
        self.sizey = size
        self.sizex = 50
        self.do = ["", 0]

    def status_set(self, do, status=True):
        # задать статус для анимаций, во время полёта статус автоматически "Jump"
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def display(self, x, y, screen, collision):
        #отображение и просчёт движения
        c = True
        for i in collision:
            col = i.collision_chek(self.x, self.y, self.sizex, self.sizey)
            if "x+" in col and self.vx >= 0:
                self.vx = 0
            elif "x-" in col and self.vx <= 0:
                self.vx = 0
            if "y+" in col and self.vy >= 0:
                self.vy = 0
                c = False
                if self.do[0] != "moveright" and self.do[0] != "moveleft":
                    self.vx = 0
            elif "y-" in col and self.vy <= 0:
                self.vy = 0
        if c:
            self.status_set("jump", True)
        else:
            self.status_set("jump", False)
        self.x = self.x + self.vx
        if self.do[0] == "jump":
            self.y = self.y + self.vy
            self.vy = self.vy + 0.5
            screen.blit(self.image, (self.x - x, self.y - y))
        elif self.do[0] == "moveright":
            self.runright.framedraw(screen, self.x - x, self.y - y)
        elif self.do[0] == "moveleft":
            self.runleft.framedraw(screen, self.x - x, self.y - y)
        else:
            screen.blit(self.image, (self.x - x, self.y - y))