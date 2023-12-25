import pygame
import os
import sys
from utilits import Word , Number, Person, load_image, Anim


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    size = 1000, 800
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    running = True
    word = Word(0, -510, screen)
    word.create_object(Person(name="person"))
    word.create_object(Number(10, 10, -30))
    person = word.return_obj("person")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    x, y = event.pos
                    returnd = word.click(x, y, True)
                    if returnd:
                        returnd.move(x, y, word.camx, word.camy)
            if event.type == pygame.KEYDOWN:
                if event.key == 32:
                    person.status_set("jump")
        word.display()
        kays = pygame.key.get_pressed()
        if kays[pygame.K_a]:
            word.camx -= 5
            if person.do[0] != "jump":
                person.status_set("move")
        elif kays[pygame.K_d]:
            word.camx += 5
            if person.do[0] != "jump":
                person.status_set("move")
        else:
            person.status_set("move", False)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
#testim