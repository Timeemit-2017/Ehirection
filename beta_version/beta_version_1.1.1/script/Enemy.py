from script.Objects import *
from script.Images import *
import script.GameVar

#创建Enemy类
class Enemy(GameObject):
    def __init__(self,number):
        GameObject.__init__(self,1,0,0,0,50,50,yellow)
        self.number=number
        self.attack=5
        self.delete=False
        self.hero_distance = 385
        if self.number=="1" or self.number==1:
            self.x = GameVar.hero.x
            self.y = GameVar.hero.y - self.hero_distance
        elif self.number=="2" or self.number==2:
            self.x = GameVar.hero.x + self.hero_distance
            self.y = GameVar.hero.y
        elif self.number=="3" or self.number==3:
            self.x = GameVar.hero.x
            self.y = GameVar.hero.y + self.hero_distance
        elif self.number=="4" or self.number==4:
            self.x = GameVar.hero.x - self.hero_distance
            self.y = GameVar.hero.y
    def step(self):
        if self.number=="1" or self.number==1:
            self.y+=100 *last_fps_time /385
        elif self.number=="2" or self.number==2:
            self.x-=100 *last_fps_time/385
        elif self.number=="3" or self.number==3:
            self.y-=100*last_fps_time /385
        else:
            self.x+=100*last_fps_time /385
    def bang(self,if_score):
        self.life -= 1
        if self.life <= 0:
            self.delete = True
        if if_score:
            GameVar.hero.score+=5