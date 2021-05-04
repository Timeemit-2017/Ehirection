import pygame,time
pygame.init()
def ifDoAction(lastTime, interval):
    if lastTime == 0:
        return False
    currectTime = time.time()
    return currectTime - lastTime >= interval

def textInit(size,font):
    font = pygame.font.Font(font, size)
    return font

def writeText(text, position, color, font,canvas):
    text = font.render(text, True, color)
    canvas.blit(text, position)

class Font():
    text = textInit(30,"ttfs/noto/NotoSansHans-Light.otf")
    score = textInit(40,"ttfs/noto/NotoSansHans-Light.otf")

