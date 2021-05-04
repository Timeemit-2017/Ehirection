import pygame
from script.Images import *
pygame.init()

#创建背景类
class BG():
    def __init__(self):
        self.number=0
        self.x=0
        self.y=0
        self.if_night = True
    def draw(self):
        if self.if_night:
            pygame.draw.rect(canvas,(0,0,0),BGblack)