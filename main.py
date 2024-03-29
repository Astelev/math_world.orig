import pygame
import os
import sys
from utilits import World, Person, Collision_reactangle, Button, Text
from mobs import Enemy, Enemystr
from objects import Example_sword, Number, RangedWeapon, Projectile, Expression
from imagefunk import load_image, Anim
import random

pygame.init()

def spawn_enemystr(person, world, clock):
    if random.randint(0, 100) == 0:
        mobs = 0
        for i in world.col:
            if i.damageble:
                mobs += 1
        if mobs < 5:
            dx = random.randint(600, 2000) * (random.random() * 2 - 1)
            dy = random.randint(500, 1000) * (random.random() * 2 - 1)
            if person.y > - 400:
                mob = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10][random.randint(0, 9)]
            elif person.y <= - 400:
                mob = ["+", "/"][random.randint(0, 1)]
            temp = False
            for i in world.collisions:
                if abs(i.x - (person.x + dx)) < i.sizex * 2 and abs(i.y - (person.y + dy)) < i.sizey * 2:
                    if "y+" in i.collision_chek(person.x + dx, person.y + dy, 100, 100):
                        temp = True
                        break
            if temp:
                world.create_object(Enemystr(person.x + dx, person.y + dy, person, mob))
            
def craftscreen(screen, clock, inventar):
    craftbtn1 = Button(350, 150, "Sword")
    craftbtn2 = Button(350, 210, "Bow")
    craftbtn3 = Button(350, 270, "=")
    craftbtn4 = Button(350, 330, "-")
    craftbtn5 = Button(350, 390, "×")
    text = Text(350, 100, "craft meny")
    craft1image = pygame.transform.scale(load_image("craft1.png"), (100, 50))
    craft2image = pygame.transform.scale(load_image("craft2.png"), (100, 50))
    craft3image = pygame.transform.scale(load_image("craft3.png"), (100, 50))
    craft4image = pygame.transform.scale(load_image("craft4.png"), (100, 50))
    craft5image = pygame.transform.scale(load_image("craft5.png"), (100, 50))
    quitbtn = Button(400, 500, "quit")
    # списки предметов для крафта состоит из списков из двух элементов 1- name требуемого обьекта, 2- количество
    craft1 = [["1", 1], ["+", 1]]
    craft2 = [["2", 2], ["+", 1]]
    craft3 = [["/", 2]]
    craft4 = [["/", 1]]
    craft5 = [["+", 1]]
    while True:
        pygame.draw.rect(screen, (50, 50, 50), (300, 100, 300, 500))
        text.display(screen)
        screen.blit(craft1image, (470, 150))
        screen.blit(craft2image, (470, 210))
        screen.blit(craft3image, (470, 270))
        screen.blit(craft4image, (470, 330))
        screen.blit(craft5image, (470, 390))
        craftbtn1.display(screen)
        craftbtn2.display(screen)
        craftbtn3.display(screen)
        craftbtn4.display(screen)
        craftbtn5.display(screen)
        quitbtn.display(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if quitbtn.check(x,y):
                    return True
                elif craftbtn1.check(x, y):
                    isresurs = True
                    delcell = []
                    for i in craft1:
                        c = 0
                        temporary = False
                        for j in inventar:
                            for k in j:
                                if k:
                                    if k.name == i[0]:
                                        delcell.append([inventar.index(j), j.index(k)])
                                        c = c + 1
                                        if c >= i[1]:
                                            temporary = True
                                            break
                            if temporary:
                                break
                        if not temporary:
                            isresurs = False
                            # нет ресов
                            break
                    if isresurs:
                        inventar[-1][-1] = Example_sword(0, 0)
                        for i in delcell:
                            inventar[i[0]][i[1]] = ""
                        return True
                elif craftbtn2.check(x, y):
                    isresurs = True
                    delcell = []
                    for i in craft2:
                        c = 0
                        temporary = False
                        for j in inventar:
                            for k in j:
                                if k:
                                    if k.name == i[0]:
                                        delcell.append([inventar.index(j), j.index(k)])
                                        c = c + 1
                                        if c >= i[1]:
                                            temporary = True
                                            break
                            if temporary:
                                break
                        if not temporary:
                            isresurs = False
                            # нет ресов
                            break
                    if isresurs:
                        inventar[-1][-1] = RangedWeapon(0, 0)
                        for i in delcell:
                            inventar[i[0]][i[1]] = ""
                        return True
                elif craftbtn3.check(x, y):
                    isresurs = True
                    delcell = []
                    for i in craft3:
                        c = 0
                        temporary = False
                        for j in inventar:
                            for k in j:
                                if k:
                                    if k.name == i[0]:
                                        delcell.append([inventar.index(j), j.index(k)])
                                        c = c + 1
                                        if c >= i[1]:
                                            temporary = True
                                            break
                            if temporary:
                                break
                        if not temporary:
                            isresurs = False
                            # нет ресов
                            break
                    if isresurs:
                        inventar[-1][-1] = Expression(0, 0)
                        for i in delcell:
                            inventar[i[0]][i[1]] = ""
                        return True
                elif craftbtn4.check(x, y):
                    isresurs = True
                    delcell = []
                    for i in craft4:
                        c = 0
                        temporary = False
                        for j in inventar:
                            for k in j:
                                if k:
                                    if k.name == i[0]:
                                        delcell.append([inventar.index(j), j.index(k)])
                                        c = c + 1
                                        if c >= i[1]:
                                            temporary = True
                                            break
                            if temporary:
                                break
                        if not temporary:
                            isresurs = False
                            # нет ресов
                            break
                    if isresurs:
                        inventar[-1][-1] = Number("-", 0, 0)
                        for i in delcell:
                            inventar[i[0]][i[1]] = ""
                        return True
                elif craftbtn5.check(x, y):
                    isresurs = True
                    delcell = []
                    for i in craft5:
                        c = 0
                        temporary = False
                        for j in inventar:
                            for k in j:
                                if k:
                                    if k.name == i[0]:
                                        delcell.append([inventar.index(j), j.index(k)])
                                        c = c + 1
                                        if c >= i[1]:
                                            temporary = True
                                            break
                            if temporary:
                                break
                        if not temporary:
                            isresurs = False
                            # нет ресов
                            break
                    if isresurs:
                        inventar[-1][-1] = Number("×", 0, 0)
                        for i in delcell:
                            inventar[i[0]][i[1]] = ""
                        return True
        pygame.display.flip()



def startscreen(screen, clock, massag=""):
    # функция меню, возвращает список данных о начале игры [начать(True, False), загрузить или новая игра(True, False), номер слота для сохранения]
    QUIT = Button(100, 300, "QUIT")
    nuw = Button(100, 100, "new game")
    load = Button(100, 200, "load game")
    slot1 = Button(100, 100, "1")
    slot2 = Button(200, 100, "2")
    slot3 = Button(300, 100, "3")
    text = Text(400, 50, "Math.s game")
    back = Button(100, 200, "back")
    massage = Text(400, 150, massag)
    if massage == "":
        massage.set_visible(False)
    meny = 0
    while True:
        screen.fill((0, 0, 0))
        massage.display(screen)
        text.display(screen)
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
                    text.text_set("select save slot")
                    meny = 1
                if load.check(x, y) and meny == 0:
                    text.text_set("select save slot")
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
                    text.text_set("Math.s game")
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
    f.write("seed " + str(world.seed) + "\n")
    for i in world.col:
        if i.name == "person":
            f.write(i.data_return() + "\n")
            f.write("inv " + str(len(i.inventar)) + " " + str(len(i.inventar[0])) + "\n")
            for k in i.inventar:
                for g in k:
                    if g:
                        f.write(g.data_return() + ";")
                    else:
                        f.write("None" + ";")
                f.write(" :nextstr: ")
            f.write(" " + "\n")
        else:
            f.write(i.data_return() + "\n")
    f.close()


def open_all(world, slot):
    # загрузить игру из слота
    try:
        f = open('savefiles\save' + slot + '.txt', 'r')
        mode = True
        for line in f:
            if mode:
                obj = line.split()
                if obj[0] == "seed":
                    world.seed = obj[1]
                elif obj[0] == "Person":
                    world.create_object(Person(int(obj[1]), int(obj[2])))
                    world.col[-1].x = float(obj[3])
                    world.col[-1].y = float(obj[4])
                    world.col[-1].hp = int(obj[5])
                elif obj[0] == "Number":
                    if obj[1] == "*":
                        world.create_object(Number("×", float(obj[2]), float(obj[3])))
                    else:
                        world.create_object(Number(str(obj[1]), float(obj[2]), float(obj[3])))
                elif obj[0] == "Enemy":
                    person = world.return_obj(name="person")
                    world.create_object(Enemy(float(obj[1]), float(obj[2]), person))
                    world.col[-1].hp = int(obj[3])
                elif obj[0] == "Sword":
                    world.create_object(Example_sword(float(obj[1]), float(obj[2])))
                elif obj[0] == "ranged_weapon":
                    world.create_object(RangedWeapon(float(obj[1]), float(obj[2])))
                elif obj[0] == "Enemystr":
                    person = world.return_obj(name="person")
                    if obj[4] == "*":
                        world.create_object(Enemystr(float(obj[1]), float(obj[2]), person, "×"))
                    else:
                        world.create_object(Enemystr(float(obj[1]), float(obj[2]), person, obj[4]))
                    world.col[-1].hp = int(obj[3])
                elif obj[0] == "Expression":
                    world.create_object(Expression(float(obj[1]), float(obj[2])))
                elif obj[0] == "inv":
                    mode = False
                    row = obj[1]
                    col = obj[2]
            else:
                inv = line.split(" :nextstr: ")
                for j in range(len(inv)):
                    string = inv[j].split(";")
                    for i in range(len(string)):
                        if string[i] != "None" and string[i] != "" and string[i] != " \n":
                            slot = string[i].split()
                            if slot[0] == "Number":
                                world.col[-1].inventar[j][i] = Number((slot[1]), float(slot[2]), float(slot[3]))
                            elif slot[0] == "Sword":
                                world.col[-1].inventar[j][i] = Example_sword(float(slot[1]), float(slot[2]))
                            elif slot[0] == "ranged_weapon":
                                world.col[-1].inventar[j][i] = RangedWeapon(float(obj[1]), float(obj[2]))
                            elif slot[0] == "Expression":
                                world.col[-1].inventar[j][i] = Expression(float(obj[1]), float(obj[2]))
                mode = True
        f.close()
        return True
    except:
        return False

def random_generation(world):
    cellx = 700
    celly = 300
    for i in range(20):
        for j in range(500):
            random.seed(i * j * world.seed)
            x = random.randint(0, cellx)
            random.seed(i * j * world.seed)
            y = random.randint(0, celly - 150)
            world.create_collision(
                Collision_reactangle(-15 * cellx + j * cellx + x, -200 - i * celly - y, 500, 50))

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
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    size = screen.get_size()
    clock = pygame.time.Clock()
    running = True
    massage = ""
    while True:
        startparam = startscreen(screen, clock, massage)
        if startparam[0]:
            world = World(0, 0, screen, size)
            world.col = []
            world.collisions = []
            world.create_collision(Collision_reactangle(-100000, 10, 200000, 1000))
            world.create_collision(Collision_reactangle(-500, -100, 200, 100))
            world.create_collision(Collision_reactangle(100, -200, 300, 50))
            if startparam[1]:
                person = Person(3, 10)
                world.create_object(person)
                world.create_object(Enemystr(900, -100, person, 1))
                world.create_object(Enemystr(900, -500, person, "+"))
                slot = startparam[2]
                world.seed = random.randint(-100000, 100000)
            else:
                slot = startparam[2]
                r = open_all(world, str(slot))
                if not r:
                    massage = "Error: save not found"
                    continue
            massage = ""
            random_generation(world)
            person = world.return_obj("person")  # ссылается на персонажа
            btncraft = Button(450, 10, "craft") # кнопка крафта
            fps = 100
            flag = False  # храниет в себе нажата ли кнопка мыши
            returnd = False  # хранит в себе обьект на который наведена мышь
            while running:
                # цикл игры, если прервать break то переходит в меню, если прервать с помощью running = False выходит из программы
                x, y = pygame.mouse.get_pos()
                person.xmous = x
                person.ymous = y
                if not flag and returnd:  # если до этого был обьект который мы двигали а сейчас отпустили убирает у него статус двигается
                    returnd.status_set("move", False)
                if not flag:
                    returnd = world.click(x, y)
                keys = pygame.key.get_pressed()
                spawn_enemystr(person, world, clock)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        flag = True
                        if x < person.sizeinventarx and y < person.sizeinventary:
                            returnd = person.get_it(x, y)
                            if returnd:
                                world.create_object(returnd)
                        elif btncraft.check(x, y):
                            if not craftscreen(screen, clock, person.inventar):
                                running = False
                        elif keys[pygame.K_LSHIFT] and returnd:
                            if returnd.name == "=":
                                returnd = returnd.take(x, y, world)
                                if returnd:
                                    world.create_object(returnd)
                        else:
                            person.attack(returnd, x, y, world)
                    if event.type == pygame.MOUSEBUTTONUP:
                        flag = False
                        if returnd:
                            if x < person.sizeinventarx and y < person.sizeinventary:
                                if person.put(x, y, returnd):
                                    world.del_object(world.col.index(returnd))
                            else:
                                click = world.click(x, y, True)
                                names = [i.name for i in click]
                                if "=" in names and returnd.name != "=":
                                    click[names.index("=")].add(returnd, returnd.x + returnd.sizex // 2, returnd.y + returnd.sizey // 2)
                                    world.del_object(world.col.index(returnd))
                    if event.type == pygame.KEYDOWN and person.do[0] != "dead":
                        if event.key == 32:
                            person.jump()
                        elif 48 < event.key < 58:
                            person.choose(event.key - 49)
                if person.do[0] != "dead":
                    if flag:
                        if returnd and not keys[pygame.K_LSHIFT]:
                            if returnd.movable:
                                returnd.moveing(x, y, world.camx, world.camy)
                    if person.y > 10000:
                        person.status_set("dead", True)
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
                world.display(fps)
                btncraft.display(screen)
                pygame.display.flip()
                clock.tick(100)
                fps = clock.get_fps()
            if not running:
                break
        else:
            break
    pygame.quit()
