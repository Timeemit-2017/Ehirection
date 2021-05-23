import pygame
from pygame.locals import *

pygame.init()

class LobbyVar():
    times = 8
    moveSpeed = 0
    canvas = pygame.image.load("images/lobby/images/hall_canvas.png")
    canvas = pygame.transform.scale(canvas, (62 * times, 62 * times))

class LobbyObject(object):
    def __init__(self,x,y,width,height,name):
        self.times = LobbyVar.times
        self.x = x * self.times
        self.y = y * self.times
        self.width = width * self.times
        self.height = height * self.times
        self.name = name
        self.sourse = pygame.image.load("images/lobby/images/hall_" + self.name + ".png")
        self.img = pygame.transform.scale(self.sourse, (self.width, self.height))
        self.item = False
    def draw(self,surface):
        surface.blit(self.img, (self.x, self.y))

class LobbyItem(LobbyObject):
    def __init__(self,land_x,land_width,width,height,name):
        x = land_x * 2 + 10
        y = int(-16 / 31 * x - 22)
        y = y * -1 - height + land_width - 1
        LobbyObject.__init__(self,x,y,width,height,name)
        self.item = True
        self.land_x = land_x
        self.origin_land_x = self.land_x
        self.land_width = land_width
        self.speed = LobbyVar.moveSpeed
        self.lighted = False
        self.highlight_sourse = pygame.image.load("images/lobby/images/hall_" + self.name + "_highlight.png")
        self.highlight = pygame.transform.scale(self.highlight_sourse, (self.width, self.height))
    def draw(self,surface):
        if self.outOfBounds():
            return
        surface.blit(self.img, (self.x, self.y))
        self.draw_highlight(surface)
    def draw_highlight(self,surface):
        if self.lighted:
            surface.blit(self.highlight, (self.x, self.y))
    def step(self,direction,last_fps_time):
        self.speed = LobbyVar.moveSpeed
        last_fps_time = last_fps_time / 1000
        self.x += direction * 2 * self.speed * self.times * last_fps_time
        self.y += direction * 1 * self.speed * self.times * last_fps_time
        self.land_x += direction * 1 * self.speed * last_fps_time
    def outOfBounds(self):
        if self.land_x < 0 - self.land_width or self.land_x > 16:
            return True
    def checkRange(self, x, y, width, height):
        return x > self.x and x < self.x + self.width and \
               y > self.y and y < self.y + self.height
    def checkHit(self,object):
        o = object
        return self.checkRange(o.x, o.y, o.width, o.height)
    def checkPlayer(self,player):
        p = player
        return player.land_x + player.land_width > self.land_x and player.land_x < self.land_x + self.land_width

class LobbyForceControl():
    def __init__(self):
        pass
    def lobbyAddForce(self, force=0.3, maxSpeed=13):
        LobbyVar.moveSpeed += force
        if LobbyVar.moveSpeed >= maxSpeed:
            LobbyVar.moveSpeed = maxSpeed
    def lobbyFriction(self, friction=15):
        # print("lobbyFriction")
        LobbyVar.moveSpeed -= friction
        if LobbyVar.moveSpeed < 0:
            LobbyVar.moveSpeed = 0
