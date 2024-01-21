import os
import sys
import pygame

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

def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image