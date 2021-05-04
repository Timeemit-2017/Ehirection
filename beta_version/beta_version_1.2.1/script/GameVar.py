import pygame,sys,os,time,random
from script.Hero import *
from script.BackGround import *
from script.SongChoose import *
from script.End import *
from script.ItemChoose import *
from script.Box import *
from script.Bgm import *

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
    score_to_coin = 10  #分数/金币的比值
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
    fps=40
    #宝箱类
    box = Box(hero,canvas)
    #玩家C值
    player_c = 0
    #玩家金币数
    coin = 0
    #主界面背景音乐
    main_page_bgm = Bgm("songs/main_page/E_nightSong.mp3",267)
    #消息列表
    messages = []
    #是否显示控制台
    if_message = True
    #使用字典存储游戏进程
    STATES={"HOME_0":0,"HOME_1":1,"SONGS_CHOOSE":2,"SONGS_CHOOSE_2":3,"START":4,"ITEM":5,"RUNNING":6,"GAME_OVER":7,"BOX":8,"BOX_GET":9}
    States = []
    for state in STATES:
        States.append(state)
    states=STATES["BOX_GET"]
    last_state = states