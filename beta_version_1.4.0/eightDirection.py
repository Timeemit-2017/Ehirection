'''
Created on 2020-3-24

@author: Time_emit
'''
import pygame
import random, time, sys, os, math
import tkinter.messagebox
from pygame.locals import *
# try:
#     from script.summon_treasure import *
#     from script.items import *
#     from script.lobby import *
#     from script.Hall import *
#     from script.Error import *
#     from script.Setting import *
#     from script.Animation import *
#     from script.Pool import *
#     from script.Box import *
# except:
#     showError("加载脚本文件时出现错误,请检查脚本文件")
#     pygame.quit()
#     sys.exit()

from script.summon_treasure import *
from script.items import *
from script.Hall import *
from script.Error import *
from script.Setting import *
from script.Animation import *
from script.Pool import *
from script.Box import *
from script.basic import *
from script.PotLight import PotLight
from script.Message import *
from script.SongChoose import *
from script.Bgm import *
from script.Account_Item import *

# 初始化
pygame.init()

def SIZEUpdate(size):
    global SIZE, HEIGHT, WIDTH, HEIGHT_2, WIDTH_2
    SIZE = size
    WIDTH = size[0]
    HEIGHT = size[1]
    WIDTH_2 = WIDTH / 2
    HEIGHT_2 = HEIGHT / 2

def canvasUpdate():
    global SIZE, SCREENTAG, BGblack, canvas
    canvas = pygame.display.set_mode((WIDTH, HEIGHT), SCREENTAG)
    BGblack = canvas.get_rect()

infoObject = pygame.display.Info()

WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
SIZE = (WIDTH, HEIGHT)
SIZE = (1280, 720)
SIZEUpdate(SIZE)
VERSION = "1.4.0.3"

pygame.display.set_icon(pygame.image.load("eightDirection.ico"))
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (20, 20)
SCREENTAG = RESIZABLE
canvasUpdate()
writeText("Loading...", (WIDTH, HEIGHT), canvas, is_right_bottom=True)
pygame.display.flip()
BGblack = canvas.get_rect()
# 设置标题
pygame.display.set_caption("八方 {0} {1}".format(VERSION, SIZE))
# 加载英雄图片
main_cover = pygame.image.load("images/mainC/main_cover.png")
yellow_ring = pygame.image.load("images/DMcs/yellowCM.png")
orange_ring = pygame.image.load("images/DMcs/orangeCM.png")
# 加载敌人图片
yellow = pygame.image.load("images/yellow.png")
orange = pygame.image.load("images/orange.png")
# 加载判子图
yellowDM = pygame.image.load("images/DMcs/yellowCM.png")
# 加载歌曲选单图片
cph = pygame.image.load("images/start/changpianhuan.png")
# 加载歌曲封面
# his_theme=pygame.image.load("images/start/songs/his_theme.jpg")
# tyx=pygame.image.load("images/start/songs/tyx.jpg")
# shib=pygame.image.load("images/start/songs/shib.jpg")
# piano=pygame.image.load("images/start/songs/The_Piano.png")
# 加载死亡图片素材
die = pygame.Surface((WIDTH, HEIGHT), SWSURFACE | RLEACCEL).convert()
die.set_alpha(128)
win = pygame.image.load("images/end/success.png")
lose = pygame.image.load("images/end/failed.png")
score = pygame.image.load("images/end/score.png")
coin = pygame.image.load("images/end/coin.png")
# 加载道具选取图片素材
item_choose = pygame.image.load("images/item_choose/choose_space.png")
choose = pygame.image.load("images/item_choose/choose.png")
all_item = pygame.image.load("images/item_choose/all_item.png")
# 加载道具图片素材
# star_light=pygame.image.load("images/items/ehi1st/star_light.png")
# 加载道具特效精灵图
# item_effect_sprite=pygame.image.load("images/items/ehi1st/item_effect_sprite.png")

hall_canvas = pygame.image.load("images/lobby/images/hall_canvas.png")
hall_canvas_512 = pygame.transform.scale(hall_canvas, (512, 512))
# 设置变量基础数值
enemyAttack = 5
# 主界面默认背景音乐
pygame.mixer.music.load("songs/main_page/E_nightSong.mp3")
pygame.mixer.music.set_volume(0.2)

# 消除note的音效
click = pygame.mixer.Sound("sounds/click.wav")
click.set_volume(0.2)
# 这是轻一点的
click2 = pygame.mixer.Sound("sounds/click2.wav")
click2.set_volume(0.2)

setIndex = 0  # 当前激活的设置按钮在GameVar.setting.settings中的索引

pygame.key.set_repeat()  # 在程序一开始设置不让键盘按键重复加入事件序列（虽然没用但会使我安心）

# 在程序一开始发送一个屏幕更新事件，有可能程序正式开始执行后不会发送（兴许是pygame 2.0的问题）
pygame.event.post(pygame.event.Event(VIDEORESIZE, size=(WIDTH, HEIGHT)))


# 一个没有用到的，未完工的非线性运动函数
def unRope(thisSpeed=0, orginPos=(0, 0), thisPos=(0, 0), ToPos=(0, 0), timeNeed=0):
    Ax = orginPos[0]
    Bx = ToPos[0]
    Ay = orginPos[1]
    By = ToPos[1]
    trangleA = math.fabs(Ax - Bx)
    trangleB = math.fabs(Ay - By)
    magnitude = trangleA * trangleB ** 0.5
    print(magnitude)
    maxSpeed = magnitude / timeNeed * 2


# 处理pygame事件队列的方法
def handleEvent():
    global canvas, die, WIDTH, HEIGHT, WIDTH_2, HEIGHT_2, SIZE, BGblack, E_EVENTS, E_MOUSE_POS, E_KEY_PRESSED, \
        SCREENTAG, setIndex
    # 基础常量
    E_EVENTS = pygame.event.get()
    E_MOUSE_POS = pygame.mouse.get_pos()
    E_KEY_PRESSED = pygame.key.get_pressed()
    SETTING = GameVar.setting
    THIS_SET = SETTING.getSet(SETTING.setting_index)
    # 设置键位
    KEYS = SettingVar.keys
    for event in E_EVENTS:
        # 快捷键
        if not THIS_SET.select:
            if event.type == QUIT or event.type == KEYUP and event.key == KEYS["game_exit"]:
                save()
                pygame.quit()
                sys.exit()
            elif event.type == KEYUP and event.key == KEYS["switch_message"]:
                if GameVar.messageControl.if_message:
                    GameVar.messageControl.if_message = False
                else:
                    GameVar.messageControl.if_message = True
            elif event.type == KEYUP and event.key == KEYS["start_indexDesigner"]:
                window = tk.Tk()
                window.withdraw()
                if tkinter.messagebox.askokcancel(title="询问", message="是否打开谱面编辑器？"):
                    startIndexDesigner()
        if event.type == VIDEORESIZE:
            WIDTH = event.size[0]
            HEIGHT = event.size[1]
            WIDTH_2 = WIDTH / 2
            HEIGHT_2 = HEIGHT / 2
            SIZE = (WIDTH, HEIGHT)

            GameVar.itemChoose.item_choose_x = (WIDTH - 1280) / 2
            GameVar.itemChoose.compensatory = (WIDTH_2 - 640, HEIGHT_2 - 360)
            GameVar.item_choose_highlight.compensatory = GameVar.itemChoose.compensatory

            GameVar.hero.x = 615 + WIDTH_2 - 640
            GameVar.hero.y = 335 + HEIGHT_2 - 360
            GameVar.hero.main_rect.topleft = (GameVar.hero.x, GameVar.hero.y)
            GameVar.hero.rect.topleft = (GameVar.hero.x, GameVar.hero.y + GameVar.hero.height)

            if not len(GameVar.DMcomp) == 0:
                for component in GameVar.DMcomp:
                    component.set()

            GameVar.setting.change_scale((WIDTH, HEIGHT))

            die = pygame.Surface((WIDTH, HEIGHT), SRCALPHA | HWSURFACE).convert()
            die.set_alpha(128)

            if not len(GameVar.DMcomp) == 0:
                for component in GameVar.DMcomp:
                    component.set()

            if not len(GameVar.DMcomp) == 0:
                for component in GameVar.DMcomp:
                    component.set()

            GameVar.setting.change_scale((WIDTH, HEIGHT))

            GameVar.box_animation.change_scale((WIDTH, HEIGHT))
            #GameVar.box_result.box_sprite.set_pos((WIDTH, HEIGHT))
            for button in GameVar.box_animation.buttons:
                button.set_pos((WIDTH, HEIGHT))

            die = pygame.Surface((WIDTH, HEIGHT), SRCALPHA | HWSURFACE).convert()
            die.set_alpha(128)

            # os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 30)
            canvas = pygame.display.set_mode((WIDTH, HEIGHT), SCREENTAG)
            BGblack = canvas.get_rect()
        elif GameVar.states == GameVar.STATES["HOME_0"]:
            if event.type == KEYUP:
                GameVar.states = GameVar.STATES["LOBBY"]
                return
        elif GameVar.states == GameVar.STATES["LOBBY"]:
            left_passer = True
            right_passer = True
            max_land_x = -999999
            min_land_x = 9999999
            for item in GameVar.lobbyObjects:
                if item.item and max_land_x < item.origin_land_x:
                    max_land_x = item.origin_land_x
                if item.item and min_land_x > item.origin_land_x:
                    min_land_x = item.origin_land_x

            max_land_pos = -9999999
            min_land_pos = 9999999
            for item in GameVar.lobbyObjects:
                if item.item and item.land_x < min_land_pos:
                    min_land_pos = item.land_x
                if item.item and item.land_x > max_land_pos:
                    max_land_pos = item.land_x
            left_index = -999999999
            right_index = 999999999
            max_item = None
            min_item = None
            max_item_land_x = -999999999
            min_item_land_x = 999999999
            for item in GameVar.lobbyObjects:
                if item.item and item.land_x > max_item_land_x:
                    max_item = item
                    max_item_land_x = item.land_x
                if item.item and item.land_x < min_item_land_x:
                    min_item = item
                    min_item_land_x = item.land_x

            middle_line = 8
            # print(min_item.land_x, max_item.land_x)
            if min_item.land_x > middle_line - min_item.land_width / 2:
                right_passer = False
            if max_item.land_x < middle_line - max_item.land_width / 2:
                left_passer = False
            if not left_passer and not right_passer:
                left_passer = True
                right_passer = True

            # print(E_KEY_PRESSED[KEYS["lobby_right"]] == 1 or E_KEY_PRESSED[KEYS["lobby_left"]] == 1)
            if event.type == KEYDOWN and (event.key == KEYS["lobby_right"] or event.key == KEYS["lobby_left"]):
                GameVar.lobbyForceControl.lobbyAddForce()
            else:
                GameVar.lobbyForceControl.lobbyFriction()
            # print(str(LobbyVar.moveSpeed))
            for item in GameVar.lobbyObjects:
                if E_KEY_PRESSED[KEYS["lobby_right"]]:
                    if item.item and right_passer:
                        item.step(1, last_fps_time)
                elif E_KEY_PRESSED[KEYS["lobby_left"]]:
                    if item.item and left_passer:
                        item.step(-1, last_fps_time)
                if event.type == KEYUP and event.key == 13:
                    GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
                    return
                if event.type == KEYUP and event.key == K_ESCAPE:
                    GameVar.states = GameVar.STATES["SETTING"]
                    return
                if item.item and item.checkRange((E_MOUSE_POS[0] - (WIDTH - 62 * 8) / 2),
                                                 (E_MOUSE_POS[1] - (HEIGHT - 62 * 8) / 2), 1, 1):
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if item.name == "musicer":
                            GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
                            return
                        elif item.name == "box":
                            GameVar.box_animation.start()
                            GameVar.states = GameVar.STATES["BOX"]
                            return
                    item.lighted = True
                else:
                    item.lighted = False
        elif GameVar.states == GameVar.STATES["BOX"]:
            # GameVar.box_animation.main(canvas, SIZE)
            if event.type == KEYUP and event.key == K_ESCAPE:
                GameVar.states = GameVar.STATES["LOBBY"]
                return
            for button in GameVar.box_animation.buttons:
                if button.checkRange(pygame.mouse.get_pos()):
                    button.animation(True)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        if GameVar.box_animation.get_item(button.text, GameVar):
                            GameVar.box_result.start()
                            GameVar.states = GameVar.STATES["BOX_GET"]
                            return
                else:
                    button.animation(False)
        elif GameVar.states == GameVar.STATES["BOX_GET"]:
            if event.type == KEYUP and event.key == K_ESCAPE and GameVar.box_result.state == 3:
                GameVar.states = GameVar.STATES["BOX"]
                return

            elif event.type == KEYUP and event.key == K_RETURN or event.type == KEYUP and event.key == K_ESCAPE and GameVar.box_result.state != 3:
                GameVar.box_result.skip(GameVar, SIZE)
        elif GameVar.states == GameVar.STATES["SETTING"]:
            if event.type == KEYUP and event.key == K_ESCAPE:
                THIS_SET.select = False
                GameVar.states = GameVar.STATES["LOBBY"]
                return
            elif event.type == KEYUP and event.key == K_b:
                if GameVar.settingsOldOrNew == "Old":
                    GameVar.setting.changeDisplayType("New")
                    GameVar.settingsOldOrNew = "New"
                else:
                    GameVar.setting.changeDisplayType("Old")
                    GameVar.settingsOldOrNew = "Old"
                for i in range(len(SETTING.settings)):
                    for set in SETTING.settings[i]:
                        set.button.changeType(GameVar.settingsOldOrNew, SIZE)
                GameVar.setting.change_scale(SIZE)

            if GameVar.settingsOldOrNew == "New":
                if event.type == MOUSEWHEEL:
                    # GameVar.messageControl.message_summon("System", str(event))
                    result = GameVar.setting.step(event.y, HEIGHT)
                    if result:
                        GameVar.messageControl.message_summon("System", result)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(len(GameVar.setting.sets)):
                        set = GameVar.setting.sets[i]
                        if set.checkRange(E_MOUSE_POS[0], E_MOUSE_POS[1]):
                            if set.select:
                                set.select = False
                            else:
                                set.select = True
                                setIndex = i
                                GameVar.messageControl.message_summon("System", str(i))
                        else:
                            set.select = False
                elif event.type == KEYUP and GameVar.setting.getSet(setIndex).select:
                    GameVar.messageControl.message_summon("System", "setKey")
                    GameVar.setting.getSet(setIndex).input(event.key)
            else:
                if not THIS_SET.select:
                    if event.type == KEYUP and event.key == K_UP:
                        SETTING.setting_index_switch(-1)
                    elif event.type == KEYUP and event.key == K_DOWN:
                        SETTING.setting_index_switch(1)
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and THIS_SET.checkRange(event.pos[0], event.pos[1]):
                        THIS_SET.select = True
                else:
                    if event.type == MOUSEBUTTONDOWN and event.button == 1 and THIS_SET.checkRange(event.pos[0], event.pos[1]):
                        THIS_SET.select = False
                    elif event.type == KEYUP:
                        THIS_SET.input(event.key)

        elif GameVar.states == GameVar.STATES["SONGS_CHOOSE"]:
            sc = GameVar.songChoose
            if event.type == KEYDOWN and event.key == KEYS["songc_up"]:
                sc.dire = False
                sc.start = True
                sc.info_pass = False
                sc.step(SIZE, last_fps_time)
            elif event.type == KEYDOWN and event.key == KEYS["songc_down"]:
                sc.dire = True
                sc.start = True
                sc.info_pass = False
                sc.step(SIZE, last_fps_time)
            elif event.type == KEYUP and (event.key == KEYS["songc_up"] or event.key == KEYS["songc_down"]):
                sc.checkMiddle()
                sc.start = False
            elif event.type == KEYUP and event.key == 13:
                GameVar.states = GameVar.STATES["SONGS_CHOOSE_2"]
                return
            elif event.type == KEYUP and event.key == K_ESCAPE:
                GameVar.states = GameVar.STATES["LOBBY"]

        elif GameVar.states == GameVar.STATES["SONGS_CHOOSE_2"]:

            if GameVar.itemChoose.state == 0:
                if event.type == KEYUP and event.key == 13:
                    GameVar.states = GameVar.STATES["START"]
                    return
                elif event.type == KEYUP and event.key == K_ESCAPE:
                    GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
                    return
                elif event.type == KEYUP and event.key == KEYS["itemc_develop"]:
                    GameVar.itemChoose.state_change(True)
            elif GameVar.itemChoose.state == 1:
                if event.type == KEYUP and event.key == KEYS["itemc_back"]:
                    GameVar.itemChoose.state_change(False)
                buttons = {KEYS["itemc_up"]: "up", KEYS["itemc_right"]: "right", KEYS["itemc_down"]: "down",
                           KEYS["itemc_left"]: "left"}
                for button in buttons:
                    if event.type == KEYUP and event.key == button:
                        GameVar.item_choose_highlight.move(buttons[button])
                if event.type == KEYUP and event.key == 13:
                    if GameVar.item_choose_highlight.this_item > len(GameVar.backpack) - 1:
                        GameVar.itemChoose.item_ready = -1
                        GameVar.item_use = "null"
                    else:
                        GameVar.itemChoose.item_ready = GameVar.item_choose_highlight.this_item
                        GameVar.item_use = GameVar.backpack[GameVar.itemChoose.item_ready]
        elif GameVar.states == GameVar.STATES["RUNNING"]:
            if event.type == KEYUP and event.key == K_ESCAPE:
                GameVar.end.init()
                GameVar.end.coin_plus = end_score()
                # if not GameVar.end.coin_plus == "NOT_SCORE":
                #     GameVar.coin += coin_plus
                GameVar.coin += GameVar.end.coin_plus
                GameVar.this_time = time.time()
                GameVar.states = GameVar.STATES["GAME_OVER"]
                return
            buttons = {KEYS["yellow_up"]: 0, KEYS["yellow_right"]: 1, KEYS["yellow_down"]: 2, KEYS["yellow_left"]: 3}
            for button in buttons:
                if event.type == KEYDOWN and event.key == button:
                    GameVar.DMcomp[buttons[button]].iflighted = True
                    GameVar.DMcomp[buttons[button]].if_lighted = True
                if event.type == KEYUP and event.key == button:
                    GameVar.DMcomp[buttons[button]].iflighted = False
                    GameVar.DMcomp[buttons[button]].if_lighted = False
            if event.type == KEYUP and event.key == 13:
                GameVar.hero.is_button_press = True
            else:
                GameVar.hero.is_button_press = False
        elif GameVar.states == GameVar.STATES["GAME_OVER"]:
            if event.type == KEYUP and event.key == 13:
                GameVar.skip += 1
                if GameVar.skip > 3:
                    GameVar.skip = 3


class EHRTObject():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class AnimateObject(EHRTObject):
    def __init__(self, x, y, width, height):
        EHRTObject.__init__(self, x, y, width, height)
        self.state = 0
        self.imgs = []

    def appendImg(self, img, position):
        img_list = [img, position]
        self.imgs.append(img_list)

    def draw(self, num="all"):
        if num == "all":
            for img in self.imgs:
                canvas.blit(img[0], img[1])
        else:
            pass
            # canvas.blit(self.imgs[num][0],self.imgs[num][1])


class GameObject(EHRTObject):
    def __init__(self, life, defeat, x, y, width, height, img):
        EHRTObject.__init__(self, x, y, width, height)
        self.life = life
        self.defeat = defeat
        self.img = img

    def draw(self):
        canvas.blit(self.img, (self.x, self.y))

    def hit(self, component):
        c = component
        return self.x - c.width < c.x < self.x + self.width and \
               self.y - c.height < c.y < self.y + self.height


# 创建Hero类
class Hero(GameObject):
    def __init__(self, life, defence):
        GameObject.__init__(self, life, defence, WIDTH_2 - 25, HEIGHT_2 - 25, 50, 50, "null")
        self.score = 0
        self.Cy = self.y
        self.rect = Rect(self.x, self.y + self.height, self.width, self.height)
        self.rect.topleft = (self.x, self.y + self.height)
        self.is_button_press = False
        self.pictures = {"yellow": yellow_ring, "orange": orange_ring}
        self.colors = {"yellow": (204, 204, 0), "orange": (222, 129, 0)}
        self.main_rect = Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        pygame.draw.rect(canvas, self.colors[GameVar.gamemode], self.main_rect)
        canvas.blit(main_cover, (self.x, self.y))
        canvas.blit(self.pictures[GameVar.gamemode], (self.x, self.y))
        pygame.draw.rect(canvas, (0, 0, 0), self.rect)

    def lifeErase(self):
        hurt = GameVar.enemy_damage - self.defeat
        if hurt <= 0:
            hurt = 0.1
        self.life -= hurt

    def Cstep(self):
        if self.Cy < self.y + self.height:
            self.Cy += 60 * last_fps_time / 1000
            self.main_rect.top = self.Cy
            return False
        else:
            self.Cy = self.y + self.height
            self.main_rect.top = self.Cy
            return True

    def bang(self):
        self.lifeErase()


# 创建背景类
class BG:
    def __init__(self):
        self.number = 0
        self.x = 0
        self.y = 0
        self.if_night = True
        self.rect = Rect(0, 0, 1280, 720)
        self.color = (0, 0, 0)

    def draw(self):
        if self.if_night:
            if GameVar.states == GameVar.STATES["HOME_1"]:
                pygame.draw.rect(canvas, (42, 42, 63), BGblack)
            else:
                pygame.draw.rect(canvas, self.color, BGblack)


class End:
    def __init__(self):
        self.result = False
        self.score_img = score
        self.coin_img = coin
        self.dieImg = die
        self.speed = 500
        self.coin_plus = 0

    def draw(self):
        canvas.blit(self.dieImg, (0, 0))
        canvas.blit(self.result_img, (self.result_x, self.result_y))
        canvas.blit(self.score_img, (self.score_x, self.score_y))
        canvas.blit(self.coin_img, (self.score_x, self.score_y))

    def init(self, result=None):
        self.score = GameVar.hero.score
        if result == "WIN" or not result == None and GameVar.hero.life > 0:
            self.result_x = 0 - 362
            self.result_img = win
        elif result == "LOSE" or result == None:
            self.result_x = 0 - 316
            self.result_img = lose
        self.result_y = 0
        self.score_x = self.result_x - 162
        self.score_y = 0

    def animate(self):
        self.result_x += self.speed * last_fps_time / 1000
        self.score_x += self.speed * last_fps_time / 1000

    def animateOver(self):
        if self.result_x >= 0:
            self.result_x = 0
        if self.score_x >= 0:
            self.score_x = 0

def turnInt(target):
    if target:
        return 1
    else:
        return -1

# 创建Enemy类
class Enemy(GameObject):
    def __init__(self, number):
        GameObject.__init__(self, 1, 0, 0, 0, 50, 50, yellow)
        self.number = number
        self.attack = enemyAttack
        self.delete = False
        self.hero_distance = GameVar.moveSpeed * GameVar.moveTime
        if self.number == 0:
            self.x = GameVar.DMcomp[self.number].x
            self.y = GameVar.DMcomp[self.number].y - self.hero_distance
        if self.number == 1:
            self.x = GameVar.DMcomp[self.number].x + self.hero_distance
            self.y = GameVar.DMcomp[self.number].y
        if self.number == 2:
            self.x = GameVar.DMcomp[self.number].x
            self.y = GameVar.DMcomp[self.number].y + self.hero_distance
        if self.number == 3:
            self.x = GameVar.DMcomp[self.number].x - self.hero_distance
            self.y = GameVar.DMcomp[self.number].y
        self.ani = Sprite(
            pygame.image.load("images/animation/disappear.png"),
            (self.x - 10, self.y - 10),
            [(0, 0), (70, 0), (140, 0), (210, 0), (280, 0)],
            (70, 70),
            0.1
        )

    def step(self):
        speedSec = GameVar.moveSpeed
        speedFrame = speedSec * last_fps_time / 1000
        if self.number == 0:
            self.y += speedFrame
        elif self.number == 1:
            self.x -= speedFrame
        elif self.number == 2:
            self.y -= speedFrame
        elif self.number == 3:
            self.x += speedFrame
        self.ani.position = (self.x - 10, self.y - 10)

    def bang(self, if_score):
        self.life -= 1
        if self.life <= 0:
            self.delete = True
        if if_score:
            GameVar.hero.score += 5

    def getDistance(self, targetPos, targetSize):
        tx = targetPos[0]
        ty = targetPos[1]
        twidth = targetSize[0]
        theight = targetSize[1]
        if self.x == tx:
            dis = abs(self.y - ty)
        elif self.y == ty:
            dis = abs(self.x - tx)
        else:  # 求此对象中点与目标中点的距离
            thisMiddle = (self.x + self.width / 2, self.y + self.height / 2)
            targetMiddle = (tx + twidth / 2, ty + theight / 2)
            x = abs(thisMiddle[0] - targetMiddle[0])
            y = abs(thisMiddle[1] - targetMiddle[1])
            dis = (x * x + y * y) ** 0.5
        return dis

    def judge(self, DMpos, DMsize, **kwargs):
        dis = self.getDistance(DMpos, DMsize)
        if 35 < dis < 50:
            result = "Bad"
        elif 15 < dis <= 35:
            result = "Good"
        elif 0 <= dis <= 15:
            result = "Perfect"
        elif dis < 0:
            result = "MISS"
        elif dis > 50:
            result = "EMPTY"
        else:
            result = "Unknown"
        GameVar.messageControl.message_summon("System.Enemy.judge", "{0} distance:".format(result) + str(dis))
        GameVar.judgeResult.append(result)
        GameVar.judgeResult.append("Combo")
        GameVar.judgeResult.changeDisplay(result)

    def animation(self):
        result = self.ani.animation(canvas, 0, 4)
        if result == "Done":
            return "Done"


class JudgeResult():
    def __init__(self, result, canvas):
        self.result = result
        self.canvas = canvas
        self.bad = 0
        self.good = 0
        self.perfect = 0
        self.combo = 0
        self.judges = {"Bad": self.bad, "Good": self.good, "Perfect": self.perfect, "Combo": self.combo}
        self.alpha = 255
        self.text_size = writeText(self.result, (WIDTH - 3, 5), canvas, alpha=self.alpha, is_right=True, is_return_size=True)

    def draw(self):
        writeText("Combo: " + str(self.combo), (WIDTH - 3, 7 + self.text_size[1]), canvas, is_right=True)
        if self.result == "None":
            return
        if self.alpha > 0:
            writeText(self.result, (WIDTH - 3, 5), canvas, alpha=self.alpha, is_right=True, is_return_size=True)


    def changeDisplay(self, result):
        self.result = result
        self.alpha = 255

    def append(self, type, num=1):
        self.judges[type] += num
        self.update()

    def update(self):
        self.bad = self.judges["Bad"]
        self.good = self.judges["Good"]
        self.perfect = self.judges["Perfect"]
        self.combo = self.judges["Combo"]

    def outPut(self):
        return self.judges

    def set(self):
        self.result = "None"
        self.bad = 0
        self.good = 0
        self.perfect = 0
        self.combo = 0
        self.judges = {"Bad": self.bad, "Good": self.good, "Perfect": self.perfect, "Combo": self.combo}


    def delete(self):
        self.alpha -= 2
        if self.alpha <= 0:
            self.alpha = 0

class Item_choose:
    def __init__(self):
        self.state = 0
        self.this_item = -1
        self.item_ready = -1
        self.item_choose = item_choose
        self.choose = choose
        self.all_item = all_item
        self.item_choose_x = 0 + (WIDTH - 1280) / 2
        self.item_choose_y = 0
        self.index = 0
        self.line = 0
        self.start = "Start"
        self.last_time = 0
        self.intertal = 0.5
        self.compensatory = (0, 0)

    def init(self):
        self.state = 0
        self.item_choose_y = 0 + HEIGHT_2 - 360

    def main(self):
        if self.state == 0:
            if self.item_choose_y > 0 + HEIGHT_2 - 360:
                self.animate_0()
                if self.item_choose_y < 0 + HEIGHT_2 - 360:
                    self.item_choose_y = 0 + HEIGHT_2 - 360
            canvas.blit(die, (0, 0))
            canvas.blit(self.item_choose, (self.item_choose_x, self.item_choose_y))
            if not self.item_ready == -1:
                canvas.blit(GameVar.backpack[self.item_ready].img,
                            (591 + self.compensatory[0], self.item_choose_y + 311))
            self.write_start()
            if self.this_item == -1:
                return
            else:
                canvas.blit(items[self.this_item], (591 + self.compensatory[0], 311 + self.compensatory[1]))
        elif self.state == 1:
            canvas.blit(die, (0, 0))
            if self.item_choose_y < 134:
                self.animate_1()
                canvas.blit(self.item_choose, (self.item_choose_x, self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(GameVar.backpack[self.item_ready].img,
                                (591 + self.compensatory[0], self.item_choose_y + 311))
                return
            else:
                canvas.blit(self.all_item, (0 + self.compensatory[0], 0 + self.compensatory[1]))
                canvas.blit(self.item_choose, (self.item_choose_x, self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(GameVar.backpack[self.item_ready].img,
                                (591 + self.compensatory[0], self.item_choose_y + 311))
                self.item_draw_1_init()
                self.item_draw_1()
                GameVar.item_choose_highlight.draw()

    def state_change(self, dire):
        if dire:
            self.state += 1
        else:
            self.state -= 1
        if self.state > 1:
            self.state = 1
        elif self.state < 0:
            self.state = 0

    def item_draw_1_init(self):
        self.index = 0
        self.line = 0

    def item_draw_1(self):
        for item in GameVar.backpack:
            pos = (335 + self.compensatory[0] + self.index * (100 + 3),
                   76 + self.compensatory[1] + self.line * (100 + 3))
            canvas.blit(item.img, pos)
            writeText(str(item.number), (pos[0] + 100, pos[1] + 100), canvas, is_right_bottom=True)
            self.index += 1
            if self.index > 5:
                self.index = 0
                self.line += 1
            if self.line > 2:
                return True

    def write_start(self):
        writeText(self.start, (WIDTH - 226, HEIGHT - 45), canvas)
        if not ifDoAction(self.last_time, self.intertal):
            return
        self.last_time = time.time()

        if self.start == "Start>>>":
            self.start = "Start"
        self.start = self.start + ">"

    def animate_1(self):
        self.item_choose_y += 37 * last_fps_time / 134

    def animate_0(self):
        self.item_choose_y -= 37 * last_fps_time / 134


# 物品选单中的那个高光
class Item_Choose_Highlight(Item_choose):
    def __init__(self):
        super().__init__()
        self.img = choose

    def move(self, dire):
        if self.this_item == -1:
            self.this_item = 0
        elif dire == "up":
            if not self.this_item - 6 < 0:
                self.this_item -= 6
        elif dire == "right":
            if not self.this_item + 1 > 17:
                self.this_item += 1
        elif dire == "down":
            if not self.this_item + 6 > 17:
                self.this_item += 6
        elif dire == "left":
            if not self.this_item - 1 < 0:
                self.this_item -= 1

    def draw(self):
        if self.this_item == -1:
            return
        x = 332 + self.compensatory[0] + (self.this_item % 6) * 103 - 1
        y = 73 + self.compensatory[1] + (self.this_item - self.this_item % 6) / 6 * 103 - 1
        canvas.blit(self.img, (x, y))


# [quality,item_id]
boxs = [[[0, 0], [1, 1], [2, 2], [2, 3], [3, 4], [3, 5], [3, 6]], ["2st"]]


# 各个交互道具的类
class Home(AnimateObject):
    def __init__(self):
        AnimateObject.__init__(self, 0, 0, 1280, 720)
        self.list = []
        self.box_id = {"FallingStarLight": 0}

    def box(self, box, times):
        self.list = []
        GameVar.box.set_prob(1, 4, 40, 55)
        i = 0
        while i < times:
            if type(box) == str:
                GameVar.box.box_init(self.box_id[box])
            elif type(box) == int:
                GameVar.box.box_init(box, boxs)
            i += 1
            self.list.append(GameVar.box.summon()[0])
        self.print()
        return self.list

    def print(self):
        for item in self.list:
            # print(item.name)
            # GameVar.messageControl.message_summon("System","您抽到了 [" + item.quality + "]" + item.name)
            pass
        # GameVar.messageControl.message_summon("System", str(self.list))
        # print(self.list)
        return self.list

    def draw_result(self):
        GameVar.box_result.draw_result(1, self.list)




class GameVar:

    # 存储玩家信息
    def save():
        backpack = []
        for item in GameVar.backpack:
            backpack.append([item.id, item.number])
        data = {'coin': GameVar.coin, "backpack": backpack}
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

    moveTime = 1.2

    moveSpeed = 320.833 * 1.5

    hero = Hero(50.0, 0.0)
    # 英雄初始数值
    hero_defeat = hero.defeat
    hero_life = hero.life
    bg = BG()
    # 敌人刷新时间
    lastTime = 0
    intertal = 0.5
    # 用列表存储敌人
    enemies = []
    # 敌人的伤害值
    enemy_damage = 5
    enemy_score = 5
    score_to_coin = 30  # 分数/金币的比值
    # 绘画时间
    paintLastTime = 0
    paintIntertal = 0
    # 判子绘画时间
    DMLastTime = 0
    DMIntertal = 0
    # 主界面文字闪烁时间
    homeWordLastTime = 0
    homeWordIntertal = 1
    # 歌曲列表索引
    indexOfSong = 1
    # 歌曲开始时间
    gameStart = 0
    # 选单页数
    songsPage = 2
    # 用列表存储判子
    DMcomp = []
    # 歌曲是否要切换
    songsChangeAni = False
    # 歌曲切换的方向
    songsChangeDire = False
    # 是否在播放歌曲
    ifsongplaying = False
    # 当前在播放的曲子谱面
    thisSong = []
    # 最后一个谱子的时间
    lastIndexTime = 99999
    # 是否要暂停
    pause = False
    # 歌曲选单类
    songChoose = SongChoose(cph, SIZE, canvas)
    # 结束类
    end = End()
    # 结束时的time.time()
    this_time = 0
    # 结束是否跳过
    skip = 0

    # 物品选择类
    itemChoose = Item_choose()
    # 物品选择高光类
    item_choose_highlight = Item_Choose_Highlight()
    # 当前使用的物品
    item_use = "null"
    item_effect_y = 360 - 50

    # 宝箱
    box_animation = Box_Animation()
    box_result = Box_result((WIDTH, HEIGHT))

    # 帧率控制模块初始化
    fpsClock = pygame.time.Clock()
    # 帧率
    fps = 60
    # 宝箱类
    box = Box(hero, canvas)
    # 玩家C值
    player_c = 0
    # 玩家金币数
    coin = 0
    # 定时保存的时间间隔(sec)
    lastTime_of_save = 0
    interval_of_save = 300
    # 主界面背景音乐
    main_page_bgm = Bgm("songs/main_page/")
    # 当前歌曲长度
    this_song_long = 0
    # 当前游戏的模式
    gamemode = "yellow"
    # 大厅
    lirb = "images/lobby/images/"  # lobby_images_road_basic
    lobbyObjects = [LobbyObject(0, 16, 62, 46, "land"), LobbyItem(0, 8, 22, 34, "bianligui"),
                    LobbyItem(8, 6, 18, 18, "box"), LobbyItem(24, 4, 14, 27, "musicer"),
                    LobbyObject(0, 0, 62, 62, "fog"), LobbyObject(32, 22, 30, 38, "cover")]
    # ,LobbyItem(30, 5, 50, 50, "_yellow")]
    # 屏幕的x
    screen_x = 0

    home = Home()

    settingsOldOrNew = "Old"

    # 设置界面
    setting = Setting((WIDTH, HEIGHT), settingsOldOrNew)

    # 大厅力控制组
    lobbyForceControl = LobbyForceControl()

    backpack = []

    # 显示在左上角的玩家数值
    attrs = ["Health:" + str(hero.life),
             "Score:" + str(hero.score),
             "defend:" + str(hero.defeat),
             "damage:" + str(enemy_damage)]

    thisSongPath = "./songs/foundation_pack/Lost_Frequencis.mp3"

    songNotes = {}

    songPaths = {}

    # False为Old, True为New
    isNewOrOld = False

    enemy_animation = []

    judgeResult = JudgeResult("None", canvas)

    dataLines = 0

    enemyLight = PotLight(50, (255, 255, 255), canvas)

    messageControl = MessageControl(canvas)

    # 使用字典存储游戏进程
    STATES = {"HOME_0": 0, "HOME_1": 1, "SONGS_CHOOSE": 2, "SONGS_CHOOSE_2": 3, "START": 4, "ITEM": 5, "RUNNING": 6,
              "GAME_OVER": 7, "BOX": 8, "BOX_GET": 9, "LOBBY": 10, "SETTING": 11}
    States = []
    for state in STATES:
        States.append(state)
    states = STATES["HOME_0"]
    last_state = states

    ITEMS = None


# 物品的图片列表
ITEMS = Items(GameVar, canvas)

GameVar.ITEMS = ITEMS

# items=[ITEMS.get_item(0),ITEMS.get_item(1),ITEMS.get_item(2)]

# 创建判子类
class DMcomponent():
    def __init__(self, number, iflighted):
        # 基础数值
        self.number = number
        self.iflighted = iflighted
        self.if_lighted = False
        self.width = 50
        self.height = 50
        self.img = yellowDM
        self.imgLighted = yellow
        self.color = self.img
        self.x = 0
        self.y = 0
        self.set()

    def set(self):
        dis = 115
        if GameVar.gamemode == "yellow":
            if self.number == 0:
                self.x = GameVar.hero.x
                self.y = GameVar.hero.y - dis
            elif self.number == 1:
                self.x = GameVar.hero.x + dis
                self.y = GameVar.hero.y
            elif self.number == 2:
                self.x = GameVar.hero.x
                self.y = GameVar.hero.y + dis
            elif self.number == 3:
                self.x = GameVar.hero.x - dis
                self.y = GameVar.hero.y

    def checkLighted(self):
        if self.if_lighted:
            self.color = self.imgLighted
        else:
            self.color = self.img

    def draw(self):
        self.checkLighted()
        canvas.blit(self.color, (self.x, self.y))

    def lighten(self):
        if self.iflighted:
            self.iflighted = False

        else:
            self.iflighted = True

    def hit(self, component):
        c = component
        return self.x - c.width < c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height

    def bang(self):
        if self.hit:
            GameVar.hero.score += 1


# 游戏中
def commentInit():
    GameVar.DMcomp.clear()
    GameVar.DMcomp.append(DMcomponent(0, False))
    GameVar.DMcomp.append(DMcomponent(1, False))
    GameVar.DMcomp.append(DMcomponent(2, False))
    GameVar.DMcomp.append(DMcomponent(3, False))


def commentEnter(song):
    GameVar.lastTime = time.time() - GameVar.gameStart
    if not GameVar.indexOfSong >= len(song) - 1:
        if GameVar.lastTime >= song[GameVar.indexOfSong + 1]:
            GameVar.enemies.append(Enemy(song[GameVar.indexOfSong] - 1))
            GameVar.indexOfSong += 2
    else:
        GameVar.lastIndexTime = song[-1]
        if GameVar.lastTime >= GameVar.lastIndexTime + 10:
            GameVar.states = GameVar.STATES["GAME_OVER"]
            return


def commentEnterNew(song):
    GameVar.lastTime = time.time() - GameVar.gameStart
    if not GameVar.indexOfSong >= len(song) - 1:
        if GameVar.lastTime >= song[GameVar.indexOfSong + 1][1]:
            GameVar.enemies.append(Enemy(song[GameVar.indexOfSong][0]))
            GameVar.indexOfSong += 1
    else:
        GameVar.lastIndexTime = song[-1][1]
        if GameVar.lastTime >= GameVar.lastIndexTime + 10:
            GameVar.states = GameVar.STATES["GAME_OVER"]
            return


def commentDraw():
    GameVar.hero.draw()
    if not ifDoAction(GameVar.paintLastTime, GameVar.paintIntertal):
        return
    GameVar.paintLastTime = time.time()
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
        if enemy.delete:
            GameVar.enemies.remove(enemy)
    for DM in GameVar.DMcomp:
        if DM.iflighted:
            for enemy in GameVar.enemies:
                if DM.hit(enemy):
                    enemy.bang(True)
                    enemy.judge((DM.x, DM.y), (DM.width, DM.height))
                    DM.iflighted = False
                    DM.if_lighted = False
                    target = random.randint(0, 1)
                    if target == 0:
                        click.play()
                    else:
                        click2.play()
                    GameVar.enemy_animation.append(enemy)
                    GameVar.enemies.remove(enemy)
                    return


def commentAnimation():
    for enemy in GameVar.enemy_animation:
        if enemy.animation() == "Done":
            GameVar.enemy_animation.remove(enemy)


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
    GameVar.judgeResult.set()

    GameVar.skip = -1
    GameVar.enemies = []
    pygame.mixer.init()

    print(GameVar.song_names)
    pygame.mixer.music.load(GameVar.songPaths[GameVar.songChoose.info_name[GameVar.songChoose.number]])
    pygame.mixer.music.set_volume(0.2)
    # thisTime = GameVar.songChoose.info_thisTime
    # GameVar.this_song_long = int(thisTime[0]
    # ) * 60 + int(thisTime[2] + thisTime[3])
    GameVar.states = GameVar.STATES["RUNNING"]


def item_init(item_name):
    GameVar.hero.defeat = 0
    ITEMS.reset(GameVar, canvas)
    if GameVar.item_use == "null":
        return
    if item_name == "Star_light":
        ITEMS.get_item(0).buff()
    if item_name == "Diamond":
        # ITEMS.get_item(1).buff()
        GameVar.enemy_damage = GameVar.enemy_damage * 2
        GameVar.score_to_coin = GameVar.score_to_coin * 0.8
    if item_name == "Apple":
        ITEMS.get_item(2).buff()
        ITEMS.get_item(2).skill_over = time.time()
    GameVar.states = GameVar.STATES["ITEM"]


# 道具效果的主函数
def item_main(item_name):
    if GameVar.item_use == "null":
        return
    if item_name == "Star_light":
        ITEMS.get_item(0).skill_main()
    elif item_name == "Apple":
        ITEMS.get_item(2).skill_main()
    elif item_name == "Crystal":
        ITEMS.get_item(4).skill_main()


# 结算分数
def end_score():
    score = GameVar.hero.score
    song_score = len(GameVar.thisSong) / 2 * GameVar.enemy_score
    # if score < song_score/2:
    #     return "NOT_SCORE"
    # else:
    #     coin = score/GameVar.score_to_coin
    #     return coin
    coin = round(score / GameVar.score_to_coin)
    return coin


# 结束的动画效果
def end_animate():
    if GameVar.hero.life <= 0:
        if not GameVar.hero.Cstep() and GameVar.skip == -1:
            return
        if GameVar.skip == -1:
            GameVar.skip = 0
    elif GameVar.skip == -1:
        GameVar.skip = 0
    if GameVar.skip == 0:
        if GameVar.end.result:
            GameVar.hero.Cy = 385
        GameVar.end.draw()
        GameVar.end.animate()
        GameVar.end.animateOver()
        if ifDoAction(GameVar.this_time + 1, 2):
            writeText(str(GameVar.hero.score), (170, 239), canvas, color=(255, 228, 0), alpha=255, font=Font.score)
            GameVar.skip = 1
    elif GameVar.skip == 1:
        if GameVar.end.result:
            GameVar.hero.Cy = 385
        GameVar.end.result_x = 0
        GameVar.end.score_x = 0
        GameVar.end.draw()
        writeText(str(GameVar.hero.score), (170, 239), canvas, color=(255, 228, 0),  alpha=255, font=Font.score)
        writeText(str(GameVar.end.coin_plus), (145, 302), canvas, color=(255, 228, 0),  alpha=255, font=Font.score)
    elif GameVar.skip == 2:
        GameVar.end.draw()
        GameVar.states = GameVar.STATES["SONGS_CHOOSE"]
        # GameVar.main_page_bgm.allowFlag = True
        GameVar.main_page_bgm.set()
        # pygame.mixer.quit()


# 存储玩家信息
def save():
    # backpack = []
    # for item in GameVar.backpack:
    #     backpack.append([item.id, item.number])
    # data = {'coin': GameVar.coin, "backpack": backpack}
    # data = str(data)
    # with open("data/player.txt", "w") as file:
    #     file.write(data)
    # i = 0
    # with open("data/settings.txt", "r", encoding="UTF-8") as file:
    #     lines = file.readlines()
    # with open("data/settings.txt", "w", encoding="UTF-8") as file:
    #     for line in lines:
    #         if i == 0:
    #             line = str(SettingVar.keys) + "\n"
    #             file.write(line)
    #         else:
    #             file.write(line)
    #         i += 1
    GameVar.save()

# 加载玩家信息
def load():
    with open('data/player.txt') as file:
        for line in file:
            data = line.rstrip()
            break
    data = eval(data)
    GameVar.coin = data['coin']
    backpack = data["backpack"]
    for item in backpack:
        GameVar.backpack.append(Account_Item(item[0], item[1], ITEMS))


def lobby_main():
    for obj in GameVar.lobby.objects:
        if obj.checkHit(GameVar.hero):
            obj.is_lighted = True
        else:
            obj.is_lighted = False
        if obj.check_page(WIDTH):
            obj.draw(WIDTH, GameVar.screen_x, canvas)


def hall_main():
    canvas.blit(LobbyVar.canvas, (WIDTH_2 - 256, HEIGHT_2 - 256))
    LobbyVar.canvas.blit(hall_canvas_512, (0, 0))
    # LobbyVar.canvas.blit(LobbyVar.canvas,(0,0))
    for item in GameVar.lobbyObjects:
        item.draw(LobbyVar.canvas)


def setting_main():
    if GameVar.settingsOldOrNew == "New":
        GameVar.setting.mainBeforeDie(canvas)
        canvas.blit(die, (0, 0))
        GameVar.setting.mainAfterDie(canvas, pygame.mouse.get_pos())
    else:
        GameVar.setting.main_old(canvas)



def message_state_change():
    if not GameVar.last_state == GameVar.states:
        if GameVar.states == GameVar.STATES["LOBBY"]:
            pygame.key.set_repeat(1, 10)
        else:
            pygame.key.set_repeat()
        GameVar.messageControl.message_summon("System", "StateChange( " + GameVar.States[GameVar.last_state] + " to " + GameVar.States[
            GameVar.states] + " )")
        GameVar.last_state = GameVar.states


# 切换state
def changeState(state_to):
    GameVar.states = GameVar.STATES[state_to]


# 播放背景音乐
def bgm_play():
    GameVar.main_page_bgm.play()


# 启动谱面编辑器
def startIndexDesigner():
    pygame.quit()
    os.system("python indexDesigner.py")
    sys.exit()


def checkCoin(coin):
    return coin < GameVar.coin


def loadNote(path="./notes"):
    files = os.listdir(path)
    txtFiles = []
    for filename in files:
        if filename.endswith(".ehinote"):
            txtFiles.append(filename)
    for path in txtFiles:
        with open("./notes/" + path, "r", encoding="UTF-8") as file:
            i = 0
            noteData = []
            this_name = ""
            for line in file:
                if i == 0:
                    GameVar.songChoose.info_name.append(infoHandle(line))
                    this_name = infoHandle(line)
                elif i == 1:
                    GameVar.songChoose.info_little_name.append(infoHandle(line))
                elif i == 2:
                    GameVar.songPaths[this_name] = infoHandle(line)
                    thisSound = pygame.mixer.Sound(infoHandle(line))
                    soundLength = thisSound.get_length()
                    soundLength = int(soundLength)
                    secs = soundLength % 60
                    mins = int((soundLength - secs) / 60)
                    if secs < 10:
                        secs = "0" + str(secs)
                    finalLength = "{0}:{1}".format(mins, secs)
                    GameVar.songChoose.info_time.append(finalLength)
                elif i == 3:
                    print(infoHandle(line))
                    image = pygame.image.load(infoHandle(line)).convert()
                    pic = pygame.transform.scale(image, (250, 250))
                    GameVar.songChoose.imgs.append(pic)
                elif i == 4:
                    pass
                elif i == 5:
                    pass
                else:
                    noteData.append(eval(dataHandle(line)))
                i += 1
            GameVar.songNotes[this_name] = noteData.copy()
            #print(noteData)


def infoHandle(resourse):
    result = resourse.split(":")[-1]
    result = result.rstrip()
    result = result.lstrip()
    return result


def dataHandle(resourse):
    result = resourse.rstrip()
    result = result.lstrip()
    return result


# 程序主函数
def control():
    global canvas
    # 循环前执行

    # 定时保存
    if ifDoAction(GameVar.lastTime_of_save, GameVar.interval_of_save) and not GameVar.states == GameVar.STATES[
        "RUNNING"]:
        GameVar.lastTime_of_save = time.time()
        # try:
        #     save()
        # except:
        #     showError("写入data.txt时出现错误,有可能文件被锁定或删除")
        #     pygame.quit()
        #     sys.exit()
        save()
        GameVar.messageControl.message_summon("System", "已保存")
    if GameVar.states == GameVar.STATES["HOME_0"]:
        pygame.mixer.init()
        bgm_play()
        GameVar.bg.draw()
        writeText("按下任意键开始游戏", (WIDTH_2 - 135, HEIGHT - 60), canvas)
    elif GameVar.states == GameVar.STATES["HOME_1"]:
        GameVar.bg.draw()
        bgm_play()
        lobby_main()
        # GameVar.hero.draw()
    elif GameVar.states == GameVar.STATES["LOBBY"]:
        # print(LobbyVar.times)
        GameVar.bg.draw()
        bgm_play()
        hall_main()
    elif GameVar.states == GameVar.STATES["SETTING"]:
        GameVar.bg.draw()
        bgm_play()
        setting_main()
    elif GameVar.states == GameVar.STATES["SONGS_CHOOSE"]:
        GameVar.bg.draw()
        hall_main()
        canvas.blit(die, (0, 0))
        bgm_play()
        GameVar.itemChoose.init()
        GameVar.songChoose.main(SIZE, last_fps_time, GameVar.messageControl.if_message)
    elif GameVar.states == GameVar.STATES["SONGS_CHOOSE_2"]:
        GameVar.bg.draw()
        hall_main()
        canvas.blit(die, (0, 0))
        bgm_play()
        GameVar.songChoose.set(SIZE)
        GameVar.songChoose.start = False
        GameVar.songChoose.draw(GameVar.messageControl.if_message)
        GameVar.songChoose.info()
        GameVar.itemChoose.main()
    elif GameVar.states == GameVar.STATES["BOX"]:
        GameVar.bg.draw()
        bgm_play()
        GameVar.box_animation.main(canvas, SIZE, Font.text)
    elif GameVar.states == GameVar.STATES["BOX_GET"]:
        GameVar.bg.draw()
        bgm_play()
        # GameVar.messages = []
        # GameVar.home.box("FallingStarLight", 10)
        GameVar.box_result.main(canvas, SIZE, GameVar, die, last_fps_time)
        # GameVar.states = GameVar.STATES["LOBBY"]
    elif GameVar.states == GameVar.STATES["START"]:

        with open("data/songs.txt", encoding="gbk") as file:
            i = 0
            for line in file:
                if i == 1:
                    GameVar.song_names = eval(line.rstrip())
                i += 1
        print(GameVar.songNotes)
        print(GameVar.songChoose.info_name)
        print(GameVar.songChoose.number)

        GameVar.thisSong = GameVar.songNotes[GameVar.songChoose.info_name[GameVar.songChoose.number]]
        GameVar.isNewOrOld = True

        song_init()
        commentInit()
        if not GameVar.item_use == "null":
            item_init(GameVar.item_use.name)
            GameVar.item_effect_y = 360 - 50
        else:
            GameVar.gameStart = time.time()
            GameVar.states = GameVar.STATES["RUNNING"]
    elif GameVar.states == GameVar.STATES["ITEM"]:
        GameVar.bg.draw()
        bgm_play()
        canvas.blit(GameVar.item_use.img, (640 - 50, GameVar.item_effect_y))
        GameVar.item_effect_y += 345 * last_fps_time / 640 + 50
        if GameVar.item_effect_y >= 1280:
            time.sleep(1.0)
            GameVar.gameStart = time.time()
            GameVar.states = GameVar.STATES["RUNNING"]
    elif GameVar.states == GameVar.STATES["RUNNING"]:
        GameVar.bg.draw()

        commentEnterNew(GameVar.thisSong)
        commentStep()
        commentDelete()
        commentDraw()
        commentAnimation()
        GameVar.judgeResult.draw()
        GameVar.judgeResult.delete()
        if not GameVar.item_use == "null":
            item_main(GameVar.item_use.name)
        GameVar.attrs = [str(GameVar.hero.life),
                         str(GameVar.hero.score),
                         str(GameVar.hero.defeat),
                         str(GameVar.enemy_damage)]
        attr_orgin = [None, None, 0, 5]
        attr_color = [(255, 255, 255), (255, 255, 255), (204, 204, 0), (255, 0, 0)]
        attr_name = ["Health:", "Score:", "Defend:", "Enemy Damage:"]

        i_plus = 0
        for i in range(len(GameVar.attrs)):
            if i < 2 or not GameVar.attrs[i] == str(attr_orgin[i]):
                writeText(attr_name[i] + GameVar.attrs[i], (0, 40 * (i + i_plus)), canvas, color=attr_color[i])
            else:
                i_plus -= 1
        if GameVar.ifsongplaying == False and time.time() - GameVar.gameStart >= 1.2:
            pygame.mixer.music.play()
            GameVar.ifsongplaying = True
        # if GameVar.hero.life<=0 or time.clock()-Game
        # Var.gameStart>GameVar.this_song_long:
        # if GameVar.thisSong[-1] < GameVar.this_song_long:
        #     time_left_plus = GameVar.this_song_long - GameVar.thisSong[-1]
        # else:
        #     time_left_plus = 0
        time_left_plus = 3
        if GameVar.isNewOrOld:
            lastOne = GameVar.thisSong[-1][1]
        else:
            lastOne = GameVar.thisSong[-1]
        if time.time() - GameVar.gameStart > lastOne + time_left_plus:
            GameVar.states = GameVar.STATES["GAME_OVER"]
            GameVar.end.init("WIN")
            GameVar.end.coin_plus = end_score()
            # if not GameVar.end.coin_plus == "NOT_SCORE":
            #     GameVar.coin += coin_plus
            GameVar.coin += GameVar.end.coin_plus
            GameVar.this_time = time.time()
        elif GameVar.hero.life <= 0:
            GameVar.states = GameVar.STATES["GAME_OVER"]
            GameVar.end.init("LOSE")
            GameVar.end.coin_plus = end_score()
            # if not GameVar.end.coin_plus == "NOT_SCORE":
            #     GameVar.coin += coin_plus
            GameVar.coin += GameVar.end.coin_plus
            GameVar.this_time = time.time()
        # print(GameVar.lastTime)
    elif GameVar.states == GameVar.STATES["GAME_OVER"]:
        GameVar.bg.draw()
        commentDraw()
        #GameVar.main_page_bgm.set()
        end_animate()
    # 循环后执行
    message_state_change()
    if GameVar.messageControl.if_message:
        writeText("fps:" + str(int(GameVar.fpsClock.get_fps())), (0, 620), canvas, color=(25, 25, 255), font=Font.text)
        writeText("coin:" + str(GameVar.coin), (0, 650), canvas, color=(25, 25, 255))
        betaMessage()
        GameVar.messageControl.message_main()
    enterEffects()


def betaMessage():
    w, h = writeText("This is a beta version and you might meet some error or bug.If you meet them, please contact "
                     "with me on github or QQ.", (WIDTH, 0), canvas, is_right=True, font=Font.console,
                     is_return_size=True)
    writeText("这是一个测试版本并且你可能会遇到一些错误和bug。如果你遇到了，请在github或者QQ上联系我。", (WIDTH, h), canvas, is_right=True, font=Font.console)


enterAlpha = 255


def enterEffects():
    global enterAlpha, enter
    if enterAlpha <= 0:
        return
    enter = pygame.Surface(SIZE, SRCALPHA).convert()
    enter.set_alpha(enterAlpha)
    canvas.blit(enter, (0, 0))
    enterAlpha -= 1


def gameInit():
    GameVar.songChoose.set_imgs()
    # GameVar.songChoose.infoInit()
    try:
        load()
    except:
        showError("加载player.txt时出现错误,有可能文件被锁定或删除")
        pygame.quit()
        sys.exit()
    GameVar.messageControl.message_summon("System", "GameStart")

    GameVar.setting.load_settings(GameVar.settingsOldOrNew)
    # try:
    #     GameVar.setting.load_settings(GameVar.settingsOldOrNew)
    # except:
    #     showError("加载settings.txt时出现错误，有可能文件被锁定或删除")
    #     pygame.quit()
    #     sys.exit()
    loadNote()
    GameVar.songChoose.init(SIZE)
    GameVar.main_page_bgm.init()


gameInit()
while True:
    pygame.display.set_caption("八方 {0} {1}".format(VERSION, SIZE))

    last_fps_time = GameVar.fpsClock.tick(GameVar.fps)

    control()

    pygame.display.update()

    handleEvent()
