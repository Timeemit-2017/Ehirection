import pygame, time
from pygame.locals import *

pygame.init()

def textInit(size, font):
    font = pygame.font.Font(font, size)
    return font

class Font():
    song_name = textInit(80, "ttfs/noto/NotoSansHans-Light.otf")
    text = textInit(30, "ttfs/noto/NotoSansHans-Light.otf")
    little_text = textInit(20, "ttfs/noto/NotoSansHans-Light.otf")
    console = textInit(15, "ttfs/noto/NotoSansHans-Light.otf")
    text_bold = textInit(30, "ttfs/noto/NotoSansHans-Bold.otf")
    text_regular = textInit(30, "ttfs/noto/NotoSansHans-Regular.otf")
    score = textInit(40, "ttfs/noto/NotoSansHans-Light.otf")

def writeText(text, position, canvas, color=(255, 255, 255, 255), alpha=255, font=Font.text, is_middle=False,
              is_right_bottom=False, is_right=False, move_pos=None, is_rect_and_color=(False, (255, 0, 0)), is_return_size=False):
    text = font.render(text, True, color)
    if is_middle:
        pos = (position[0] - text.get_width() / 2, position[1] - text.get_height() / 2)
        position = pos
    elif is_right_bottom:
        pos = (position[0] - text.get_width(),
               position[1] - text.get_height())
        position = pos
    elif is_right:
        pos = (position[0] - text.get_width(), position[1])
        position = pos
    elif move_pos is not None:
        pos = (position[0] + move_pos[0], position[1] + move_pos[1])
        position = pos
    if not alpha == 255:
        surface_under = pygame.Surface((text.get_width(), text.get_height()), SRCALPHA).convert()
        surface_under.blit(text, (0, 0))
        surface_under.set_alpha(alpha)
        canvas.blit(surface_under, position)
    else:
        canvas.blit(text, position)
    if is_rect_and_color[0]:
        pygame.draw.rect(canvas, is_rect_and_color[1], (position[0], position[1], text.get_width(), text.get_height()),
                         width=1)
    if is_return_size:
        return text.get_size()




# 创建是否到了画组件时间的方法
def ifDoAction(lastTime, interval):
    if lastTime == 0:
        return True
    currectTime = time.time()
    return currectTime - lastTime >= interval
