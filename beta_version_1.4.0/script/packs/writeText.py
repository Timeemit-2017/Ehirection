import pygame,time
from script.Images import *
pygame.init()

#创建是否到了画组件时间的方法
def ifDoAction(lastTime,interval):
        if lastTime==0:
            return True
        currectTime=time.time()
        return currectTime-lastTime>=interval


def textInit(size,font):
    font = pygame.font.Font(font, size)
    return font

class Font():
    text = textInit(30,"ttfs/noto/NotoSansHans-Light.otf")
    console = textInit(15,"ttfs/noto/NotoSansHans-Light.otf")
    text_bold = textInit(30,"ttfs/noto/NotoSansHans-Bold.otf")
    text_regular = textInit(30, "ttfs/noto/NotoSansHans-Regular.otf")
    score = textInit(40,"ttfs/noto/NotoSansHans-Light.otf")

def writeText(text, position, color=(255,255,255), alpha=255, font=Font.text):
    text = font.render(text, True, color)
    if not alpha == 255:
        text.set_alpha(alpha)
    canvas.blit(text, position)