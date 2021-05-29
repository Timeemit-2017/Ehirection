import pygame

class BackGround(object):
    def __init__(self,color=(0,0,0),size=(1280,720)):
        self.color = color
        self.size = size
        self.surface = pygame.Surface(size)
        self.surface.fill(self.color)
    def draw(self,target):
        target.blit(self.surface, (0,0))

