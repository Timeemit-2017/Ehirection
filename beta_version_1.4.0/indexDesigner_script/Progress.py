import pygame

pygame.init()


class Progress:
    def __init__(self, canvas):
        self.width = 0
        self.height = 10
        self.color = (255, 255, 255)
        self.hoverColor = (155, 155, 155)
        self.time = 0
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.canvas = canvas

    def draw(self):
        pygame.draw.rect(self.canvas, self.color, self.rect)

    def hover(self, mouse_x):
        temp = pygame.Rect(0, 0, mouse_x, self.height)
        pygame.draw.rect(self.canvas, self.hoverColor, temp)

    def update(self, thisTime, songTime, WIDTH):
        self.rect.update(0, 0, thisTime / songTime * WIDTH, self.height)

    def render(self, MOUSE_POS):
        if 0 <= MOUSE_POS[1] <= self.height:
            self.hover(MOUSE_POS[0])
        self.draw()

    def main(self, thisTime, songTime, WIDTH, MOUSE_POS):
        self.render(MOUSE_POS)
        self.update(thisTime, songTime, WIDTH)
