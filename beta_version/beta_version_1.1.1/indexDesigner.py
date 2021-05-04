'''
Created on 2020-3-2

@author: 李天立 Time_emit
'''
# coding:utf-8
import pygame, sys, random, time, easygui,win32ui
from pygame.locals import *
# 初始化pygame环境
pygame.init()
pygame.mixer.music.load("songs/foundation_pack/sakurashi.mp3")
# 创建一个长宽分别为480/650窗口
canvas = pygame.display.set_mode((480,360))
canvas.fill((255, 255, 255))

# 设置窗口标题
pygame.display.set_caption("indexDesigner")
#导入图片素材
# a_up=pygame.image.load("indexImages/arrow/up.png")
# a_down=pygame.image.load("indexImages/arrow/down.png")
# a_left=pygame.image.load("indexImages/arrow/left.png")
# a_right=pygame.image.load("indexImages/arrow/right.png")

a_pup=pygame.image.load("indexImages/arrow/purple/up.png")
a_pdown=pygame.image.load("indexImages/arrow/purple/down.png")
a_pleft=pygame.image.load("indexImages/arrow/purple/left.png")
a_pright=pygame.image.load("indexImages/arrow/purple/right.png")

nightBG=pygame.image.load("indexImages/nightBG.png")
whiteBG=pygame.image.load("indexImages/whiteBG.png")
_line_=pygame.image.load("indexImages/line.png")
timepic=pygame.image.load("indexImages/time.png")

edit=pygame.image.load("indexImages/edit.png")
editK=pygame.image.load("indexImages/editK.png")
editAdown=pygame.image.load("indexImages/editArrowDown.png")
editAup=pygame.image.load("indexImages/editArrowUP.png")

night=True
if night:
    color=255
else:
    color=0
proList=[]
# try:
#     with open("songs") as file:
#         ifname=True
#         for line in file:
#             if ifname:
#                 song=[]
#                 song.append(line.rstrip)#name
#                 ifname=False
#             else:
#                 song.append(line.rstrip)#index
#                 proList.append(song)
#                 ifname=True
# except:
#     easygui.msgbox("歌曲文件丢失！请尝试重新下载游戏！")
def ifDoAction(lastTime,interval):
        if lastTime==0:
            return True
        currectTime=time.time()
        return currectTime-lastTime>=interval
thisProName="name"
thisPro=0

hitArrows=[]
def handleEvent():
    global thisProName,load
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        if GameVar.states==GameVar.STATES["MAIN_0"]:
            if event.type==KEYDOWN:
                GameVar.states=GameVar.STATES["MAIN_1"]
        elif GameVar.states==GameVar.STATES["MAIN_1"]:
            if event.type==MOUSEBUTTONDOWN and event.button==1:
                if event.pos[0]>=195 and event.pos[0]<=263 and event.pos[1]<=149 and event.pos[1]>=100:
                    #"new"
                    GameVar.states=GameVar.STATES["NEW"]
                    return
                elif event.pos[0]>=195 and event.pos[0]<=263 and event.pos[1]<=199 and event.pos[1]>=150:
                    GameVar.states=GameVar.STATES["OPEN"]
                elif event.pos[0]>=195 and event.pos[0]<=263 and event.pos[1]<=249 and event.pos[1]>=200:
                    GameVar.states=GameVar.STATES["QUIT"]
        elif GameVar.states==GameVar.STATES["NEW"]:
            if event.type==MOUSEBUTTONDOWN and event.button==1:
                if event.pos[0]>=195 and event.pos[0]<=263 and event.pos[1]<=149 and event.pos[1]>=100:
                    thisProName=easygui.enterbox("项目名")
                elif event.pos[0]>=195 and event.pos[0]<=263 and event.pos[1]<=199 and event.pos[1]>=150:
                    GameVar.states=GameVar.STATES["PROINIT"]
        elif GameVar.states==GameVar.STATES["MAKING"]:
            if event.type==KEYDOWN:
                if event.key==K_SPACE:
                    if GameVar.time.start==False:
                        GameVar.time.pauseTime += time.clock() - GameVar.time.oldtime+0.05
                        GameVar.time.start=True
                        if GameVar.ifSongsPlaying==False:
                            pygame.mixer.music.play()
                            GameVar.ifSongsPlaying=True
                        else:
                            pygame.mixer.music.unpause()
                    else:
                        GameVar.time.start=False
                        GameVar.time.oldtime=time.clock()
                        pygame.mixer.music.pause()
                if GameVar.time.start==True:
                    if event.key==K_UP:
                        GameVar.arrowList.append(Arrow(GameVar.arrowImgs[0],GameVar.time.time,False,1))
                    elif event.key==K_RIGHT:
                        GameVar.arrowList.append(Arrow(GameVar.arrowImgs[1],GameVar.time.time,True,2))
                    elif event.key==K_DOWN:
                        GameVar.arrowList.append(Arrow(GameVar.arrowImgs[2],GameVar.time.time,False,3))
                    elif event.key==K_LEFT:
                        GameVar.arrowList.append(Arrow(GameVar.arrowImgs[3],GameVar.time.time,True,4))
                else:
                    if event.key==280:#PageUp
                        if len(GameVar.arrowList)==0:
                            return
                        GameVar.time.timetime=GameVar.arrowList[0].timex
                    elif event.key==281:#PageDown
                        if len(GameVar.arrowList)==0:
                            return
                        GameVar.time.time=GameVar.arrowList[-1].timex
                    elif event.key==K_LEFT:
                        GameVar.time.keyDownLeft=True
                    elif event.key==K_RIGHT:
                        GameVar.time.keyDownRight=True
                    elif event.key==K_s:
                        answer=easygui.choicebox(msg="是否要退出并保存",title="确认退出",choices=["Yes","No"])
                        if answer=="Yes":
                            GameVar.states=GameVar.STATES["SAVE"]
            elif event.type==KEYUP:
                GameVar.time.keyDownLeft=False
                GameVar.time.keyDownRight=False
class Time():
    def __init__(self):
        self.x=240
        self.y=0
        self.height=480
        self.width=1
        self.time=0
        self.start=False
        self.lastTime=0
        self.pauseTime=0
        self.oldtime=0
        self.keyDownLeft=False
        self.keyDownRight=False
    def paint(self):
        canvas.blit(timepic,(self.x,self.y))
    def getTime(self):
        if not self.start==False:
            self.time=time.clock()-self.pauseTime
        else:
            self.time=self.time
    def step(self):
        if self.keyDownLeft==True:
            self.time-=0.05
        elif self.keyDownRight==True:
            self.time+=0.05
    def timeBarrier(self):
        if self.time<=0:
            self.time=0
class Arrow():
    def __init__(self,img,x,num,dire):
        self.img=img
        self.num=num
        if self.num:
            self.width=44
            self.height=26
        else:
            self.width=26
            self.height=44
        self.timex=x#谱面坐标
        self.x=240-self.width/2-((GameVar.time.time-self.timex)*88)
        self.y=180-self.height/2
        self.dire=dire
    def draw(self):
        canvas.blit(self.img,(self.x,self.y))
    def step(self):
        self.x=240-self.width/2-((GameVar.time.time-self.timex)*88)
    def checkHit(self,c):
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
    def highLight(self):
        global hitArrows
        if self.checkHit(GameVar.time):
            rect=self.img.get_rect()
            rect.topleft=(self.x,self.y)
            pygame.draw.rect(canvas,(255,255,255),rect)
            hitArrows.append(self)
        else:
            try:
                hitArrows.remove(self)
            except:
                return
    def appendList(self):
        GameVar.hitArrows.append(self)


hitArrows=[]
#创建编辑栏类
class Edit():
    def __init__(self):
        self.arrowNum=len(hitArrows)
        self.x=0
        self.y=0
        self.height=156
        self.width=145
        self.img=edit
        self.Kimg=editK
        self.Aup=editAup
        self.Adown=editAdown
        self.x=0-self.width
        self.y=0
        self.aupY=0
        self.adownY=0
        self.aAniDire=True
        self.aniSpeed=0
    def draw(self):
        canvas.blit(self.img,(self.x,0))
        canvas.blit(self.Kimg, (self.x,0))
        canvas.blit(self.Aup, (0,self.aupY))
        canvas.blit(self.Adown, (0,self.adownY))
    def drawArrows(self):
        self.arrowNum=len(hitArrows)

        for arrow in hitArrows:
            print("a")
    def animation(self):
        if not self.x>=0:
            if self.x<=-self.width/2:
                self.aniSpeed+=1
            else:
                self.aniSpeed-=1
            self.x+=self.aniSpeed
        else:
            self.x=0
            self.aniSpeed=0
    def arrowAni(self):#箭头抖动特效
        if self.aAniDire:
            self.aupY+=1
            self.adownY-=1
            if self.aupY>=2:
                self.aAniDire=False
        else:
            self.aupY-=1
            self.adownY+=1
            if self.aupY<=0:
                self.aAniDire=True

def save():
    savelist=[]
    savelist.append(thisProName)
    for arrow in GameVar.arrowList:
        savelist.append(arrow.dire)
        savelist.append(arrow.timex)
    return savelist
def fillText(text, position,size):
    global color
    TextFont = pygame.font.Font('script/NotoSansHans-Light.otf', size)
    newText = TextFont.render(str(text), True, (color,color,color))
    canvas.blit(newText, position)
def drawBG():
    if night:
        canvas.blit(nightBG,(0,0))
    else:
        canvas.blit(whiteBG,(0,0))
#创建软件数值类
class GameVar():
    STATES={"MAIN_0":1,"MAIN_1":2,"NEW":3,"OPEN":4,"PROINIT":5,"MAKING":6,"SAVE":7,"QUIT":8}
    states=STATES["MAIN_0"]
    arrowImgs=[a_pup,a_pright,a_pdown,a_pleft]

    hitArrows=[]
    time=Time()
    edit=Edit()
    arrowList=[]

    ifSongsPlaying=False
def componentDraw():
    for a in GameVar.arrowList:
        a.highLight()
        a.draw()
        a.step()
#创建控制软件进程的方法
def control():
    global thisPro,thisProName,proList
    if GameVar.states==GameVar.STATES["MAIN_0"]:
        drawBG()
        fillText("按下任意键继续",(170,300),20)
    elif GameVar.states==GameVar.STATES["MAIN_1"]:
        drawBG()
        fillText("new",(195,100),40)
        fillText("open",(195,150),40)
        fillText("quit",(195,200),40)
        #fillText("quit",(263,200),40)
        thisProName="[name]"
    elif GameVar.states==GameVar.STATES["NEW"]:
        drawBG()
        fillText(thisProName,(195,100),40)
        fillText("start!",(195,150),40)
    elif GameVar.states==GameVar.STATES["PROINIT"]:
        proList.append([thisProName,len(proList)-1])
        thisPro=len(proList)-1
        pygame.mixer.music.set_volume(0.2)
        GameVar.states=GameVar.STATES["MAKING"]
    elif GameVar.states==GameVar.STATES["MAKING"]:
        drawBG()
        canvas.blit(_line_,(0,0))
        # GameVar.edit.draw()
        # GameVar.edit.arrowAni()
        GameVar.time.paint()
        GameVar.time.getTime()
        GameVar.time.step()
        GameVar.time.timeBarrier()
        componentDraw()
    elif GameVar.states==GameVar.STATES["OPEN"]:
        drawBG()
        songs_can_open = []
        with open("songs.txt") as file:
            for line in file:
                songs_can_open.append(eval(line.rstrip())[0])
            songs = easygui.choicebox("choose the song you want to open", "choose the song", songs_can_open)
            #print(songs)
        with open("songs.txt") as file:
            for line in file:
                #print(eval(line.rstrip()))
                if eval(line.rstrip())[0] == songs:
                    arrowlist = eval(line.rstrip())
                    pygame.mixer.music.load("songs/foundation_pack/" + arrowlist[0] +".mp3")
                    arrowlist.pop(0)
                    i = 0
                    arrowlist_dire_pictures = [a_pup, a_pright, a_pdown, a_pleft]
                    arrowlist_dire_nums = [False,True,False,True]
                    while i<len(arrowlist):
                        dire = arrowlist[i]
                        this_dire_img = arrowlist_dire_pictures[dire-1]
                        this_dire_time = arrowlist[i+1]
                        this_num = arrowlist_dire_nums[dire-1]
                        GameVar.arrowList.append(Arrow(this_dire_img,this_dire_time,this_num,dire))
                        i += 2
                        
                    #print(GameVar.arrowList)
                    break

            GameVar.states = GameVar.STATES["MAKING"]

        fillText(songs,(100,100),10)
    elif GameVar.states==GameVar.STATES["SAVE"]:
        with open("songs.txt", "a") as file:
            file.write(str(save()))
        GameVar.states=GameVar.STATES["MAIN_1"]
    elif GameVar.states==GameVar.STATES["QUIT"]:
        pygame.quit()
        sys.exit()
    #print(GameVar.states)
while True:
    handleEvent()

    control()

    pygame.display.update()

    pygame.time.delay(15)