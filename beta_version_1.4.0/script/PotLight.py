import pygame
from pygame.locals import *

pygame.init()

class PotLight:
    def __init__(self, size, lightColor, canvas, backgroundColor=(0, 0, 0), lightStrength=70, pos=(0, 0),
                 if_background=False):
        self.size = size
        self.lightColor = lightColor
        self.backgroundColor = backgroundColor
        self.lightStrength = lightStrength  # 越大越暗
        self.if_background = if_background
        self.light = self.potLight()
        self.pos = pos
        self.canvas = canvas

    def potLight(self):
        global bg_example
        """生成光的图片"""
        sur = pygame.Surface((self.size, self.size), SRCALPHA)
        bg = pygame.Surface((self.size * 2, self.size * 2), SRCALPHA)
        under = pygame.Surface((self.size, self.size), SRCALPHA)
        under.fill(self.lightColor)
        # 绘制单个挡板
        for y in range(int(-self.size / 2), int(self.size / 2)):
            for x in range(int(-self.size / 2), int(self.size / 2)):
                a = 255 - abs((x / self.size * 255) * (y / self.size * 255)) / self.lightStrength
                a = alphaRange(a)
                sur.set_at((x + int(self.size / 2), y + int(self.size / 2)), self.backgroundColor + tuple([a]))
        # 将四个挡板绘制在背景上。
        for y in range(0, 2 * self.size, self.size):
            for x in range(0, 2 * self.size, self.size):
                bg.blit(sur, (x, y))
        # 将颜色放在挡板后，使之产生颜色效果。
        under.blit(bg, (0 - sur.get_width() / 2, 0 - sur.get_height() / 2))
        # 去背景。
        if self.if_background:
            return under
        for y in range(self.size):
            for x in range(self.size):
                colorKey = list(under.get_at((x, y)))
                colorKey[3] = colorKey[0] - self.backgroundColor[0]
                colorKey = tuple(colorKey)
                under.set_at((x, y), colorKey)
        bg_example = bg  # 仅演示用！
        return under

    def draw(self, pos=None):
        """绘制"""
        if pos is None:
            p = self.pos
        else:
            p = pos
        self.canvas.blit(self.light, p)

    def move(self, pos):
        """改变位置"""
        self.pos = pos

    def update(self):
        """更新图片，用在改变参数之后。（运行很慢）"""
        self.light = self.potLight()


def alphaRange(a):
    if a > 255:
        a = 255
    elif a < 0:
        a = 0
    return a
