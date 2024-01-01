import pygame
import os
import sys
from utilits import World, Number, Person, load_image, Anim, Collision_reactangle, Physical_object

if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    world = World(0, 0, screen)
    world.create_object(Person(3, 4, name="person"))
    world.create_object(Number(10, 10, -30))
    world.create_object(Number(10, 10, -20))
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
                if x < 200 and y < 100:
                    returnd = person.get_it(x, y)
                    if returnd:
                        world.create_object(returnd)

            if event.type == pygame.MOUSEBUTTONUP:
                flag = False
                if returnd and x < 200 and y < 100:
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
        pygame.display.flip()
        clock.tick(100)
    pygame.quit()
