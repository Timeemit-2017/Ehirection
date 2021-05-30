import pygame
from script.Animation import *

pygame.init()

class Pool():
    def __init__(self, img):
        self.img = img
        self.img_orgin = self.img
    def draw(self, target):
        target.blit(self.img, (0,0))
    def set_size(self, screen_size):
        self.img = pygame.transform.scale(self.img_orgin, screen_size)
    def update(self):
        self.img = self.img_orgin


class PoolButton(Sprite):
    def __init__(self,source,position,pos,size,text):
        Sprite.__init__(self, source, position, pos, size, 0)
        self.text = text
        self.minus_size = (self.position[0] / 1920, self.position[1] / 1080)
    def animation(self, mouse_press):
        if mouse_press == True:
            self.index = 1
        else:
            self.index = 0
    def set_pos(self,screen_size):
        self.position = (screen_size[0] * self.minus_size[0], screen_size[1] * self.minus_size[1])
    def checkRange(self, pos, size=(1, 1)):
        x = pos[0]
        y = pos[1]
        width = size[0]
        height = size[1]
        return x > self.position[0] - width and x < self.position[0] + 40 * 5 and \
               y > self.position[1] - height and y < self.position[1] + 16 * 5



class Preview():
    def __init__(self, img, pos, word, word_dire,text=None):
        self.img = img  # 放大后的图片，不支持自己放大
        self.pos = pos  # 相对于Pool.img的坐标
        self.word = word  # 一张图片
        self.text = text  # 使用三引号的字符串（可选）
        self.word_surface = pygame.Surface((self.word.get_size[0], self.word.get_size[1]))
        self.word_dire = word_dire # 1 或 -1
        self.word_pos = (0, self.word_dire * self.word_surface.get_width())
        self.speed = 6
    def set_pos(self,screen_size):
        minus_size = (self.position[0] / 1920, self.position[1] / 1080)
        self.position = (screen_size[0] * minus_size[0], screen_size[1] * minus_size[1])
    def draw_word(self,target):
        self.word_surface.blit(self.word, self.word_pos)
        target.blit(self.word_surface, (self.pos[0] - self.word_surface.get_width(), self.pos[1]))
    def animation(self):
        self.word_pos[0] += -self.word_dire * 6
        if self.word_dire == 1 and self.word_pos < 0:
            self.word_pos = (0, 0)
        elif self.word_dire == -1 and self.word_pos > 0:
            self.word_pos = (0, 0)