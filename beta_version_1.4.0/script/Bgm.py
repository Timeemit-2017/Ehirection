import os, pygame, random, time
from script.basic import *

pygame.mixer.init()


class Bgm:
    def __init__(self):
        self.basicPath = "./songs/main_page/"
        self.songsPaths = os.listdir(self.basicPath)
        print(self.songsPaths)
        self.lastTime = 0
        self.interval = 0
        self.temp = 1

    def set(self):
        self.lastTime = 0

    def play(self):
        if not ifDoAction(self.lastTime, self.interval + 1):
            if self.temp == 1:
                pygame.mixer.music.play()
                self.temp = 0
        else:
            self.lastTime = time.time()
            self.bgm_init()
            pygame.mixer.music.stop()
            if self.temp == 0:
                self.temp = 1
                return

    def bgm_init(self):
        path = self.basicPath + self.songsPaths[random.randint(0, len(self.songsPaths) - 1)]
        print(path)
        temp = pygame.mixer.Sound(path)
        self.interval = temp.get_length()
        pygame.mixer.music.load(path)
