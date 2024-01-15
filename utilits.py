import pygame
import os
import sys
import random


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    # класс кнопки,
    def __init__(self, x, y, text, size=50):
        font = pygame.font.Font(None, size)
        self.text = font.render(text, True, (10, 100, 100))
        self.x = x
        self.y = y
        self.w = self.text.get_width()
        self.h = self.text.get_height()

    def display(self, screen):
        screen.blit(self.text, (self.x, self.y))
        pygame.draw.rect(screen, (10, 100, 100), (self.x - 10, self.y - 10,
                                                  self.w + 20, self.h + 20), 1)

    def check(self, x, y):
        if self.x < x < self.x + self.w and self.y < y < self.y + self.h:
            return True
        else:
            return False


class Text:
    def __init__(self, x, y, text, size=50):
        font = pygame.font.Font(None, size)
        self.text = font.render(text, True, (10, 100, 100))
        self.x = x
        self.y = y
        self.w = self.text.get_width()
        self.h = self.text.get_height()
        self.visible = True

    def display(self, screen):
        if self.visible:
            screen.blit(self.text, (self.x, self.y))

    def set_visible(self, visible):
        self.visible = visible


class Anim:
    # класс анимаций. экзепляр хранит в себе анимацию.
    def __init__(self, filename, frames):
        self.images = []
        for i in range(frames):
            name = os.path.join('anime', filename, (str(i) + ".png"))
            self.images.append(load_image(name))
        self.nowframe = 0

    def framedraw(self, screen, x, y):
        # отрисовывает кадр на координатах
        screen.blit(self.images[self.nowframe], (x, y))
        if self.nowframe < len(self.images) - 1:
            self.nowframe += 1
        else:
            self.nowframe = 0


class World:
    def __init__(self, camerax, cameray, screen, objects=[], florcol=(100, 100, 100), backcol=(0, 0, 0)):
        self.seed = 0
        self.florcol = florcol
        self.backcol = backcol
        self.camx = camerax
        self.camy = cameray
        self.col = objects
        self.collisions = []
        self.scr = screen
        self.camera_binding = "person"  # обьект к которому будет прикреплена камера

    def create_object(self, object):
        self.col.append(object)

    def create_collision(self, object):
        self.collisions.append(object)

    def display(self):
        # отображение обьектов и колизий
        self.scr.fill(self.backcol)
        self.camx = self.return_obj(self.camera_binding).x - 400
        self.camy = self.return_obj(self.camera_binding).y - 510
        for i in self.collisions:
            i.display(int(self.camx), int(self.camy), self.scr, self.florcol)
        for i in self.col:
            i.display(int(self.camx), int(self.camy), self.scr, self.collisions)
            if i.do[0] == "dead":
                self.del_object(self.col.index(i))

    def return_obj(self, name="", number=-1):
        # возвращает обьект с именем или с индексом
        if name != "":
            for i in self.col:
                if i.name == name:
                    return i

    def del_object(self, i):
        # удаляет обьект с номером i
        self.col.pop(i)

    def click(self, x, y):
        # возвращает обьект на координатах x, y, eсли обьекта нет то возвращает False
        for i in self.col:
            if i.x < x + self.camx < i.x + i.sizex and i.y < y + self.camy < i.y + i.sizey:
                return i
        return False


class Person:
    # класс персонажа
    def __init__(self, row, col, x=0, y=-200, size=109, name="person"):
        # загрузка анимаций
        self.image = load_image("person.png")
        self.runright = Anim("runright", 2)
        self.runleft = Anim("runleft", 2)
        self.attackAnim = Anim("person_attack", 1)
        self.name = name
        self.x = x
        self.vx = 0
        self.vy = 0
        self.y = y
        self.sizey = size
        self.sizex = 50
        self.do = ["", 0]
        self.inventar = [["" for j in range(col)] for i in range(row)]
        self.sizeinventarx = 400
        self.sizeinventary = 100
        self.hp = 400
        self.movable = False
        self.damageble = False
        self.use = False
        self.usenum = 0

    def attack(self, enemy):
        self.status_set("attack", True)
        if self.do[1] == 0:
            if self.use:
                enemy.damag(self.use.damage)
            else:
                enemy.damag(5)
            self.do[1] = 20

    def damag(self, level):
        self.hp -= level
        if self.hp <= 0:
            self.status_set("dead", True)

    def heal(self, level):
        if self.hp < 400:
            self.hp += level

    def status_set(self, do, status=True):
        # задать статус для анимаций, во время полёта статус автоматически "Jump"
        if status:
            self.do[0] = do
        elif self.do[0] == do and not status:
            self.do[0] = ""
            self.do[1] = 0

    def display(self, x, y, screen, collision):
        # отображение и просчёт движения
        if self.do[0] != "dead":
            if random.randint(0, 1):
                self.heal(random.randint(0, 1))
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
            elif self.do[0] == "attack":
                if self.do[1] > 0:
                    self.do[1] = self.do[1] - 1
                else:
                    self.status_set("attack", False)
                self.attackAnim.framedraw(screen, self.x - x, self.y - y)
            else:
                screen.blit(self.image, (self.x - x, self.y - y))
            pygame.draw.rect(screen, (0, 100, 100), (0, 0, self.sizeinventarx, self.sizeinventary))
            sizey = self.sizeinventary // len(self.inventar)
            sizex = self.sizeinventarx // len(self.inventar[0])
            for i in range(len(self.inventar)):
                for j in range(len(self.inventar[0])):
                    pygame.draw.rect(screen, (0, 0, 0), (j * sizex + 1, i * sizey + 1, sizex - 2, sizey - 2))
                    if self.inventar[i][j] == "":
                        pass
                    else:
                        self.inventar[i][j].display_into_inventar(screen, j * sizex + 1, i * sizey + 1, sizex, sizey)
            if self.usenum:
                pygame.draw.rect(screen, (100, 100, 100), ((self.usenum - 1) * sizex, 0, sizex, sizey), 3)
            pygame.draw.rect(screen, (255, 255, 255), (750, 20, self.hp // 2, 10))
            pygame.draw.rect(screen, (0, 100, 100), (747, 17, 206, 16), 1)

    def move(self, side):
        if side:
            self.vx = 5
        else:
            self.vx = -5

    def jump(self):
        if self.do[0] != "jump":
            self.vy = self.vy - 17

    def put(self, xmous, ymous, object):
        # положить обьект в инвентарь.
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
        # достать обьект из инвентаря.
        sizey = self.sizeinventary // len(self.inventar)
        sizex = self.sizeinventarx // len(self.inventar[0])
        row = ymous // sizey
        col = xmous // sizex
        if self.inventar[row][col] != "":
            returnd = self.inventar[row][col]
            returnd.x = self.x - 400 + col * sizex
            returnd.y = self.y - 510 + row * sizey
            self.inventar[row][col] = ""
            return returnd
        else:
            return False

    def data_return(self):
        # вернуть данные для сохранения
        return "Person" + " " + str(len(self.inventar)) + " " + str(len(self.inventar[0])) + " " + str(self.x) + " " + \
            str(self.y) + " " + str(self.hp)

    def respawn(self):
        self.status_set("dead", False)
        self.x = 0
        self.vx = 0
        self.vy = 0
        self.y = -200
        for i in range(len(self.inventar)):
            for j in range(len(self.inventar[i])):
                self.inventar[i][j] = ""
        self.hp = 50

    def choose(self, num):
        if num + 1 != self.usenum:
            choos = self.inventar[0][num]
            if choos:
                if choos.usable:
                    self.use = choos
                    self.usenum = num + 1
        else:
            self.usenum = 0
            self.use = False


class Collision_reactangle:
    def __init__(self, x, y, sizex, sizey):
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey

    def collision_chek(self, x, y, sizex, sizey):
        # проверка на столкновение с колизией
        # возвращает тип столкновение y+ - столкновение по y с верху
        # y- столкновение по y с низу
        # x+ столкновение по x слева
        # x- столкновение по x cправа
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
        r, g, b = color
        r = int(r - self.y * 0.01) % 255
        g = int(g - self.y * 0.01) % 255
        b = int(b - self.y * 0.01) % 255
        # отображение
        pygame.draw.rect(screen, (r, g, b), (self.x - x, self.y - y, self.sizex, self.sizey))
