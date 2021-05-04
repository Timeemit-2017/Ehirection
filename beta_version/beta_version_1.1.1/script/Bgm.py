import time
from script.packs.writeText import *

class Bgm():
    def __init__(self,road,time):
        self.road = road
        self.time = time
        self.lastTime = 0
        self.interval = self.time
    def set(self):
        self.lastTime = 0
    def play(self):
        if not ifDoAction(self.lastTime,self.interval + 1):
            return
        self.lastTime = time.time()
        self.bgm_init(self.road)
        pygame.mixer.music.play()
    def bgm_init(self,road):
        pygame.mixer.init()
        pygame.mixer.music.load(road)
        pygame.mixer.music.set_volume(0.2)