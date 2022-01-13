import os
import pygame
import random
import time
from script.basic import ifDoAction


class Bgm:
    def __init__(self, road):
        self.road = road  # 背景音乐文件夹路径
        self.lastTime = 0
        self.interval = 0
        self.songs = []
        self.songIndex = 0  # 歌曲编号
        self.path = ""
        self.start = "init"  # 是否为刚启动的标识

    def init(self):
        self.songs = os.listdir(self.road)
        self.set()

    def set(self):
        self.songIndex = random.randint(0, len(self.songs) - 1)
        self.path = self.road + "/" + self.songs[self.songIndex]
        temp = pygame.mixer.Sound(self.path)
        self.interval = temp.get_length()  # 秒
        self.lastTime = 0

    def play(self):
        if not ifDoAction(self.lastTime, self.interval + 1):
            return
        self.lastTime = time.time()
        if self.start is not "init":
            self.set()
        self.bgm_init()
        pygame.mixer.music.play()

    def bgm_init(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.path)
        pygame.mixer.music.set_volume(1)

