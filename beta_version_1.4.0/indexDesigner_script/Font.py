import pygame
from pygame.locals import *

pygame.init()

class Font():
    normal_text = pygame.font.Font("ttfs/fangzheng/fzHei.TTF", 30)
    small_normal_text = pygame.font.Font("ttfs/fangzheng/fzHei.TTF", 15)

def renderText(text, pos, canvas, color = (255,255,255), font=Font.normal_text, alpha=255, leftLine=False):
    text = text.encode("UTF-8")
    text = font.render(text, True, color)
    if not alpha == 255:
        surface = pygame.Surface((text.get_width(), text.get_height()), SRCALPHA).convert()
        surface.set_alpha(alpha)
        surface.blit(text, (0,0))
        canvas.blit(surface, pos)
        return
    if leftLine:
        canvas.blit(text, (pos[0] - text.get_width(), pos[1]))
    else:
        canvas.blit(text, pos)
