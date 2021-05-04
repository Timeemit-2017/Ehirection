from script.Objects import *
from script.Images import *
import script.GameVar

class SongChoose():
    def __init__(self,imgs,cph):
        self.dire=True
        self.start=False
        self.width = 250
        self.height = 250
        self.x1 = WIDTH/2 - self.width/2
        self.x2 = self.x1
        self.y1 = HEIGHT/2 - self.height/2
        self.y2 = HEIGHT + HEIGHT/2 - self.height/2
        self.imgs=imgs
        self.cph=cph
        self.number1=0
        self.number2=1
        self.cphy1=(HEIGHT - 720)/2
        self.cphy2=HEIGHT + (HEIGHT - 720)/2
        self.song_played=False
    def draw(self):
        canvas.blit(self.imgs[self.number1], (self.x1-1, self.y1-1))
        canvas.blit(self.cph, ((WIDTH - 960)/2,self.cphy1))
        canvas.blit(self.imgs[self.number2], (self.x2-1, self.y2-1))
        canvas.blit(self.cph, ((WIDTH - 960)/2,self.cphy2))
    def set(self,dire):
        self.dire=dire
        if self.dire==True:#dire为True向下,反之向上
            self.y1=HEIGHT_2-self.height/2
            self.y2=-HEIGHT_2-self.height/2
            self.cphy1=(HEIGHT - 720)/2
            self.cphy2=-HEIGHT + (HEIGHT - 720)/2
        else:
            self.y1=HEIGHT_2-self.height/2
            self.y2=HEIGHT + HEIGHT_2 -self.height/2
            self.cph1=(HEIGHT - 720)/2
            self.cphy2=HEIGHT + (HEIGHT - 720)/2
    def step(self):
        speed=360
        if self.dire==True:
            self.y1+=speed *last_fps_time /720
            self.y2+=speed *last_fps_time /720
            self.cphy1+=speed *last_fps_time /720
            self.cphy2+=speed *last_fps_time /720
            # self.y1 += speed * last_fps_time
            # self.y2 += speed * last_fps_time
            # self.cphy1 += speed * last_fps_time
            # self.cphy2 += speed * last_fps_time
        else:
            self.y1 -= speed *last_fps_time /720
            self.y2 -= speed *last_fps_time /720
            self.cphy1 -= speed *last_fps_time /720
            self.cphy2 -= speed *last_fps_time /720
    def ifAnimeTime(self):
        if self.dire==True:
            if self.cphy1>=HEIGHT + (HEIGHT - 720)/2:
                self.number(self.dire)
                self.start=False
                return True
            else:
                return False
        else:
            if self.cphy1<=-HEIGHT + (HEIGHT - 720)/2:
                self.number(self.dire)
                self.start=False
                return True
            else:
                return False
    def anime(self):
        if self.start and not self.ifAnimeTime():
            self.step()
    def number(self,dire):
        if dire==True:
            self.number1-=1
        else:
            self.number1+=1
        if self.number1>len(self.imgs)-1:
            self.number1=0
        elif self.number1<0:
            self.number1=len(self.imgs)-1
        if dire==True:
            self.number2=self.number1-1
        else:
            self.number2=self.number1+1
        if self.number2>len(self.imgs)-1:
            self.number2=0
        elif self.number2<0:
            self.number2=len(self.imgs)-1
    def check(self):
        if self.number2>len(self.imgs)-1:
            self.number2=0
        elif self.number2<0:
            self.number2=len(self.imgs)-1
    def main(self):
        if self.start==False:
            self.cphy1=(HEIGHT - 720)/2
            self.set(self.dire)
        self.draw()
        self.anime()
