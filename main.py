import pygame
import os
import sys
from utilits import World, Number, Person, load_image, Anim

if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    running = True
    world = World(0, 0, screen)
    world.create_object(Person(name="person"))
    world.create_object(Number(10, 10, -30))
    person = world.return_obj("person")
    flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
            if event.type == pygame.MOUSEBUTTONUP:
                flag = False
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    person.status_set("jump")
        if flag:
            x, y = pygame.mouse.get_pos()
            returnd = world.click(x, y)
            if returnd:
                returnd.move(x, y, world.camx, world.camy)
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
# testim
