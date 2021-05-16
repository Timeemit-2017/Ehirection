import pygame
from pygame.locals import *


class Arrow(object):
    def __init__(self, mode, img, time, dire):
        self.mode = mode
        self.img = img
        self.size = img.get_size()
        self.time = time
        self.dire = dire
        self.if_highLight = False
        self.pos = (0, 0)
        self.width = self.img.get_width()
    def draw_pos(self, canvas, pos):
        canvas.blit(self.img, pos)

    def draw(self, times, canvas, thisTime, set=None, list=None):
        video_size = canvas.get_size()
        pos = (video_size[0] / 2 - self.size[0] / 2 - (thisTime - self.time) * times,
               video_size[1] / 2 - self.size[1] / 2
               )
        self.pos = pos
        self.checkHighLightRange(pos, video_size)
        if not 0 - self.width < pos[0] < video_size[0]:
            return
        canvas.blit(self.img, pos)

    def drawHighLight(self, canvas, color=(255, 255, 255)):
        rect = self.img.get_rect()
        rect.move_ip(self.pos[0], self.pos[1])
        pygame.draw.rect(canvas, color, rect, width=1)

    def checkHighLight(self, pos, video_size, set=None, list=None):
        # 已停用
        if not set == None and set and self in list:
            self.if_highLight = set
            return
        x = pos[0]
        width = self.width
        if video_size[0] / 2 - width <= x <= video_size[0] / 2:
            self.if_highLight = True
        else:
            self.if_highLight = False

    def setHighLight(self, target):
        self.if_highLight = target

    def checkHighLightRange(self, pos, video_size):
        x = pos[0]
        width = self.width
        if video_size[0] / 2 - width <= x <= video_size[0] / 2:
            self.if_highLight = True
        else:
            self.if_highLight = False


    def setImg(self, img):
        self.img = img
        self.size = self.img.get_size()
        self.width = self.img.get_width()
