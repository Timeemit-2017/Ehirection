'''
Created on 2020-3-24

@author: Time_emit
'''
import pygame,random,time,sys,os
from pygame.locals import *
#初始化
pygame.init ()

canvas = pygame.display.set_mode((1280, 720),pygame.FULLSCREEN|pygame.HWSURFACE)
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
#加载道具选取图片素材
item_choose=pygame.image.load("images/item_choose/choose_space.png")
choose=pygame.image.load("images/item_choose/choose.png")
all_item=pygame.image.load("images/item_choose/all_item.png")
#加载道具图片素材
star_light=pygame.image.load("images/items/ehi1st_/star_light.png")
#加载道具特效精灵图
item_effect_sprite=pygame.image.load("images/items/ehi1st_/item_effect_sprite.png")
#设置变量基础数值
enemyAttack=5

#创建handleEvent方法     
def handleEvent():  
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_F1:
            pygame.quit()
            sys.exit()
        elif GameVar.states==GameVar.STATES["HOME_0"]:
            if event.type==KEYDOWN:
                GameVar.states=GameVar.STATES["SONGS_CHOOSE"]
        elif GameVar.states==GameVar.STATES["SONGS_CHOOSE"]:
            #print("SONGS_CHOOSE")
            if event.type==KEYDOWN and event.key==K_UP:
                GameVar.songChoose.cphy1 = 0
                GameVar.songChoose.dire = True
                GameVar.songChoose.set(GameVar.songChoose.dire)
                GameVar.songChoose.number2 = GameVar.songChoose.number1 - 1
                GameVar.songChoose.check()
                GameVar.songChoose.start = True
            elif event.type==KEYDOWN and event.key==K_DOWN:
                GameVar.songChoose.cphy1 = 0
                GameVar.songChoose.dire = False
                GameVar.songChoose.set(GameVar.songChoose.dire)
                GameVar.songChoose.number2 = GameVar.songChoose.number1 + 1
                GameVar.songChoose.check()
                GameVar.songChoose.start = True
            elif event.type==KEYDOWN and event.key==13:
                GameVar.states=GameVar.STATES["SONGS_CHOOSE_2"]
        elif GameVar.states==GameVar.STATES["SONGS_CHOOSE_2"]:

            if GameVar.itemChoose.state==0:
                if event.type==KEYDOWN and event.key==13:
                    GameVar.states=GameVar.STATES["START"]
                elif event.type==KEYDOWN and event.key==K_ESCAPE:
                    GameVar.states=GameVar.STATES["SONGS_CHOOSE"]
                elif event.type == KEYDOWN and event.key == 303:
                    GameVar.itemChoose.state_change(True)
            elif GameVar.itemChoose.state==1:
                if event.type == KEYDOWN and event.key == 303:
                    GameVar.itemChoose.state_change(False)
                elif event.type == KEYUP and event.key == K_UP:
                    GameVar.item_choose_highlight.move("up")
                elif event.type == KEYUP and event.key == K_RIGHT:
                    GameVar.item_choose_highlight.move("right")
                elif event.type==KEYUP and event.key==K_DOWN:
                    GameVar.item_choose_highlight.move("down")
                elif event.type==KEYUP and event.key==K_LEFT:
                    GameVar.item_choose_highlight.move("left")
                elif event.type == KEYUP and event.key == 13:
                    if GameVar.item_choose_highlight.this_item > len(GameVar.items) - 1:
                        GameVar.itemChoose.item_ready = -1
                        GameVar.item_use = "null"
                    else:
                        GameVar.itemChoose.item_ready = GameVar.item_choose_highlight.this_item
                        GameVar.item_use = GameVar.items[GameVar.itemChoose.item_ready]
        elif GameVar.states==GameVar.STATES["RUNNING"]:
            if not event.type == KEYDOWN and not event.type == KEYUP:
                return
            if event.type==KEYDOWN and (event.key==K_UP or event.key == K_w):
                GameVar.DMcomp[0].iflighted = True
                GameVar.DMcomp[0].if_lighted = True
            if event.type==KEYDOWN and (event.key==K_RIGHT or event.key == K_d):
                GameVar.DMcomp[1].iflighted = True
                GameVar.DMcomp[1].if_lighted = True
            if event.type==KEYDOWN and (event.key==K_DOWN or event.key == K_s):
                GameVar.DMcomp[2].iflighted = True
                GameVar.DMcomp[2].if_lighted = True
            if event.type==KEYDOWN and (event.key==K_LEFT or event.key == K_a):
                GameVar.DMcomp[3].iflighted = True
                GameVar.DMcomp[3].if_lighted = True
            if event.type==KEYUP and (event.key==K_UP or event.key == K_w):
                GameVar.DMcomp[0].iflighted=False
                GameVar.DMcomp[0].if_lighted=False
            if event.type == KEYUP and (event.key==K_RIGHT or event.key == K_d):
                GameVar.DMcomp[1].iflighted = False
                GameVar.DMcomp[1].if_lighted = False
            if event.type == KEYUP and (event.key==K_DOWN or event.key == K_s):
                GameVar.DMcomp[2].iflighted = False
                GameVar.DMcomp[2].if_lighted = False
            if event.type == KEYUP and (event.key==K_LEFT or event.key == K_a):

                GameVar.DMcomp[3].iflighted = False
                GameVar.DMcomp[3].if_lighted = False
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


def textInit(size,font):
    font = pygame.font.Font(font, size)
    return font


def writeText(text, position, color, font):
    text = font.render(text, True, color)
    canvas.blit(text, position)


class Font():
    text = textInit(30,"ttfs/noto/NotoSansHans-Light.otf")
    score = textInit(40,"ttfs/noto/NotoSansHans-Light.otf")


#创建Hero类            
class Hero():
    def __init__(self,life,defence):
        self.life=life
        self.defeat=defence
        self.score=0
        self.x=640-25
        self.y=360-25
        self.width=50
        self.height=50
        self.mainImg=yellowM
        self.CImg=yellowC
        self.Cy=360-25
        self.rect=self.mainImg.get_rect()
        self.rect.topleft=(self.x,self.y+self.height)
    def draw(self):
        canvas.blit(self.CImg,(640-25,self.Cy))
        pygame.draw.rect(canvas,(0,0,0),self.rect)
        canvas.blit(self.mainImg, (640 - 25, 360 - 25))
    def lifeErase(self):
        hurt = 5 - self.defeat
        if hurt <=0:
            hurt = 0.1
        self.life -= hurt
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
        self.x1 = 640 - self.width / 2
        self.x2 = self.x1
        self.y1 = 360 - self.height / 2
        self.y2 = 1080 - self.height / 2
        self.imgs=imgs
        self.cph=cph
        self.number1=0
        self.number2=1
        self.cphy1=0
        self.cphy2=720
        self.song_played=False
    def draw(self):
        canvas.blit(self.imgs[self.number1], (self.x1-1, self.y1-1))
        canvas.blit(self.cph, (160,self.cphy1))
        canvas.blit(self.imgs[self.number2], (self.x2-1, self.y2-1))
        canvas.blit(self.cph, (160,self.cphy2))
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
        speed=360
        if self.dire==True:
            self.y1+=speed *last_fps_time /720
            self.y2+=speed *last_fps_time /720
            self.cphy1+=speed *last_fps_time /720
            self.cphy2+=speed *last_fps_time /720
        else:
            self.y1 -= speed *last_fps_time /720
            self.y2 -= speed *last_fps_time /720
            self.cphy1 -= speed *last_fps_time /720
            self.cphy2 -= speed *last_fps_time /720
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
            self.cphy1=0
            self.set(self.dire)
        self.draw()
        self.anime()

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
            self.x=640-25
            self.y=0-self.height
        elif self.number=="2" or self.number==2:
            self.x=1025
            self.y=360-25
        elif self.number=="3" or self.number==3:
            self.x=640-25
            self.y=720
        elif self.number=="4" or self.number==4:
            self.x=230-self.width+25
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

class Item():
    def __init__(self,name,english_name,type,img):
        self.name=name
        self.english_name=english_name
        self.type=type
        self.img=img
        self.lastTime=0
        self.time_left=0
        self.cd=0
        self.time=0
        self.can_use=False
        self.is_using=False
    def draw(self,x,y):
        canvas.blit(self.img,(x,y))




class Item_choose():
    def __init__(self):
        self.state = 0
        self.this_item = -1
        self.item_ready = -1
        self.item_choose = item_choose
        self.choose = choose
        self.all_item = all_item
        self.item_choose_y=0
        self.index=0
        self.line=0
        self.start="Start"
        self.last_time=0
        self.intertal=0.5
    def init(self):
        self.state=0
        self.item_choose_y=0
    def main(self):
        if self.state == 0:
            if self.item_choose_y>0:
                self.animate_0()
                if self.item_choose_y < 0:
                    self.item_choose_y = 0
            #canvas.blit(die, (0, 0))
            canvas.blit(self.item_choose, (0,self.item_choose_y))
            if not self.item_ready == -1:
                canvas.blit(GameVar.items[self.item_ready].img,(591,self.item_choose_y+311))
            self.write_start()
            if self.this_item == -1:
                return
            else:
                canvas.blit(GameVar.items[self.this_item], (591, 311))
        elif self.state==1:
            if self.item_choose_y<134:
                GameVar.songChoose.draw()
                #canvas.blit(die, (0, 0))
                self.animate_1()
                canvas.blit(self.item_choose,(0, self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(GameVar.items[self.item_ready].img, (591, self.item_choose_y + 311))
                return
            else:
                GameVar.songChoose.draw()
                #canvas.blit(die, (0, 0))
                canvas.blit(self.all_item,(0,0))
                canvas.blit(self.item_choose,(0,self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(GameVar.items[self.item_ready].img, (591, self.item_choose_y + 311))
                self.item_draw_1_init()
                self.item_draw_1()
                GameVar.item_choose_highlight.draw()
    def state_change(self, dire):
        if dire:
            self.state += 1
        else:
            self.state -= 1
        if self.state>1:
            self.state=1
        elif self.state<0:
            self.state=0
    def item_draw_1_init(self):
        self.index=0
        self.line=0
    def item_draw_1(self):
        for item in GameVar.items:
            item.draw(335+self.index*(100+3),76+self.line*(100+3))
            self.index+=1
            if self.index>5:
                self.index=0
                self.line+=1
            if self.line>2:
                return True
    def write_start(self):
        writeText(self.start, (1054, 657), (255, 255, 255), Font.text)
        if not ifDoAction(self.last_time,self.intertal):
            return
        self.last_time = time.time()

        if self.start == "Start>>>":
            self.start = "Start"
        self.start = self.start + ">"
    def animate_1(self):
        self.item_choose_y+=37 *last_fps_time/134
    def animate_0(self):
        self.item_choose_y-=37 *last_fps_time/134

class Item_Choose_Highlight(Item_choose):
    def __init__(self):
        super().__init__()
        self.img=choose
    def move(self,dire):
        if self.this_item==-1:
            self.this_item=0
        elif dire=="up":
            if not self.this_item - 6 < 0:
                self.this_item-=6
        elif dire=="right":
            if not self.this_item + 1 > 17:
                self.this_item+=1
        elif dire=="down":
            if not self.this_item + 6 > 17:
                self.this_item+=6
        elif dire=="left":
            if not self.this_item - 1 < 0:
                self.this_item-=1
    def draw(self):
        if self.this_item==-1:
            return
        x = 332 + (self.this_item % 6) * 103 -1
        y = 73 + (self.this_item - self.this_item % 6)/6 * 103 -1
        canvas.blit(self.img,(x,y))


class GameVar():
    hero=Hero(50.0,0.0)
    #英雄初始数值
    hero_defeat=hero.defeat
    hero_life=hero.life
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
    #物品的图片列表
    items=[Item("星光","star_light","挂件",star_light)]
    #物品选择类
    itemChoose=Item_choose()
    #物品选择高光类
    item_choose_highlight=Item_Choose_Highlight()
    #当前使用的物品
    item_use="null"
    item_effect_y=360-50
    #帧率控制模块初始化
    fpsClock = pygame.time.Clock()
    #帧率
    fps=30
    #使用字典存储游戏进程
    STATES={"HOME_0":1,"HOME_1":2,"SONGS_CHOOSE":3,"SONGS_CHOOSE_2":4,"START":5,"ITEM":6,"RUNNING":7,"GAME_OVER":8}
    states=STATES["HOME_0"]






#创建判子类
class DMcomponent():
    def __init__(self,number,iflighted):
        #基础数值
        self.number=number
        self.iflighted=iflighted
        self.if_lighted=False
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
            if self.if_lighted:
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
                DM.iflighted=False
        if enemy.delete:
            GameVar.enemies.remove(enemy)

          

def song_init():
    GameVar.itemChoose.this_item = -1
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

def item_init(item_name):
    GameVar.hero.defeat = 0
    if GameVar.item_use == "null":
        return
    if item_name=="star_light":
        global star_light
        from script.star_light import Star_light
        star_light = Star_light(GameVar.hero,item_effect_sprite,canvas)
        star_light.buff()
    GameVar.states = GameVar.STATES["ITEM"]

def item_main(item_name):
    if GameVar.item_use == "null":
        return
    if item_name == "star_light":
        star_light.skill_main()

def control():
    if GameVar.states==GameVar.STATES["HOME_0"]:
        GameVar.bg.draw(bgBlack)
        writeText("按下任意键开始游戏",(517,660),(255,255,255),Font.text)
    elif GameVar.states==GameVar.STATES["HOME_1"]:
        GameVar.bg.draw(bgBlack)
        pygame.mixer.init()
    elif GameVar.states==GameVar.STATES["SONGS_CHOOSE"]:
        GameVar.bg.draw(bgBlack)
        GameVar.itemChoose.init()
        GameVar.songChoose.main()
    elif GameVar.states==GameVar.STATES["SONGS_CHOOSE_2"]:
        canvas.blit(bgBlack,(0,0))
        GameVar.songChoose.set(GameVar.songChoose.dire)
        GameVar.songChoose.cphy1=0
        GameVar.songChoose.start=False
        GameVar.songChoose.draw()
        GameVar.itemChoose.main()
        
    elif GameVar.states==GameVar.STATES["START"]:
        commentInit()
        GameVar.gameStart=time.clock()
        with open("songs.txt") as file:
            for line in file:
                if eval(line.rstrip())[0]==GameVar.song_names[GameVar.songChoose.number1]:
                    GameVar.thisSong=eval(line.rstrip())

        if not GameVar.item_use == "null":
            item_init(GameVar.item_use.english_name)
            GameVar.item_effect_y = 360-50
        else:
            song_init()
            GameVar.states = GameVar.STATES["RUNNING"]
    elif GameVar.states == GameVar.STATES["ITEM"]:
        GameVar.bg.draw(bgBlack)
        GameVar.item_use.draw(640-50,GameVar.item_effect_y)
        GameVar.item_effect_y += 345 * last_fps_time / 640+50
        if GameVar.item_effect_y >= 1280:
            time.sleep(1.0)
            song_init()
            GameVar.states = GameVar.STATES ["RUNNING"]
    elif GameVar.states==GameVar.STATES["RUNNING"]:
        GameVar.bg.draw(bgBlack)

        commentEnter(GameVar.thisSong)
        commentDraw()
        commentStep()
        commentDelete()
        if not GameVar.item_use == "null":
            item_main(GameVar.item_use.english_name)
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
    pygame.display.set_caption("八方"+" fps:"+str(GameVar.fpsClock.get_fps()))

    last_fps_time = GameVar.fpsClock.tick(GameVar.fps)

    control()

    writeText("fps:" + str(int(GameVar.fpsClock.get_fps())), (0, 620), (25, 25, 255), Font.text)

    pygame.display.update()
    
    handleEvent()

