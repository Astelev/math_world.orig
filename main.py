import pygame
import os
import sys
from utilits import World, Person, load_image, Anim, Collision_reactangle, Physical_object
from objects import Number

def startscreen(screen, clock):
    while True:
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (20, 100, 200), (100, 100, 100, 50), 5)
        pygame.draw.rect(screen, (20, 100, 200), (100, 200, 100, 50), 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 < x < 200 and  100 < y < 150:
                    return True
                elif 100 < x < 200 and  200 < y < 250:
                    return False
        pygame.display.flip()
        clock.tick(100)

def pausmenu(screen, clock):
    while True:
        pygame.draw.rect(screen, (20, 100, 200), (400, 200, 100, 50), 5)
        pygame.draw.rect(screen, (20, 100, 200), (400, 300, 100, 50), 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 400 < x < 500 and  200 < y < 250:
                    return True
                elif 400 < x < 500 and  300 < y < 350:
                    return False
        pygame.display.flip()
        clock.tick(100)

def save_all(world, slot):
    f = open('savefiles\save' + slot +'.txt', 'w')
    for i in world.col:
        f.write(i.data_return() + "\n")
    f.close()

def open_all(world, slot):
    f = open('savefiles\save' + slot +'.txt', 'r')
    for line in f:
        obj = line.split()
        if obj[0] == "Person":
            world.create_object(Person(int(obj[1]), int(obj[2])))
            world.col[-1].x = float(obj[3])
            world.col[-1].y = float(obj[4])
        elif obj[0] == "Number":
            world.create_object(Number(int(obj[1]), float(obj[2]), float(obj[3])))
    f.close()




if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    if startscreen(screen, clock):
        running = True
        world = World(0, 0, screen)
        open_all(world, "1")
        """world.create_object(Person(3, 10))
        world.create_object(Number(10, 10, -30))
        world.create_object(Number(10, 10, -20))"""
        world.create_collision(Collision_reactangle(-1000, 10, 2000, 1000))
        world.create_collision(Collision_reactangle(-500, -100, 200, 100))
        world.create_collision(Collision_reactangle(100, -200, 300, 50))
        person = world.return_obj("person") # ссылается на персонажа
        flag = False # храниет в себе нажата ли кнопка мыши
        returnd = False # хранит в себе обьект на который было проиведено нажатие
        while running:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag = True
                    if x < person.sizeinventarx and y < person.sizeinventary:
                        returnd = person.get_it(x, y)
                        if returnd:
                            world.create_object(returnd)

                if event.type == pygame.MOUSEBUTTONUP:
                    flag = False
                    if returnd and x < person.sizeinventarx and y < person.sizeinventary:
                        if person.put(x, y, returnd):
                            world.del_object(world.col.index(returnd))
                if event.type == pygame.KEYDOWN:
                    if event.key == 32:
                        person.jump()
            if not flag and returnd:
                returnd.status_set("move", False)
                returnd = False
            elif flag:
                returnd = world.click(x, y)
                if returnd:
                    if returnd.movable:
                        returnd.moveing(x, y, world.camx, world.camy)
                        returnd.status_set("move", True)
            world.display()
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
                    save_all(world, "1")
                    if not startscreen(screen, clock):
                        running = False
            pygame.display.flip()
            clock.tick(100)
        pygame.quit()
