'''
Created on 2020-3-24

@author: Time_emit
'''
import pygame,random,time,sys,os
import tkinter as tk
from pygame.locals import *
try:
    from script.summon_treasure import *
    from script.items import *
    from script.lobby import *
    from script.Hall import *
    from script.Error import *
    from script.Setting import *
except:
    showError("加载脚本文件时出现错误,请检查脚本文件")
    pygame.quit()
    sys.exit()

#初始化
pygame.init ()

WIDTH = 1280
HEIGHT = 720
WIDTH_2 = WIDTH/2
HEIGHT_2 = HEIGHT/2
# os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0,0)
canvas = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE|HWSURFACE)

canvas.fill((255,255,255))
BGblack = canvas.get_rect()
#设置标题
pygame.display.set_caption("八方")
#加载英雄图片
main_cover=pygame.image.load("images/mainC/main_cover.png")
yellow_ring = pygame.image.load("images/DMcs/yellowCM.png")
orange_ring = pygame.image.load("images/DMcs/orangeCM.png")
#加载敌人图片
yellow=pygame.image.load("images/yellow.png")
orange = pygame.image.load("images/orange.png")
#加载判子图
yellowDM=pygame.image.load("images/DMcs/yellowCM.png")
#加载背景图片
#bgBlack=pygame.image.load("images/bgBlack.png")
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
coin = pygame.image.load("images/end/coin.png")
#加载道具选取图片素材
item_choose=pygame.image.load("images/item_choose/choose_space.png")
choose=pygame.image.load("images/item_choose/choose.png")
all_item=pygame.image.load("images/item_choose/all_item.png")
#加载道具图片素材
# star_light=pygame.image.load("images/items/ehi1st/star_light.png")
#加载道具特效精灵图
item_effect_sprite=pygame.image.load("images/items/ehi1st/item_effect_sprite.png")

hall_canvas = pygame.image.load("images/lobby/images/hall_canvas.png")
hall_canvas_512 = pygame.transform.scale(hall_canvas,(512,512))
#设置变量基础数值
enemyAttack=5
#主界面默认背景音乐
pygame.mixer.music.load("songs/main_page/E_nightSong.mp3")
pygame.mixer.music.set_volume(0.2)




#创建handleEvent方法
def handleEvent():
    global canvas,WIDTH,HEIGHT,WIDTH_2,HEIGHT_2,BGblack,E_EVENTS,E_MOUSE_POS,E_KEY_PRESSED
    #基础常量
    E_EVENTS = pygame.event.get()
    E_MOUSE_POS = pygame.mouse.get_pos()
    E_KEY_PRESSED = pygame.key.get_pressed()
    SETTING = GameVar.setting
    THIS_SET = SETTING.settings[SETTING.setting_index]
    #设置键位
    KEYS = SettingVar.keys
    for event in E_EVENTS:
        #快捷键
        if not THIS_SET.select:
            if event.type == QUIT or event.type == KEYDOWN and event.key == KEYS["game_exit"]:
                save()
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == KEYS["switch_message"]:
                if GameVar.if_message:
                    GameVar.if_message = False
                else:
                    GameVar.if_message = True
        if event.type == VIDEORESIZE:
            WIDTH = event.size[0]
            HEIGHT = event.size[1]
            WIDTH_2 = WIDTH / 2
            HEIGHT_2 = HEIGHT / 2

            GameVar.itemChoose.item_choose_x = (WIDTH - 1280)/2
            GameVar.itemChoose.compensatory = (WIDTH_2-640, HEIGHT_2-360)
            GameVar.item_choose_highlight.compensatory = GameVar.itemChoose.compensatory

            GameVar.hero.x = 615 + WIDTH_2 - 640
            GameVar.hero.y = 335 + HEIGHT_2 - 360
            GameVar.hero.main_rect.topleft = (GameVar.hero.x, GameVar.hero.y)
            GameVar.hero.rect.topleft = (GameVar.hero.x, GameVar.hero.y + GameVar.hero.height)

            if not len(GameVar.DMcomp) == 0:
                for component in GameVar.DMcomp:
                    component.set()

            GameVar.setting.change_scale((WIDTH, HEIGHT))

            os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 30)
            canvas = pygame.display.set_mode((WIDTH, HEIGHT),RESIZABLE|HWSURFACE)
            BGblack = canvas.get_rect()
        elif GameVar.states==GameVar.STATES["HOME_0"]:
            if event.type==KEYDOWN:
                GameVar.states=GameVar.STATES["LOBBY"]
        elif GameVar.states == GameVar.STATES["HOME_1"]:

            if event.type == KEYDOWN and event.key == 13:
                GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
            if event.type == MOUSEMOTION:
                GameVar.hero.x = event.pos[0]
                GameVar.hero.y = event.pos[1]
                GameVar.hero.width = 1
                GameVar.hero.height = 1
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if GameVar.lobby.objects[0].is_lighted == True:
                    GameVar.states = GameVar.STATES["BOX_GET"]
                elif GameVar.lobby.objects[3].is_lighted == True:
                    GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
        elif GameVar.states == GameVar.STATES["LOBBY"]:
            for item in GameVar.lobbyObjects:
                if E_KEY_PRESSED[KEYS["lobby_right"]]:
                    if item.item:
                        item.step(1,last_fps_time)
                elif E_KEY_PRESSED[KEYS["lobby_left"]]:
                    if item.item:
                        item.step(-1,last_fps_time)
                if event.type == KEYDOWN and event.key == 13:
                    GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    GameVar.states = GameVar.STATES["SETTING"]

                if item.item and item.checkRange((E_MOUSE_POS[0] - (WIDTH - 62 * 8) / 2), (E_MOUSE_POS[1] - (HEIGHT - 62 * 8) / 2), 1, 1):
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if item.name == "musicer":
                            GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
                        elif item.name == "box":
                            GameVar.states = GameVar.STATES["BOX_GET"]
                    item.lighted = True
                else:
                    item.lighted = False
        elif GameVar.states == GameVar.STATES["SETTING"]:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                THIS_SET.select = False
                GameVar.states = GameVar.STATES["LOBBY"]
            if not THIS_SET.select:
                if event.type == KEYDOWN and event.key == K_UP:
                    SETTING.setting_index_switch(-1)
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    SETTING.setting_index_switch(1)
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and THIS_SET.checkRange(event.pos[0], event.pos[1], 1, 1):
                    THIS_SET.select = True
            else:
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and THIS_SET.checkRange(event.pos[0], event.pos[1], 1, 1):
                    THIS_SET.select = False
                elif event.type == KEYDOWN:
                    THIS_SET.input(event.key)
        elif GameVar.states==GameVar.STATES["SONGS_CHOOSE"]:
            #print("SONGS_CHOOSE")
            if event.type==KEYDOWN and event.key == KEYS["songc_up"]:
                GameVar.songChoose.cphy1 = (HEIGHT - 720)/2
                GameVar.songChoose.dire = True
                GameVar.songChoose.set(GameVar.songChoose.dire)
                GameVar.songChoose.number2 = GameVar.songChoose.number1 - 1
                GameVar.songChoose.check()
                GameVar.songChoose.start = True
                GameVar.songChoose.info_pass = False
                GameVar.songChoose.switch_info()
            elif event.type==KEYDOWN and event.key == KEYS["songc_down"]:
                GameVar.songChoose.cphy1 = (HEIGHT - 720)/2
                GameVar.songChoose.dire = False
                GameVar.songChoose.set(GameVar.songChoose.dire)
                GameVar.songChoose.number2 = GameVar.songChoose.number1 + 1
                GameVar.songChoose.check()
                GameVar.songChoose.start = True
                GameVar.songChoose.info_pass = False
                GameVar.songChoose.switch_info()
            elif event.type==KEYDOWN and event.key==13:
                GameVar.states=GameVar.STATES["SONGS_CHOOSE_2"]
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                GameVar.states = GameVar.STATES["LOBBY"]
        elif GameVar.states==GameVar.STATES["SONGS_CHOOSE_2"]:

            if GameVar.itemChoose.state==0:
                if event.type==KEYDOWN and event.key==13:
                    GameVar.states=GameVar.STATES["START"]
                elif event.type==KEYDOWN and event.key==K_ESCAPE:
                    GameVar.states=GameVar.STATES["SONGS_CHOOSE"]
                elif event.type == KEYDOWN and event.key == KEYS["itemc_develop"]:
                    GameVar.itemChoose.state_change(True)
            elif GameVar.itemChoose.state==1:
                if event.type == KEYDOWN and event.key == KEYS["itemc_back"]:
                    GameVar.itemChoose.state_change(False)
                buttons = {KEYS["itemc_up"]:"up",KEYS["itemc_right"]:"right",KEYS["itemc_down"]:"down",KEYS["itemc_left"]:"left"}
                for button in buttons:
                    if event.type == KEYUP and event.key == button:
                        GameVar.item_choose_highlight.move(buttons[button])
                if event.type == KEYUP and event.key == 13:
                    if GameVar.item_choose_highlight.this_item > len(items) - 1:
                        GameVar.itemChoose.item_ready = -1
                        GameVar.item_use = "null"
                    else:
                        GameVar.itemChoose.item_ready = GameVar.item_choose_highlight.this_item
                        GameVar.item_use = items[GameVar.itemChoose.item_ready]
        elif GameVar.states==GameVar.STATES["RUNNING"]:
            if not event.type == KEYDOWN and not event.type == KEYUP:
                return
            buttons = {KEYS["yellow_up"]: 0,KEYS["yellow_right"]: 1, KEYS["yellow_down"]: 2, KEYS["yellow_left"]: 3}
            for button in buttons:
                if event.type == KEYDOWN and event.key == button:
                    GameVar.DMcomp[buttons[button]].iflighted = True
                    GameVar.DMcomp[buttons[button]].if_lighted = True
                if event.type == KEYUP and event.key == button:
                    GameVar.DMcomp[buttons[button]].iflighted = False
                    GameVar.DMcomp[buttons[button]].if_lighted = False
            if event.type == KEYDOWN and event.key == 13:
                GameVar.hero.is_button_press = True
            else:
                GameVar.hero.is_button_press = False
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

class Font():
    song_name = textInit(80,"ttfs/noto/NotoSansHans-Light.otf")
    text = textInit(30,"ttfs/noto/NotoSansHans-Light.otf")
    little_text = textInit(20,"ttfs/noto/NotoSansHans-Light.otf")
    console = textInit(15,"ttfs/noto/NotoSansHans-Light.otf")
    text_bold = textInit(30,"ttfs/noto/NotoSansHans-Bold.otf")
    text_regular = textInit(30, "ttfs/noto/NotoSansHans-Regular.otf")
    score = textInit(40,"ttfs/noto/NotoSansHans-Light.otf")

def writeText(text, position, color=(255,255,255), alpha=255, font=Font.text):
    text = font.render(text, True, color)
    if not alpha == 255:
        text.set_alpha(alpha)
    canvas.blit(text, position)


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

class EHRTObject():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class AnimateObject(EHRTObject):
    def __init__(self,x,y,width,height):
        EHRTObject.__init__(self,x,y,width,height)
        self.state = 0
        self.imgs = []
    def appendImg(self,img,position):
        img_list = [img,position]
        self.imgs.append(img_list)
    def draw(self,num="all"):
        if num == "all":
            for img in self.imgs:
                canvas.blit(img[0],img[1])
        else:
            pass
            # canvas.blit(self.imgs[num][0],self.imgs[num][1])


class GameObject(EHRTObject):
    def __init__(self,life,defeat,x,y,width,height,img):
        EHRTObject.__init__(self,x,y,width,height)
        self.life = life
        self.defeat = defeat
        self.img = img
    def draw(self):
        canvas.blit(self.img,(self.x,self.y))
    def hit(self, component):
        c = component
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height

#创建提示类
class Message(EHRTObject):
    def __init__(self,x,y,width,height,_from_,message):
        EHRTObject.__init__(self,x,y,width,height)
        self._from_ = _from_
        self.from_display = "<" + self._from_ + ">"
        self.message = message
        self.alpha = 255
        self.can_delete = False
        self.summon_time = time.time()
        self.speed = len(GameVar.messages) + 1
    def set_y(self):
        index = GameVar.messages.index(self)
    def draw(self):
        writeText(self.from_display + self.message,(self.x,self.y),(255,255,255),self.alpha,Font.console)
    def check_time(self):
        if not ifDoAction(self.summon_time,1):
            return
        self.can_delete = True
    def delete(self):
        #消失特效
        if self.can_delete:
            # self.y -= len(GameVar.messages)
            self.y -= 2
            if self.y <= -15:
                GameVar.messages.remove(self)

#创建Hero类
class Hero(GameObject):
    def __init__(self,life,defence):
        GameObject.__init__(self,life,defence,WIDTH_2 - 25,HEIGHT_2 -25,50,50,"null")
        self.score=0
        self.Cy=self.y
        self.rect=Rect(self.x, self.y + self.height, self.width, self.height)
        self.rect.topleft=(self.x,self.y+self.height)
        self.is_button_press = False
        self.pictures = {"yellow":yellow_ring, "orange":orange_ring}
        self.colors = {"yellow":(204,204,0), "orange":(222,129,0)}
        self.main_rect = Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        # canvas.blit(self.CImg,(WIDTH/2 - 25,self.Cy))
        # pygame.draw.rect(canvas,(0,0,0),self.rect)
        # canvas.blit(self.mainImg, (self.x, self.y))
        pygame.draw.rect(canvas, self.colors[GameVar.gamemode], self.main_rect)
        canvas.blit(main_cover, (self.x, self.y))
        canvas.blit(self.pictures[GameVar.gamemode], (self.x, self.y))
        pygame.draw.rect(canvas, (0, 0, 0), self.rect)
    def lifeErase(self):
        hurt = GameVar.enemy_damage - self.defeat
        if hurt <=0:
            hurt = 0.1
        self.life -= hurt
    def Cstep(self):
        if self.Cy<self.y+self.height:
            self.Cy += 60 * last_fps_time / 1000
            self.main_rect.top = self.Cy
            return False
        else:
            self.Cy=self.y+self.height
            self.main_rect.top = self.Cy
            return True

    def bang(self):
        self.lifeErase()



#创建背景类
class BG():
    def __init__(self):
        self.number=0
        self.x=0
        self.y=0
        self.if_night = True
        self.rect = Rect(0,0,1280,720)
    def draw(self):
        if self.if_night:
            if GameVar.states==GameVar.STATES["HOME_1"]:
                pygame.draw.rect(canvas,(42,42,63),BGblack)
            else:
                pygame.draw.rect(canvas, (0,0,0), BGblack)



class End():
    def __init__(self):
        self.result=False
        self.score_img=score
        self.coin_img = coin
        self.dieImg=die
        self.speed=20
        self.coin_plus = 0
    def draw(self):
        canvas.blit(self.dieImg,(0,0))
        canvas.blit(self.result_img,(self.result_x,self.result_y))
        canvas.blit(self.score_img,(self.score_x,self.score_y))
        canvas.blit(self.coin_img, (self.score_x, self.score_y))
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
    def __init__(self,cph):
        self.dire=True
        self.start=False
        self.width = 250
        self.height = 250
        self.x1 = WIDTH/2 - self.width/2
        self.x2 = self.x1
        self.y1 = HEIGHT/2 - self.height/2
        self.y2 = HEIGHT + HEIGHT/2 - self.height/2
        self.imgs=[]
        self.imgs_road = []
        self.cph=cph
        self.number1=0
        self.number2=1
        self.cphx = (WIDTH - 960)/2
        self.cphy1=(HEIGHT - 720)/2
        self.cphy2=HEIGHT + (HEIGHT - 720)/2
        self.song_played=False
        self.info_time = 0.5
        self.info_lastTime = 0
        self.info_pass = False
        self.info_x = 300
        self.info_y = 95
        i = 0
        with open("data/song_name.txt", encoding="utf-8") as file:
            for line in file:
                if i == 0:
                    self.info_name = eval(line.rstrip())
                elif i == 1:
                    self.info_little_name = eval(line.rstrip())
                elif i == 2:
                    self.info_time = eval(line.rstrip())
                i += 1
        self.info_thisName = self.info_name[0]
        self.info_thisLittleName = self.info_little_name[0]
        self.info_thisTime = self.info_time[0]
        # print(type(self.info_thisTime))
    def draw(self):

        # print(self.info_thisName)
        self.cphx = (WIDTH - 960) / 2
        self.x1 = WIDTH/2 - self.width/2
        self.x2 = self.x1
        # self.y1 = HEIGHT/2 - self.height/2
        # self.y2 = HEIGHT + HEIGHT/2 - self.height/2
        canvas.blit(self.imgs[self.number1], (self.x1-1, self.y1-1))
        canvas.blit(self.cph, (self.cphx,self.cphy1))
        canvas.blit(self.imgs[self.number2], (self.x2-1, self.y2-1))
        canvas.blit(self.cph, (self.cphx,self.cphy2))
    def set(self,dire):
        self.dire=dire
        if self.start:
            self.number(self.dire)
        if self.dire==True:#dire为True向下,反之向上
            self.y1=HEIGHT_2-self.height/2
            self.y2=-HEIGHT_2-self.height/2
            self.cphy1=(HEIGHT - 720)/2
            self.cphy2=-HEIGHT + (HEIGHT - 720)/2
        else:
            self.y1=HEIGHT_2-self.height/2
            self.y2=HEIGHT + HEIGHT_2 -self.height/2
            self.cphy1=(HEIGHT - 720)/2
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
    def set_imgs(self):
        with open("data/songs.txt", encoding ="gbk") as file:
            for line in file:
                self.imgs_road = eval(line.rstrip())
                break
        basic_road = "images/start/songs/"
        for img_road in self.imgs_road:
            self.imgs.append(pygame.image.load(basic_road + img_road))
    def info(self):
        # if self.start:
        #     return
        # if not (self.info_pass or ifDoAction(self.info_lastTime,self.info_time)):
        #     return
        # self.info_lastTime = time.time()
        # self.info_pass = True
        self.draw_info()
    def switch_info(self):
        self.info_thisName = self.info_name[self.number2]
        self.info_thisLittleName = self.info_little_name[self.number2]
        self.info_thisTime = self.info_time[self.number2]
    def draw_info(self):
        writeText(self.info_thisName,(self.info_x, self.info_y),(255,255,255),255,Font.song_name)
        writeText(self.info_thisLittleName, (self.info_x, self.info_y + 100),(255,255,255),255,Font.text)
        writeText("时长：" + self.info_thisTime, (self.info_x, self.info_y + 150),(255,255,255),255,Font.little_text)
    def main(self):
        if self.start==False:
            self.cphy1=(HEIGHT - 720)/2
            self.set(self.dire)
            self.info()
        self.draw()
        self.anime()

#创建Enemy类
class Enemy(GameObject):
    def __init__(self,number):
        GameObject.__init__(self,1,0,0,0,50,50,yellow)
        self.number=number
        self.attack=enemyAttack
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
            self.y-=100 *last_fps_time /385
        else:
            self.x+=100 *last_fps_time /385
    def bang(self,if_score):
        self.life -= 1
        if self.life <= 0:
            self.delete = True
        if if_score:
            GameVar.hero.score+=5



class Item_choose():
    def __init__(self):
        self.state = 0
        self.this_item = -1
        self.item_ready = -1
        self.item_choose = item_choose
        self.choose = choose
        self.all_item = all_item
        self.item_choose_x = 0 + (WIDTH - 1280)/2
        self.item_choose_y=0
        self.index=0
        self.line=0
        self.start="Start"
        self.last_time=0
        self.intertal=0.5
        self.compensatory = (0,0)
    def init(self):
        self.state=0
        self.item_choose_y=0 + HEIGHT_2 - 360
    def main(self):
        if self.state == 0:
            if self.item_choose_y>0 + HEIGHT_2 - 360:
                self.animate_0()
                if self.item_choose_y < 0 + HEIGHT_2 - 360:
                    self.item_choose_y = 0 + HEIGHT_2 - 360
            canvas.blit(die, (0, 0))
            canvas.blit(self.item_choose, (self.item_choose_x,self.item_choose_y))
            if not self.item_ready == -1:
                canvas.blit(items[self.item_ready].img,(591 + self.compensatory[0],self.item_choose_y+311))
            self.write_start()
            if self.this_item == -1:
                return
            else:
                canvas.blit(items[self.this_item], (591 + self.compensatory[0], 311 + self.compensatory[1]))
        elif self.state==1:
            if self.item_choose_y<134:
                GameVar.songChoose.draw()
                #canvas.blit(die, (0, 0))
                self.animate_1()
                canvas.blit(self.item_choose,(self.item_choose_x, self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(items[self.item_ready].img, (591 + self.compensatory[0], self.item_choose_y + 311))
                return
            else:
                GameVar.songChoose.draw()
                #canvas.blit(die, (0, 0))
                canvas.blit(self.all_item,(0 + self.compensatory[0],0 + self.compensatory[1]))
                canvas.blit(self.item_choose,(self.item_choose_x,self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(items[self.item_ready].img, (591 + self.compensatory[0], self.item_choose_y + 311))
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
        for item in items:
            canvas.blit(item.img,(335 + self.compensatory[0] + self.index*(100+3),76 + self.compensatory[1] + self.line*(100+3)))
            self.index+=1
            if self.index>5:
                self.index=0
                self.line+=1
            if self.line>2:
                return True
    def write_start(self):
        writeText(self.start, (WIDTH-226, HEIGHT-45))
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
        x = 332 + self.compensatory[0] + (self.this_item % 6) * 103 -1
        y = 73 + self.compensatory[1] + (self.this_item - self.this_item % 6)/6 * 103 -1
        canvas.blit(self.img,(x,y))

#[quality,item_id]
boxs = [[[0,0],[1,1],[2,2],[2,3],[3,4]],["2st"]]
class Box():
    def __init__(self,hero,canvas):
        self.hero = hero
        self.canvas = canvas
        self.qua_list = [0,1,2,3]
        self.qua_prob_list = []
        self.items = []
        self.this_item = 0
    def box_init(self,num):
        self.this_box = boxs[num]
        #print(self.this_box)
        #self.this_box.pop(0)
        self.index_prob = random.randint(0,99)
        self.this_qua = self.qua_prob_list[self.index_prob]
        # print(self.this_qua)
        self.items = []
        for item in self.this_box:
            if item[0] == self.this_qua:
                self.items.append(item[1])
        self.this_item = random.randint(0,len(self.items) - 1)
    def set_prob(self,gold,purple,blue,green):
        self.qua_prob_list = []
        if not ((gold + purple + blue + green) == 100):
            return
            # print("return")
        prob_list = [gold,purple,blue,green]
        # for porb in prob_list:
        #     porb = porb * 10
        prob_i = 0
        for qua in self.qua_list:
            i = 0
            while i < prob_list[prob_i]:
                self.qua_prob_list.append(qua)
                i += 1
            prob_i += 1
        # print(self.qua_prob_list)
    def summon(self):
        items = Items(self.hero,self.canvas)
        self.real_items = []
        self.real_items.append(items.list[self.items[self.this_item]][0])
        return self.real_items

class Home(AnimateObject):
    def __init__(self):
        AnimateObject.__init__(self,0,0,1280,720)
        self.list = []
    def box(self,box,times):
        GameVar.box.set_prob(1,4,40,55)
        i = 0
        while i < times:
            GameVar.box.box_init(0)
            i += 1
            self.list = GameVar.box.summon()
            self.print()
    def print(self):
        for item in self.list:
            # print(item.name)
            message_summon("System","您抽到了 [" + item.quality + "]" + item.name)



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
    #敌人的伤害值
    enemy_damage = 5
    enemy_score = 5
    score_to_coin = 30  #分数/金币的比值
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
    songChoose = SongChoose(cph)
    #结束类
    end=End()
    #结束时的time.time()
    this_time=0
    #结束是否跳过
    skip=0

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
    fps=60
    #宝箱类
    box = Box(hero,canvas)
    #玩家C值
    player_c = 0
    #玩家金币数
    coin = 0
    #定时保存的时间间隔(sec)
    lastTime_of_save = 0
    interval_of_save = 300
    #主界面背景音乐
    main_page_bgm = Bgm("songs/main_page/E_nightSong.mp3",267)
    #消息列表
    messages = []
    #是否显示控制台
    if_message = True
    #当前游戏的模式
    gamemode = "yellow"
    #大厅
    lirb = "images/lobby/images/" #lobby_images_road_basic
    # lobby = Lobby([Lobby_object("宝箱",418,305,405,295,327,327,0,[pygame.image.load(lirb + "box.png")],pygame.image.load(lirb + "box_highlight.png")),Lobby_object("便利柜电源",43,485,None,None,55,57,0,[pygame.image.load(lirb + "bianli_light.png")],None),Lobby_object("便利柜",99,49,90,37,407,583,0,[pygame.image.load(lirb + "bianligui.png")],pygame.image.load(lirb + "bianligui_highlight.png")),Lobby_object("留声机",890,81,890,81,278,511,0,[pygame.image.load(lirb + "musicer.png")],pygame.image.load(lirb + "musicer_highlight.png"))])
    lobbyObjects = [LobbyObject(0,16,62,46,"land"), LobbyItem(0,8,22,34,"bianligui"), LobbyItem(8,6,18,18,"box"), LobbyItem(20,4,14,27,"musicer"),  LobbyObject(0,0,62,62,"fog"), LobbyObject(32,22,30,38,"cover")]
    #屏幕的x
    screen_x = 0

    home = Home()

    #设置界面
    setting = Setting((WIDTH, HEIGHT))

    #使用字典存储游戏进程
    STATES={"HOME_0":0,"HOME_1":1,"SONGS_CHOOSE":2,"SONGS_CHOOSE_2":3,"START":4,"ITEM":5,"RUNNING":6,"GAME_OVER":7,"BOX":8,"BOX_GET":9,"LOBBY":10,"SETTING":11}
    States = []
    for state in STATES:
        States.append(state)
    states=STATES["HOME_0"]
    last_state = states

#物品的图片列表
ITEMS = Items(GameVar,canvas)
items=[ITEMS.get_item(0),ITEMS.get_item(1),ITEMS.get_item(2)]

#创建判子类
class DMcomponent():
    def __init__(self,number,iflighted):
        #基础数值
        self.number=number
        self.iflighted=iflighted
        self.if_lighted=False
        self.width=50
        self.height=50
        self.img=yellowDM
        self.imgLighted=yellow
        self.color=self.img
        self.set()
    def set(self):
        if GameVar.gamemode == "yellow":
            if self.number == 0:
                self.x = GameVar.hero.x
                self.y = GameVar.hero.y - 85
            elif self.number == 1:
                self.x = GameVar.hero.x + 85
                self.y = GameVar.hero.y
            elif self.number == 2:
                self.x = GameVar.hero.x
                self.y = GameVar.hero.y + 85
            elif self.number == 3:
                self.x = GameVar.hero.x - 85
                self.y = GameVar.hero.y
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
    GameVar.hero.Cy = HEIGHT_2 - 25
    GameVar.indexOfSong = 1

    GameVar.hero.x = WIDTH_2 - 25
    GameVar.hero.y = HEIGHT_2 - 25
    GameVar.hero.main_rect.top = HEIGHT_2 - 25
    GameVar.hero.width = 50
    GameVar.hero.height = 50
    GameVar.hero.life = 50.0
    GameVar.ifsongplaying = False
    GameVar.hero.score = 0
    GameVar.enemy_damage = 5
    GameVar.score_to_coin = 30

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
    if item_name=="Star_light":
        ITEMS.get_item(0).buff()
    if item_name == "Diamond":
        # ITEMS.get_item(1).buff()
        GameVar.enemy_damage = GameVar.enemy_damage * 2
        GameVar.score_to_coin = GameVar.score_to_coin * 0.8
    if item_name == "Apple":
        ITEMS.get_item(2).buff()
        ITEMS.get_item(2).skill_over = time.time()
    GameVar.states = GameVar.STATES["ITEM"]

def item_main(item_name):
    if GameVar.item_use == "null":
        return
    if item_name == "Star_light":
        ITEMS.get_item(0).skill_main()
    elif item_name == "Apple":
        ITEMS.get_item(2).skill_main()

def end_score():
    score = GameVar.hero.score
    song_score = len(GameVar.thisSong)/2 * GameVar.enemy_score
    # if score < song_score/2:
    #     return "NOT_SCORE"
    # else:
    #     coin = score/GameVar.score_to_coin
    #     return coin
    coin = round(score / GameVar.score_to_coin)
    return coin

def end_animate():
    if GameVar.hero.life <= 0:
        if not GameVar.hero.Cstep() and GameVar.skip == -1:
            return
        elif GameVar.skip == -1:
            GameVar.skip = 0
    else:
        if GameVar.skip == -1:
            GameVar.skip = 0
    if GameVar.skip == 0:
        if GameVar.end.result:
            GameVar.hero.Cy = 385
        GameVar.end.draw()
        GameVar.end.animate()
        GameVar.end.animateOver()
        if ifDoAction(GameVar.this_time + 1, 2):
            writeText(str(GameVar.hero.score), (170, 239), (255, 228, 0), 255, Font.score)
            GameVar.skip = 1
    elif GameVar.skip == 1:
        if GameVar.end.result:
            GameVar.hero.Cy = 385
        GameVar.end.result_x = 0
        GameVar.end.score_x = 0
        GameVar.end.draw()
        writeText(str(GameVar.hero.score), (170, 239), (255, 228, 0), 255, Font.score)
        writeText(str(GameVar.end.coin_plus), (145, 302), (255, 228, 0), 255, Font.score)
    elif GameVar.skip == 2:
        GameVar.end.draw()
        GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
        pygame.mixer.quit()

def save():
    data = {'coin':GameVar.coin}
    data = str(data)
    with open("data/player.txt", "w") as file:
        file.write(data)
    i = 0
    with open("data/settings.txt", "r", encoding="UTF-8") as file:
        lines = file.readlines()
    with open("data/settings.txt", "w", encoding="UTF-8") as file:
        for line in lines:
            if i == 0:
                line = str(SettingVar.keys) + "\n"
                file.write(line)
            else:
                file.write(line)
            i += 1

def load():
    with open('data/player.txt') as file:
        for line in file:
            data = line.rstrip()
            break
    data = eval(data)
    GameVar.coin = data['coin']


def lobby_main():
    for obj in GameVar.lobby.objects:
        if obj.checkHit(GameVar.hero):
            obj.is_lighted = True
        else:
            obj.is_lighted = False
        if obj.check_page(WIDTH):
            obj.draw(WIDTH,GameVar.screen_x,canvas)

def hall_main():
    canvas.blit(LobbyVar.canvas, (WIDTH_2 - 256, HEIGHT_2 - 256))
    LobbyVar.canvas.blit(hall_canvas_512, (0,0))
    # LobbyVar.canvas.blit(LobbyVar.canvas,(0,0))
    for item in GameVar.lobbyObjects:
        item.draw(LobbyVar.canvas)

def setting_main():
    GameVar.setting.main(canvas)

def message_summon(come,message):
    GameVar.messages.append(Message(0,0,None,None,come,message))

def message_state_change():
    if not GameVar.last_state == GameVar.states:
        if GameVar.states == GameVar.STATES["LOBBY"] or GameVar.states == GameVar.STATES["RUNNING"]:
            pygame.key.set_repeat(1, 1)
        else:
            pygame.key.set_repeat()
        message_summon("System","StateChange( " + GameVar.States[GameVar.last_state] + " to " + GameVar.States[GameVar.states] + " )")
        GameVar.last_state = GameVar.states
def message_check_y():
    i = 0
    for message in GameVar.messages:
        if message.can_delete == False:
            message.y = i * 15
        i += 1
def message_draw():
    for message in GameVar.messages:
        message.draw()

def message_delete():
    for message in GameVar.messages:
        message.check_time()
        message.delete()

def message_main():
    if not GameVar.if_message:
        GameVar.messages = []
        return
    message_state_change()
    if GameVar.messages == []:
        return
    message_check_y()
    message_draw()
    message_delete()

def bgm_play():
    GameVar.main_page_bgm.play()


def control():
    global canvas
    #循环前执行
    #定时保存

    if ifDoAction(GameVar.lastTime_of_save, GameVar.interval_of_save) and not GameVar.states == GameVar.STATES["RUNNING"]:
        GameVar.lastTime_of_save = time.time()
        # try:
        #     save()
        # except:
        #     showError("写入data.txt时出现错误,有可能文件被锁定或删除")
        #     pygame.quit()
        #     sys.exit()
        save()
        message_summon("System","已保存")
    if GameVar.states==GameVar.STATES["HOME_0"]:
        pygame.mixer.init()
        bgm_play()
        GameVar.bg.draw()
        writeText("按下任意键开始游戏",(WIDTH_2 - 135,HEIGHT - 60))
    elif GameVar.states==GameVar.STATES["HOME_1"]:
        GameVar.bg.draw()
        bgm_play()
        lobby_main()
        # GameVar.hero.draw()
    elif GameVar.states == GameVar.STATES["LOBBY"]:
        # print(LobbyVar.times)
        GameVar.bg.draw()
        hall_main()
    elif GameVar.states == GameVar.STATES["SETTING"]:
        GameVar.bg.draw()
        setting_main()
    elif GameVar.states==GameVar.STATES["SONGS_CHOOSE"]:
        GameVar.bg.draw()
        # lobby_main()
        # canvas.blit(die,(0,0))
        bgm_play()
        GameVar.itemChoose.init()
        GameVar.songChoose.main()
    elif GameVar.states==GameVar.STATES["SONGS_CHOOSE_2"]:
        GameVar.bg.draw()
        bgm_play()
        GameVar.songChoose.set(GameVar.songChoose.dire)
        GameVar.songChoose.start=False
        GameVar.songChoose.draw()
        GameVar.itemChoose.main()
    elif GameVar.states == GameVar.STATES["BOX"]:
        GameVar.bg.draw()
        bgm_play()
    elif GameVar.states == GameVar.STATES["BOX_GET"]:
        # GameVar.bg.draw()
        bgm_play()
        GameVar.messages = []
        GameVar.home.box(None,10)
        GameVar.states = GameVar.STATES["LOBBY"]
    elif GameVar.states==GameVar.STATES["START"]:

        with open("data/songs.txt", encoding ="gbk") as file:
            i = 0
            for line in file:
                if i == 1:
                    GameVar.song_names = eval(line.rstrip())
                i += 1

        with open("data/songs.txt", encoding ="gbk") as file:
            i = 0
            for line in file:
                if not (i == 0 or i == 1):
                    if eval(line.rstrip())[0]==GameVar.song_names[GameVar.songChoose.number1]:
                        GameVar.thisSong=eval(line.rstrip())
                i += 1

        song_init()
        commentInit()
        if not GameVar.item_use == "null":
            item_init(GameVar.item_use.name)
            GameVar.item_effect_y = 360-50
        else:
            GameVar.gameStart = time.clock()
            GameVar.states = GameVar.STATES["RUNNING"]
    elif GameVar.states == GameVar.STATES["ITEM"]:
        GameVar.bg.draw()
        bgm_play()
        canvas.blit(GameVar.item_use.img,(640-50,GameVar.item_effect_y))
        GameVar.item_effect_y += 345 * last_fps_time / 640+50
        if GameVar.item_effect_y >= 1280:
            time.sleep(1.0)
            GameVar.gameStart = time.clock()
            GameVar.states = GameVar.STATES ["RUNNING"]
    elif GameVar.states==GameVar.STATES["RUNNING"]:
        GameVar.bg.draw()

        commentEnter(GameVar.thisSong)
        commentDraw()
        commentStep()
        commentDelete()
        if not GameVar.item_use == "null":
            item_main(GameVar.item_use.name)
        writeText("Health:"+str(GameVar.hero.life),(0,0))
        writeText("Score:"+str(GameVar.hero.score),(0,40))
        if GameVar.ifsongplaying==False and time.clock()-GameVar.gameStart>=1.2:
            pygame.mixer.music.play()
            GameVar.ifsongplaying=True
        if GameVar.hero.life<=0 or time.clock()-GameVar.gameStart>GameVar.thisSong[-1]+3:
            GameVar.states = GameVar.STATES["GAME_OVER"]
            GameVar.end.init()
            GameVar.end.coin_plus = end_score()
            # if not GameVar.end.coin_plus == "NOT_SCORE":
            #     GameVar.coin += coin_plus
            GameVar.coin += GameVar.end.coin_plus
            GameVar.this_time=time.time()
        #print(GameVar.lastTime)
    elif GameVar.states==GameVar.STATES["GAME_OVER"]:
        GameVar.bg.draw()
        commentDraw()
        GameVar.main_page_bgm.set()
        end_animate()
    #循环后执行
    message_main()
    writeText("fps:" + str(int(GameVar.fpsClock.get_fps())), (0, 620), (25, 25, 255), 255, Font.text)

GameVar.songChoose.set_imgs()
try:
    load()
except:
    showError("加载player.txt时出现错误,有可能文件被锁定或删除")
    pygame.quit()
    sys.exit()
message_summon("System","GameStart")

try:
    GameVar.setting.load_settings()
except:
    showError("加载settings.txt时出现错误，有可能文件被锁定或删除")
    pygame.quit()
    sys.exit()

while True:

    pygame.display.set_caption("八方"+" fps:"+str(GameVar.fpsClock.get_fps()))

    last_fps_time = GameVar.fpsClock.tick(GameVar.fps)

    control()

    # print(last_fps_time)

    pygame.display.update()

    handleEvent()

