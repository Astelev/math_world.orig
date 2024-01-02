import pygame
import utilits


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