'''
Created on 2019-12-31

@author: Time_emit
'''
import pygame,random,time,sys,os
from pygame.locals import *
#初始化
pygame.init ()


canvas = pygame.display.set_mode((960, 720))
canvas.fill((255,255,255))
#设置标题
pygame.display.set_caption("八方")
#加载英雄图片
yellowC=pygame.image.load("images/mainC/yellowC.png")
yellowM=pygame.image.load("images/mainC/yellowM.png")
#加载敌人图片
yellow=pygame.image.load("images/yellow.png")
#加载判子图片
yellowDM=pygame.image.load("images/DMcs/yellowCM.png")
#加载背景图片
bgBlack=pygame.image.load("images/bgBlack.png")
#加载歌曲选单图片
cph=pygame.image.load("images/start/changpianhuan.png")
#加载歌曲封面
his_theme=pygame.image.load("images/start/songs/his_theme.jpg")
tyx=pygame.image.load("images/start/songs/tyx.jpg")
shib=pygame.image.load("images/start/songs/shib.jpg")
piano=pygame.image.load("images/start/songs/The_Piano.png")
#加载死亡图片素材
die=pygame.image.load("images/end/died.png")
win=pygame.image.load("images/end/success.png")
lose=pygame.image.load("images/end/failed.png")
score=pygame.image.load("images/end/score.png")

#设置变量基础数值
enemyAttack=5

#创建handleEvent方法     
def handleEvent():  
    for event in pygame.event.get():
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
        elif GameVar.states==GameVar.STATES["HOME_0"]:
            if event.type==KEYDOWN:
                GameVar.states=GameVar.STATES["SONGS_CHOOSE"]
        elif GameVar.states==GameVar.STATES["SONGS_CHOOSE"]:
            #print("SONGS_CHOOSE")
            if event.type==KEYDOWN and event.key==K_UP:
                GameVar.songChoose.dire = True
                GameVar.songChoose.set(GameVar.songChoose.dire)
                GameVar.songChoose.number2 = GameVar.songChoose.number1 - 1
                GameVar.songChoose.check()
                GameVar.songChoose.start = True
            elif event.type==KEYDOWN and event.key==K_DOWN:
                GameVar.songChoose.dire = False
                GameVar.songChoose.set(GameVar.songChoose.dire)
                GameVar.songChoose.number2 = GameVar.songChoose.number1 + 1
                GameVar.songChoose.check()
                GameVar.songChoose.start = True
            elif event.type==KEYDOWN and event.key==13:
                GameVar.states=GameVar.STATES["START"]
        elif GameVar.states==GameVar.STATES["RUNNING"]:
            if event.type==KEYDOWN and event.key==K_UP:
                GameVar.DMcomp[0].iflighted = True
            if event.type==KEYDOWN and event.key==K_RIGHT:
                GameVar.DMcomp[1].iflighted = True
            if event.type==KEYDOWN and event.key==K_DOWN:
                GameVar.DMcomp[2].iflighted = True
            if event.type==KEYDOWN and event.key==K_LEFT:
                GameVar.DMcomp[3].iflighted = True
            if event.type==KEYUP and event.key==K_UP:
                GameVar.DMcomp[0].iflighted=False
            if event.type == KEYUP and event.key == K_RIGHT:
                GameVar.DMcomp[1].iflighted = False
            if event.type == KEYUP and event.key == K_DOWN:
                GameVar.DMcomp[2].iflighted = False
            if event.type == KEYUP and event.key == K_LEFT:
                GameVar.DMcomp[3].iflighted = False
        elif GameVar.states==GameVar.STATES["GAME_OVER"]:
            if event.type==KEYDOWN and event.key==13:
                GameVar.skip+=1
                if GameVar.skip>3:
                    GameVar.skip=3
#创建是否到了画组件时间的方法
def ifDoAction(lastTime,interval):
        if lastTime==0:
            return True
        currectTime=time.time() 
        return currectTime-lastTime>=interval


def textInit(size):
    font = pygame.font.Font("ttfs/noto/NotoSansHans-Light.otf", size)
    return font


def writeText(text, position, color, font):
    text = font.render(text, True, color)
    canvas.blit(text, position)


class Font():
    text = textInit(30)
    score = textInit(40)


#创建Hero类            
class Hero():
    def __init__(self,life,defence):
        self.life=life
        self.defeat=defence
        self.score=0
        self.x=480-25
        self.y=360-25
        self.width=50
        self.height=50
        self.mainImg=yellowM
        self.CImg=yellowC
        self.Cy=360-25
        self.rect=self.mainImg.get_rect()
        self.rect.topleft=(self.x,self.y+self.height)
    def draw(self):
        canvas.blit(self.CImg,(480-25,self.Cy))
        pygame.draw.rect(canvas,(0,0,0),self.rect)
        canvas.blit(self.mainImg, (480 - 25, 360 - 25))
    def lifeErase(self):
        self.life-=5-5*self.defeat
    def Cstep(self):
        if self.Cy<self.y+self.height:
            self.Cy+=2
            return False
        else:
            self.Cy=self.y+self.height
            return True
    def bang(self):
        self.lifeErase()
    def hit(self,component):
        c=component
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
            

#创建背景类
class BG():
    def __init__(self):
        self.number=0
        self.x=0
        self.y=0
    def draw(self,image):
        canvas.blit(image,(self.x,self.y))


class End():
    def __init__(self):
        self.result=False
        self.score_img=score
        self.dieImg=die
        self.speed=20
    def draw(self):
        canvas.blit(self.dieImg,(0,0))
        canvas.blit(self.result_img,(self.result_x,self.result_y))
        canvas.blit(self.score_img,(self.score_x,self.score_y))
    def init(self):
        self.score = GameVar.hero.score
        if GameVar.hero.life>0:
            self.result_x = 0 - 362
            self.result_img=win
        else:
            self.result_x = 0 - 316
            self.result_img=lose
        self.result_y=0
        self.score_x=self.result_x-162
        self.score_y=0
    def animate(self):
        self.result_x+=self.speed
        self.score_x+=self.speed
    def animateOver(self):
        if self.result_x>=0:
            self.result_x=0
        if self.score_x>=0:
            self.score_x=0


class SongChoose():
    def __init__(self,imgs,cph):
        self.dire=True
        self.start=False
        self.width = 250
        self.height = 250
        self.x1 = 480 - self.width / 2
        self.x2 = self.x1
        self.y1 = 360 - self.height / 2
        self.y2 = 1080 - self.height / 2
        self.imgs=imgs
        self.cph=cph
        self.number1=0
        self.number2=1
        self.cphy1=0
        self.cphy2=720
    def draw(self):
        canvas.blit(self.imgs[self.number1], (self.x1-1, self.y1-1))
        canvas.blit(self.cph, (0,self.cphy1))
        canvas.blit(self.imgs[self.number2], (self.x2-1, self.y2-1))
        canvas.blit(self.cph, (0,self.cphy2))
    def set(self,dire):
        self.dire=dire
        if self.dire==True:#dire为True向下,反之向上
            self.y1=360-self.height/2
            self.y2=-360-self.height/2
            self.cphy1=0
            self.cphy2=-720
        else:
            self.y1=360-self.height/2
            self.y2=1080-self.height/2
            self.cph1=0
            self.cphy2=720
    def step(self):
        speed=25
        if self.dire==True:
            self.y1+=speed
            self.y2+=speed
            self.cphy1+=speed
            self.cphy2+=speed
        else:
            self.y1 -= speed
            self.y2 -= speed
            self.cphy1 -= speed
            self.cphy2 -= speed
    def ifAnimeTime(self):
        if self.dire==True:
            if self.cphy1>=720:
                self.number(self.dire)
                self.start=False
                return True
            else:
                return False
        else:
            if self.cphy1<=-720:
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
            self.set(self.dire)
            self.cphy1 = 0
        self.draw()
        self.anime()


class GameVar():
    hero=Hero(50.0,0.0)
    bg=BG()
    #敌人刷新时间
    lastTime=0
    intertal=0.5
    #用列表存储敌人
    enemies = []
    #绘画时间
    paintLastTime=0
    paintIntertal=0
    #判子绘画时间
    DMLastTime=0
    DMIntertal=0
    #主界面文字闪烁时间
    homeWordLastTime=0
    homeWordIntertal=1
    #歌曲列表索引
    indexOfSong=1
    #歌曲开始时间
    gameStart=0
    #选单页数
    songsPage=2
    #用列表存储判子
    DMcomp = []
    #歌曲是否要切换
    songsChangeAni=False
    #歌曲切换的方向
    songsChangeDire=False
    #是否在播放歌曲
    ifsongplaying=False
    #当前在播放的曲子谱面
    thisSong=[]
    #最后一个谱子的时间
    lastIndexTime=99999
    #是否要暂停
    pause=False
    #歌曲列表
    songs=["His Theme","惑星ループ ","Fragments","失波(Lost Frequencis)","Text","Text","Text"]
    #歌曲列表
    song_names = ["The_Piano","his_theme", "solar_system", "Lost_Frequencis"]
    #歌曲封面列表
    songsImages=[piano,his_theme,tyx,shib]
    # 歌曲选单类
    songChoose = SongChoose(songsImages,cph)
    #结束类
    end=End()
    #结束时的time.time()
    this_time=0
    #结束是否跳过
    skip=0
    #帧率控制模块初始化
    fpsClock = pygame.time.Clock()
    #帧率
    fps=24
    #使用字典存储游戏进程
    STATES={"HOME_0":1,"HOME_1":2,"SONGS_CHOOSE":3,"SONGS_CHOOSE_2":4,"START":5,"RUNNING":6,"GAME_OVER":7}
    states=STATES["HOME_0"]

#创建Enemy类
class Enemy(object):
    def __init__(self,number):
        self.width=50
        self.height=50
        self.number=number
        self.attack=enemyAttack
        self.color=yellow
        self.delete=False
        self.lastTime=0
        self.interval=0.01
        if self.number=="1" or self.number==1:
            self.x=480-25
            self.y=0-self.height
        elif self.number=="2" or self.number==2:
            self.x=840
            self.y=360-25
        elif self.number=="3" or self.number==3:
            self.x=480-25
            self.y=720
        elif self.number=="4" or self.number==4:
            self.x=120-self.width
            self.y=360-25
    def draw(self):
        canvas.blit(self.color,(self.x,self.y))
    def step(self):
        if self.number=="1" or self.number==1:
            self.y+=100 *last_fps_time /385
        elif self.number=="2" or self.number==2:
            self.x-=100 *last_fps_time/385
        elif self.number=="3" or self.number==3:
            self.y-=100*last_fps_time /385
        else:
            self.x+=100*last_fps_time /385
    def hit(self,component):
        c=component
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
    def bang(self,if_score):
        self.delete=True
        if if_score:
            GameVar.hero.score+=5



#创建判子类
class DMcomponent():
    def __init__(self,number,iflighted):
        #基础数值
        self.number=number
        self.iflighted=iflighted
        if self.number==0:
            self.x=GameVar.hero.x
            self.y=GameVar.hero.y-85
        elif self.number==1:
            self.x=GameVar.hero.x+85
            self.y=GameVar.hero.y
        elif self.number==2:
            self.x=GameVar.hero.x
            self.y=GameVar.hero.y+85
        elif self.number==3:
            self.x=GameVar.hero.x-85
            self.y=GameVar.hero.y
        self.x=self.x
        self.y=self.y
        self.width=50
        self.height=50
        self.img=yellowDM
        self.imgLighted=yellow
        self.color=self.img
    def checkLighted(self):
            if self.iflighted:
                self.color=self.imgLighted
            else:
                self.color=self.img
    def draw(self):
        self.checkLighted()
        canvas.blit(self.color,(self.x,self.y)) 
    def lighten(self):
        if self.iflighted==True:
            self.iflighted=False
        else:
            self.iflighted=True  
    def hit(self,component):
        c=component
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
    def bang(self):
        if self.hit==True:
            GameVar.hero.score+=1

#游戏中
def commentInit():
    GameVar.DMcomp.clear()
    GameVar.DMcomp.append(DMcomponent(0,False))
    GameVar.DMcomp.append(DMcomponent(1,False))
    GameVar.DMcomp.append(DMcomponent(2,False))
    GameVar.DMcomp.append(DMcomponent(3,False))
    
def commentEnter(song):
    GameVar.lastTime=time.clock()-GameVar.gameStart
    if not GameVar.indexOfSong>=len(song)-1:
        if GameVar.lastTime>=song[GameVar.indexOfSong+1]:
            GameVar.enemies.append(Enemy(song[GameVar.indexOfSong]))
            GameVar.indexOfSong+=2
    else:
        GameVar.lastIndexTime = song[-1]
        if GameVar.lastTime>=GameVar.lastIndexTime+10:
            GameVar.states=GameVar.STATES["GAME_OVER"]
            return

def commentDraw():
    GameVar.hero.draw()
    if not ifDoAction(GameVar.paintLastTime,GameVar.paintIntertal):
        return
    GameVar.paintLastTime=time.time()
    for component in GameVar.DMcomp:
        component.draw()
    for enemy in GameVar.enemies:
        enemy.draw()

def commentStep():
    for enemy in GameVar.enemies:
        enemy.step()

def commentDelete():
    for enemy in GameVar.enemies:
        if GameVar.hero.hit(enemy):
            enemy.bang(False)
            GameVar.hero.bang()
        for DM in GameVar.DMcomp:
            if DM.iflighted == True and DM.hit(enemy):
                enemy.bang(True)
        if enemy.delete:
            GameVar.enemies.remove(enemy)

          

def song_init():
    GameVar.hero.Cy = 360 - 25
    GameVar.indexOfSong = 1
    GameVar.gameStart = time.clock()
    GameVar.hero.life = 50.0
    GameVar.ifsongplaying = False
    GameVar.hero.score = 0
    GameVar.skip = -1
    GameVar.enemies = []
    pygame.mixer.init()
    pygame.mixer.music.load("songs/foundation_pack/" +GameVar.song_names[GameVar.songChoose.number1] + ".mp3")
    pygame.mixer.music.set_volume(0.2)
    GameVar.states = GameVar.STATES["RUNNING"]



def control():
    if GameVar.states==GameVar.STATES["HOME_0"]:
        GameVar.bg.draw(bgBlack)
        writeText("按下任意键开始游戏",(365,660),(255,255,255),Font.text)
    elif GameVar.states==GameVar.STATES["HOME_1"]:
        GameVar.bg.draw(bgBlack)
    elif GameVar.states==GameVar.STATES["SONGS_CHOOSE"]:
        GameVar.bg.draw(bgBlack)
        GameVar.songChoose.main()
    elif GameVar.states==GameVar.STATES["SONGS_CHOOSE_2"]:
        GameVar.states=GameVar.STATES["START"]
    elif GameVar.states==GameVar.STATES["START"]:
        commentInit()
        GameVar.gameStart=time.clock()
        with open("songs.txt") as file:
            for line in file:
                if eval(line.rstrip())[0]==GameVar.song_names[GameVar.songChoose.number1]:
                    GameVar.thisSong=eval(line.rstrip())
        song_init()
    elif GameVar.states==GameVar.STATES["RUNNING"]:
        GameVar.bg.draw(bgBlack)
        commentEnter(GameVar.thisSong)
        commentDraw()
        commentStep()
        commentDelete()
        writeText("Health:"+str(GameVar.hero.life),(0,0),(255,255,255),Font.text)
        writeText("Score:"+str(GameVar.hero.score),(0,40),(255,255,255),Font.text)
        if GameVar.ifsongplaying==False and time.clock()-GameVar.gameStart>=1.2:
            pygame.mixer.music.play()
            GameVar.ifsongplaying=True
        if GameVar.hero.life<=0 or time.clock()-GameVar.gameStart>GameVar.thisSong[-1]+3:
            GameVar.states = GameVar.STATES["GAME_OVER"]
            GameVar.end.init()
            GameVar.this_time=time.time()
        #print(GameVar.lastTime)
    elif GameVar.states==GameVar.STATES["GAME_OVER"]:
        GameVar.bg.draw(bgBlack)
        commentDraw()
        if GameVar.hero.life<=0:
            if not GameVar.hero.Cstep() and GameVar.skip==-1:
                return
            elif GameVar.skip==-1:
                GameVar.skip=0
        else:
            if GameVar.skip==-1:
                GameVar.skip = 0
        if GameVar.skip==0:
            if GameVar.end.result:
                GameVar.hero.Cy=385
            GameVar.end.draw()
            GameVar.end.animate()
            GameVar.end.animateOver()
            if ifDoAction(GameVar.this_time+1,2):
                writeText(str(GameVar.hero.score),(170,239),(255,228,0),Font.score)
                GameVar.skip=1
        elif GameVar.skip==1:
            if GameVar.end.result:
                GameVar.hero.Cy = 385
            GameVar.end.result_x=0
            GameVar.end.score_x=0
            GameVar.end.draw()
            writeText(str(GameVar.hero.score), (170, 239), (255, 228, 0),Font.score)
        elif GameVar.skip==2:
            GameVar.end.draw()
            GameVar.states=GameVar.STATES["SONGS_CHOOSE"]
            pygame.mixer.quit()


while True:

    last_fps_time = GameVar.fpsClock.tick(GameVar.fps)

    control()
    
    pygame.display.update()
    
    handleEvent()

