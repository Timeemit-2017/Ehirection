import pygame,os
from script.Objects import *
pygame.init()

#加载英雄图片
yellowC=pygame.image.load("images/mainC/yellowC.png")
yellowM=pygame.image.load("images/mainC/yellowM.png")
#加载敌人图片
yellow=pygame.image.load("images/yellow.png")
#加载判子图片
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
star_light=pygame.image.load("images/items/ehi1st_/star_light.png")
#加载道具特效精灵图
item_effect_sprite=pygame.image.load("images/items/ehi1st_/item_effect_sprite.png")

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0,0)
canvas = pygame.display.set_mode((WIDTH, HEIGHT),pygame.NOFRAME)

canvas.fill((255,255,255))
BGblack = canvas.get_rect()

last_fps_time = 0
