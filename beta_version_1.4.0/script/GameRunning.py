import pygame
import time
import numpy as np


class Bezier:
    def __init__(self, p0, p1, p2, p3):
        # 都是np.array
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def getBezier(self, t):
        if not 0 <= t <= 1:
            print(t)
            raise ValueError
        return ((1 - t) ** 3) * self.p0 + 3 * t * ((1 - t) ** 2) * self.p1 + self.p2 * 3 * (t ** 2) * (1 - t) + (t ** 3) * self.p3


if __name__ == "__main__":

    canvas = pygame.display.set_mode((1150, 620))
    canvas.fill((255, 255, 255))
    WIDTH = canvas.get_width()
    HEIGHT = canvas.get_height()

    b = Bezier(np.array([0, 1]), np.array([0, 9]), np.array([1, 6]), np.array([3, 1]))

    cube = pygame.Surface((50, 50))
    x = 0
    y = 300
    t = 0
    append = 0.001
    while True:
        pygame.display.update()

        canvas.fill((255, 255, 255))

        for i in range(1, 1001):
            vec = b.getBezier(i / 1000)
            pos = vec[0:2]
            pos = pos * 100
            # print((int(pos[0]), int(pos[1])))
            canvas.blit(pygame.Surface((2, 2)), (pos[0], HEIGHT - pos[1]))

        canvas.blit(cube, (x, y))

        x += b.getBezier(t)[0:2][1]

        t = x / (WIDTH - 50)

        if t >= 1:
            t = 0
            x = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


class Enemy:
    def __init__(self, startPos, endPos, speedType="linear", speedValue=1, moveType="line", moveValue=(), **kwargs):
        if self.startPos == "same_line":
            dm = kwargs["dm_target"]
            hero = kwargs["hero"]
            if dm.x == hero.x:
                pass
            elif dm.y == hero.y:
                pass
            else:
                dmPos = (dm.x, dm.y)
                hPos = (hero.x, hero.y)
                
        self.startPos = startPos
        self.endPos = endPos
        self.speedType = speedType
        self.speedValue = speedValue
