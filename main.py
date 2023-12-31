import pygame
import os
import sys
from utilits import World, Person, load_image, Anim, Collision_reactangle, Button, Text
from objects import Number, Example_sword
from mobs import Enemy
import random

pygame.init()


def startscreen(screen, clock, massag=""):
    # функция меню, возвращает список данных о начале игры [начать(True, False), загрузить или новая игра(True, False), номер слота для сохранения]
    QUIT = Button(100, 300, "QUIT")
    nuw = Button(100, 100, "new game")
    load = Button(100, 200, "load game")
    slot1 = Button(100, 100, "1")
    slot2 = Button(200, 100, "2")
    slot3 = Button(300, 100, "3")
    back = Button(100, 200, "back")
    massage = Text(400, 100, massag)
    if massage == "":
        massage.set_visible(False)
    meny = 0
    while True:
        screen.fill((0, 0, 0))
        massage.display(screen)
        if meny == 0:
            nuw.display(screen)
            load.display(screen)
            QUIT.display(screen)
        elif meny == 1 or meny == 2:
            slot1.display(screen)
            slot2.display(screen)
            slot3.display(screen)
            back.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return [False]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if nuw.check(x, y) and meny == 0:
                    meny = 1
                if load.check(x, y) and meny == 0:
                    meny = 2
                if slot1.check(x, y):
                    if meny == 1:
                        return [True, True, 1]
                    elif meny == 2:
                        return [True, False, 1]
                if slot2.check(x, y):
                    if meny == 1:
                        return [True, True, 2]
                    elif meny == 2:
                        return [True, False, 2]
                if slot3.check(x, y):
                    if meny == 1:
                        return [True, True, 3]
                    elif meny == 2:
                        return [True, False, 3]
                if QUIT.check(x, y) and meny == 0:
                    return [False]
                if back.check(x, y) and (meny == 1 or meny == 2):
                    meny = 0
        pygame.display.flip()
        clock.tick(100)


def pausmenu(screen, clock):
    # функция паузы
    cont = Button(400, 200, "continue")
    out = Button(400, 300, "go to menu")
    while True:
        cont.display(screen)
        out.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if cont.check(x, y):
                    return True
                elif out.check(x, y):
                    return False
        pygame.display.flip()
        clock.tick(100)


def save_all(world, slot):
    # сохранить текущую игру в слот
    f = open('savefiles\save' + slot + '.txt', 'w')
    for i in world.col:
        f.write(i.data_return() + "\n")
    f.close()


def open_all(world, slot):
    # загрузить игру из слота
    try:
        f = open('savefiles\save' + slot + '.txt', 'r')
        for line in f:
            obj = line.split()
            if obj[0] == "Person":
                world.create_object(Person(int(obj[1]), int(obj[2])))
                world.col[-1].x = float(obj[3])
                world.col[-1].y = float(obj[4])
                world.col[-1].hp = int(obj[5])
            elif obj[0] == "Number":
                world.create_object(Number(int(obj[1]), float(obj[2]), float(obj[3])))
            elif obj[0] == "Enemy":
                person = world.return_obj(name="person")
                world.create_object(Enemy(float(obj[1]), float(obj[2]), person))
                world.col[-1].hp = int(obj[3])
            elif obj[0] == "Sword":
                world.create_object(Example_sword(float(obj[1]), float(obj[2])))
        f.close()
        return True
    except:
        return False


def deadscreen(screen, clock):
    text = Text(400, 200, "you are dead!")
    out = Button(400, 300, "go to menu")
    while True:
        text.display(screen)
        out.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if out.check(x, y):
                    return True
        pygame.display.flip()
        clock.tick(100)


if __name__ == '__main__':
    # инициализация Pygame:
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    massage = ""
    while True:
        startparam = startscreen(screen, clock, massage)
        if startparam[0]:
            world = World(0, 0, screen)
            world.col = []
            world.collisions = []
            if startparam[1]:
                person = Person(3, 10)
                world.create_object(person)
                world.create_object(Number(10, 10, -30))
                world.create_object(Number(10, 10, -20))
                world.create_object(Enemy(900, -300, person))
                world.create_object(Example_sword(200, -300))
                slot = startparam[2]
            else:
                slot = startparam[2]
                r = open_all(world, str(slot))
                if not r:
                    massage = "Error: save not found"
                    continue
            massage = ""
            world.create_collision(Collision_reactangle(-1000, 10, 2000, 1000))
            world.create_collision(Collision_reactangle(-500, -100, 200, 100))
            world.create_collision(Collision_reactangle(100, -200, 300, 50))
            person = world.return_obj("person")  # ссылается на персонажа
            flag = False  # храниет в себе нажата ли кнопка мыши
            returnd = False  # хранит в себе обьект на который было проиведено нажатие
            while running:
                # цикл игры, если прервать break то переходит в меню, если прервать с помощью running = False выходит из программы
                x, y = pygame.mouse.get_pos()
                if not flag and returnd:  # если до этого был обьект который мы двигали а сейчас отпустили убирает у него статус двигается
                    returnd.status_set("move", False)
                returnd = world.click(x, y)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN and person.do[0] != "dead":
                        flag = True
                        if x < person.sizeinventarx and y < person.sizeinventary:
                            returnd = person.get_it(x, y)
                            if returnd:
                                world.create_object(returnd)
                        elif returnd:
                            if returnd.damageble:
                                person.attack(returnd)
                    if event.type == pygame.MOUSEBUTTONUP:
                        flag = False
                        if returnd and x < person.sizeinventarx and y < person.sizeinventary:
                            if person.put(x, y, returnd):
                                world.del_object(world.col.index(returnd))
                    if event.type == pygame.KEYDOWN and person.do[0] != "dead":
                        if event.key == 32:
                            person.jump()
                        elif 48 < event.key < 58:
                            person.choose(event.key - 49)
                if person.do[0] != "dead":
                    if flag:
                        if returnd:
                            if returnd.movable:
                                returnd.moveing(x, y, world.camx, world.camy)
                    if person.y > 10000:
                        person.status_set("dead", True)
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_a]:
                        person.move(False)
                        if person.do[0] != "jump":
                            person.status_set("moveleft")
                    elif keys[pygame.K_d]:
                        person.move(True)
                        if person.do[0] != "jump":
                            person.status_set("moveright")
                    else:
                        person.status_set("moveleft", False)
                        person.status_set("moveright", False)
                    if keys[pygame.K_ESCAPE]:
                        if not pausmenu(screen, clock):
                            save_all(world, str(slot))
                            break
                elif deadscreen(screen, clock):
                    break
                else:
                    running = False
                world.display()
                pygame.display.flip()
                clock.tick(100)
            if not running:
                break
        else:
            break
    pygame.quit()
