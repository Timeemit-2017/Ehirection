import pygame,sys,easygui,os,tkinter,tkinter.filedialog,time, tkinter.messagebox
from pygame.locals import *
from mutagen.mp3 import MP3


from indexDesigner_script.BackGround import *
from indexDesigner_script.Button import *
from indexDesigner_script.Font import *
from indexDesigner_script.Arrow import *
from indexDesigner_script.History import *

pygame.init()

WIDTH = 1280
HEIGHT = 720
SIZE = (WIDTH, HEIGHT)
canvas = pygame.display.set_mode((WIDTH, HEIGHT),HWSURFACE|RESIZABLE)
canvas.fill((0,0,0))

originCaption = "Index Designer 1.0.0"
pygame.display.set_caption(originCaption)

arrow_name = ["up", "right", "down", "left"]
arrow_img = []
for name in arrow_name:
    arrow_img.append(pygame.image.load("indexImages/arrow/purple/" + name + ".png"))
middleLine = pygame.Surface((WIDTH, 1))
middleLineColor = (255,0,255)
middleLine.fill((255,0,255))
TimeLine = pygame.Surface((1,HEIGHT))
TimeLineColor = (0,0,255)
TimeLine.fill(TimeLineColor)
window = tkinter.Tk()
window.withdraw()

MUSIC_OFFSET = 0
LEFT_HOLD = False
RIGHT_HOLD = False
aHOLD = False
dHOLD = False
shouldBeRecored = False
def handleEvent():
    global canvas,SIZE,WIDTH,HEIGHT,WIDTH_2,HEIGHT_2,MOUSE_POS,middleLine,middleLineColor,BUTTONLOCK,MUSIC_OFFSET,LEFT_HOLD,RIGHT_HOLD,aHOLD,dHOLD,shouldBeRecored
    #常量
    MOUSE_POS = pygame.mouse.get_pos()
    BUTTONLOCK = False #按钮锁，每一次点击只可以激活一个按钮
    eventList = pygame.event.get()
    buttonPressed = pygame.key.get_pressed()
    shouldBeRecored = False
    # print(eventList)
    for event in eventList:
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_F1:
            if checkState("INDEX"):
                save(exit=True)
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            SIZE = event.size
            WIDTH = event.size[0]
            HEIGHT = event.size[1]
            WIDTH_2 = WIDTH / 2
            HEIGHT_2 = HEIGHT / 2

            Locals.backGround = BackGround(
                color = (0,0,0),
                size = SIZE
            )

            for button in Locals.buttons:
                button.video_change(SIZE)

            middleLine = pygame.Surface((WIDTH, 1))
            middleLine.fill(middleLineColor)
            TimeLine = pygame.Surface((1, HEIGHT))
            TimeLine.fill(TimeLineColor)

            canvas = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | RESIZABLE)
        for button in Locals.buttons:
            if button.checkRange(MOUSE_POS):
                button.is_hightLight = True
                if event.type == MOUSEBUTTONUP and not BUTTONLOCK:
                    var = button.click(Locals.state)
                    if type(button.command) == str:
                        if not var == "StateNotMatch":
                            print(var)
                            try:
                                Locals.state = Locals.STATES[var]
                                BUTTONLOCK = True
                            except:
                                pass


            else:
                 button.is_hightLight = False
        if checkState("INDEX"):
            if event.type == USEREVENT:
                Locals.startIndexFlag = False
                Locals.thisTime = Locals.thisSongLong * 1000
                pygame.mixer.music.play()
                pygame.mixer.music.pause()
                pygame.mixer.music.set_pos(Locals.thisTime)
                Locals.if_restart = True

            if Locals.startIndexFlag:
                direc = {K_UP: 0, K_RIGHT: 1, K_DOWN: 2, K_LEFT: 3}
                if event.type == KEYDOWN and event.key == K_SPACE:
                    pygame.mixer.music.pause()
                    Locals.startIndexFlag = False
                for dire in direc:
                    if event.type == KEYDOWN and event.key == dire:
                        set_arrow(Locals.thisTime/1000, direc[dire])
                        shouldBeRecored = True
            else:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if Locals.if_restart:
                        if Locals.thisTime == Locals.thisSongLong:
                            #还在末尾就回到开头
                            Locals.thisTime = 0
                            Locals.if_restart = False
                        else:
                            #结束后又调了位置位置不变
                            Locals.if_restart = False
                    MUSIC_OFFSET = pygame.mixer.music.get_pos() - Locals.thisTime
                    print(MUSIC_OFFSET)
                    pygame.mixer.music.unpause()
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.set_pos(Locals.thisTime/1000)
                    Locals.startIndexFlag = True
                    # Locals.thisTime = pygame.mixer.music.get_pos() - MUSIC_OFFSET
                    break
                elif event.type == KEYDOWN and event.key == 13:
                    Locals.editFloor += 1
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    Locals.editFloor -= 1
                if Locals.editFloor < 0:
                    Locals.editFloor = 0
                elif Locals.editFloor > 2:
                    Locals.editFloor = 2

                if event.type == KEYDOWN and event.key == K_LEFT:
                    if Locals.editFloor == 0:
                        LEFT_HOLD = True
                        if event.mod & KMOD_SHIFT:
                            Locals.moveSpeed = 40 * 50 / Locals.scaleTimes
                        else:
                            Locals.moveSpeed = 40
                        if event.mod & KMOD_CTRL:
                            Locals.deHighLight = False
                        else:
                            Locals.deHighLight = True
                    elif Locals.editFloor == 1 and event.mod & KMOD_ALT:
                        pass
                    elif Locals.editFloor == 2:
                        Locals.highLightArrows[Locals.editChoose].dire = 3
                        Locals.highLightArrows[Locals.editChoose].setImg(arrow_img[3])
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    if Locals.editFloor == 0:
                        RIGHT_HOLD = True
                        if event.mod & KMOD_SHIFT:
                            Locals.moveSpeed = 40 * 50 / Locals.scaleTimes
                        else:
                            Locals.moveSpeed = 40
                        if event.mod & KMOD_CTRL:
                            Locals.deHighLight = False
                        else:
                            Locals.deHighLight = True
                    elif Locals.editFloor == 2:
                        Locals.highLightArrows[Locals.editChoose].dire = 1
                        Locals.highLightArrows[Locals.editChoose].setImg(arrow_img[1])
                if event.type == KEYDOWN and event.key == K_UP:
                    if Locals.editFloor == 1:
                        Locals.editChoose -= 1
                    elif Locals.editFloor == 2:
                        Locals.highLightArrows[Locals.editChoose].dire = 0
                        Locals.highLightArrows[Locals.editChoose].setImg(arrow_img[0])
                if event.type == KEYDOWN and event.key == K_DOWN:
                    if Locals.editFloor == 1:
                        Locals.editChoose += 1
                    elif Locals.editFloor == 2:
                        Locals.highLightArrows[Locals.editChoose].dire = 2
                        Locals.highLightArrows[Locals.editChoose].setImg(arrow_img[2])
                if event.type == KEYDOWN and event.key == K_a:
                    aHOLD = True
                if event.type == KEYDOWN and event.key == K_d:
                    dHOLD = True



                if event.type == KEYUP and event.key == K_LEFT:
                    LEFT_HOLD = False
                if event.type == KEYUP and event.key == K_RIGHT:
                    RIGHT_HOLD = False
                if event.type == KEYUP and event.key == K_a:
                    aHOLD = False
                    shouldBeRecored = True
                if event.type == KEYUP and event.key == K_d:
                    dHOLD = False
                    shouldBeRecored = True
                if event.type == KEYUP and event.key == K_DELETE:
                    if Locals.editFloor == 2:
                        Locals.arrows.remove(Locals.highLightArrows[Locals.editChoose])
                        Locals.highLightArrows.pop(Locals.editChoose)
                        shouldBeRecored = True

                if Locals.editChoose < 0:
                    Locals.editChoose = 0
                elif Locals.editChoose >= len(Locals.highLightArrows):
                    Locals.editChoose = len(Locals.highLightArrows) - 1

                if not Locals.highLightArrows:
                    Locals.editFloor = 0

                if event.type == KEYDOWN and event.key == K_F2:
                    save()
                    changeState("HOME")


            if event.type == KEYUP and event.mod & KMOD_CTRL and event.mod & KMOD_ALT and event.key == K_z:
                temp = Locals.history.undo()
                if temp != "None":
                    Locals.arrows = temp.copy()
                # print(Locals.history.history, Locals.history.index)
            elif event.type == KEYUP and event.mod & KMOD_CTRL and event.key == K_z:
                temp = Locals.history.redo()
                if temp != "None":
                    Locals.arrows = temp.copy()
            if event.type == KEYUP and event.mod & KMOD_CTRL and event.key == K_s:
                save()
            if event.type == MOUSEWHEEL and pygame.key.get_mods() & KMOD_CTRL:
                Locals.scaleTimes += event.y * 10
                if Locals.scaleTimes <= 10:
                    Locals.scaleTimes = 10
            if event.type == KEYUP and event.key == K_F3:
                willStart = True
                start = 0
                if not easygui.boolbox("是否开始快捷编写旋转结构？"):
                    willStart = False
                if easygui.boolbox("顺时针还是逆时针？", choices=["顺时针", "逆时针"]):
                    # 顺时针
                    dire = 1
                else:
                    # 逆时针
                    dire = -1
                choices = ["上", "右", "下", "左"]
                temp = easygui.choicebox("以哪个方向为开始？", choices=choices)
                if temp is None:
                    willStart = False
                else:
                    start = choices.index(temp)
                if willStart:
                    for arrow in Locals.highLightArrows:
                        arrow.dire = start
                        arrow.setImg(arrow_img[start])
                        start += dire
                        if start > 3:
                            start = 0
                        elif start < 0:
                            start = 3
                        print("oneOVer")
                    shouldBeRecored = True
                    print("over")

            if shouldBeRecored:
                if Locals.history.checkIfHasUndo():
                    Locals.history.update()
                Locals.history.append(Locals.arrows.copy())



def askformusic():
    print("askmusic")
    var = tkinter.filedialog.askopenfilename(title="选择谱面要使用的音乐",
                                       initialdir="./songs",
                                       filetypes=[("*MP3", ".mp3")]
                                       )
    if var == "":
        return
    varSplited = var.split("/")[-1]
    Locals.project_music_road = var

    #print(var)
    return varSplited

def askforname():
    var = easygui.enterbox("请输入项目名称","项目名称")
    Locals.project_name = var
    print(var)
    return var

def askForLittleName():
    var = easygui.enterbox("请输入项目小名称", "项目小名称")
    Locals.project_littleName = var
    print(var)
    return var

def askforcover():
    var = tkinter.filedialog.askopenfilename(title="选择谱面要使用的封面",
                                             initialdir="./images/start/songs",
                                             filetypes=[("*PNG", ".png"), ("*JPG", ".jpg")]
                                             )
    if var == "":
        return
    varSplited = var.split("/")[-1]
    Locals.project_cover_road = var

    print(var)
    return varSplited

def askForAuthor():
    var = easygui.enterbox("请输入音乐作者名称", "作者名称")
    Locals.project_author = var
    print(var)
    return var

def askForDesigner():
    var = easygui.enterbox("请输入谱师名称", "谱师名称")
    Locals.project_noteDesigner = var
    print(var)
    return var

#询问存档地址
def askForData():
    var = tkinter.filedialog.askopenfilename(title="选择存档",
                                             initialdir="./notes",
                                             filetypes=[("*EHINOTE", ".ehinote")]
                                             )
    return var

def createNewProject():
    Locals.project_name = "Unnamed"
    if Locals.project_music_road == "Undefined":
        Locals.project_music_road = "./songs/foundation_pack/idealism,jinsang - winter bokeh.mp3"
    if Locals.project_cover_road == "Undefined":
        Locals.project_cover_road = "./images/start/songs/winter bokeh.jpg"
    Locals.state = Locals.STATES["CREATE"]

class Locals():
    thisCaption = originCaption

    STATES = {"LOAD":0, "HOME":1, "CREATE":2, "OPEN":3, "QUIT":4, "INDEX":5, "INFO":6}
    state = STATES["HOME"]

    project_name = "name"
    project_littleName = "littleName"
    project_music_road = "Undefined"
    project_cover_road = "Undefined"
    project_author = "Unknown"
    project_noteDesigner = "Unknown"

    fps = 60
    clock = pygame.time.Clock()
    mode = "yellow"
    arrows = []
    highLightArrows = []

    startIndexFlag = False
    thisTime = 0

    moveSpeed = 40

    editFloor = 0

    editChoose = 0

    editChoose1 = 0

    thisSongLong = 50000

    if_restart = False

    history = History()

    textPath = ""

    scaleTimes = 100

    deHighLight = True

    backGround = BackGround(color = (0,0,0),
                            size = (1280, 720)
                            )

    buttons = [Button((440, 260), (400, 100), "OPEN",
                      this_state= STATES["HOME"],
                      text="Open a project",
                      font=Font.normal_text,
                      to = "Locals.state"
                      ),
               Button((440, 360), (400, 100), "QUIT",
                      this_state= STATES["HOME"],
                      text="Back To Game",
                      font=Font.normal_text,
                      to = "Locals.state"
                      ),
               FunctionButton((440, 160), (400, 100), askforname,
                              this_state=STATES["CREATE"],
                              text="UnNamed",
                              title="Name",
                              font=Font.normal_text,
                              to = "Locals.project_name"
                              ),
               Button((440, 260), (400, 100), "INFO",
                      this_state=STATES["CREATE"],
                      text="Edit Info",
                      font=Font.normal_text,
                      to="Locals.state"
                      ),
               FunctionButton((440, 60), (400, 100), askForLittleName,
                              this_state=STATES["INFO"],
                              text="UnNamed",
                              title="LittleName",
                              font=Font.normal_text,
                              to="Locals.project_littleName"
                              ),
               FunctionButton((440, 160), (400, 100), askformusic,
                              this_state=STATES["INFO"],
                              text="Undefined",
                              title="SongRoad",
                              font=Font.normal_text,
                              to="Locals.project_music_road"
                              ),
               FunctionButton((440, 260), (400, 100), askforcover,
                              this_state=STATES["INFO"],
                              text="Undefined",
                              title="CoverRoad",
                              font=Font.normal_text,
                              to="Locals.project_cover_road"
                              ),
               FunctionButton((440, 360), (400, 100), askForAuthor,
                              this_state=STATES["INFO"],
                              text="None",
                              title="Author",
                              font=Font.normal_text,
                              to="Locals.project_author"
                              ),
               FunctionButton((440, 460), (400, 100), askForDesigner,
                              this_state=STATES["INFO"],
                              text="None",
                              title="NoteDesigner",
                              font=Font.normal_text,
                              to="Locals.project_noteDesigner"
                              ),
               Button((440, 560), (400, 100), "CREATE",
                      this_state=STATES["INFO"],
                      text="Back",
                      font=Font.normal_text,
                      to="Locals.state"
                      ),
               Button((440, 360), (400, 100), "LOAD",
                      this_state=STATES["CREATE"],
                      text="Start",
                      font=Font.normal_text,
                      to = "Locals.state"
                      ),
               Button((440, 460), (400, 100), "HOME",
                      this_state=STATES["CREATE"],
                      text="Back",
                      font=Font.normal_text,
                      to="Locals.state"
                      ),
               FunctionButton((440, 160), (400, 100), createNewProject,
                              this_state=STATES["HOME"],
                              text="Create new project",
                              font=Font.normal_text,
                              to="Locals.state"
                              )
               ]


def checkState(state):
    return Locals.state == Locals.STATES[state]

def changeState(state):
    Locals.state = Locals.STATES[state]

def button_main():
    for button in Locals.buttons:
        button.draw(canvas, Locals.state)

def set_arrow(time, dire, arrow=None):
    print(dire)
    if not arrow == None:
        Locals.arrows.append(arrow)
    else:
        Locals.arrows.append(Arrow(Locals.mode, arrow_img[dire], time, dire))

def draw_arrow():
    for arrow in Locals.arrows:
        arrow.draw(Locals.scaleTimes, canvas, Locals.thisTime/1000, Locals.deHighLight)

        if Locals.startIndexFlag:
            arrow.if_highLight = False
        if Locals.editFloor >= 1:
            arrow.if_highLight = False

        if not Locals.highLightArrows == []:
            if Locals.editFloor >= 1 and Locals.highLightArrows[Locals.editChoose] == arrow:
                arrow.if_highLight = True




def move_arrow():
    global aHOLD,dHOLD
    if not Locals.editFloor == 2:
        return
    if aHOLD:
        Locals.highLightArrows[Locals.editChoose].time -= Locals.moveSpeed / 1000
    elif dHOLD:
        Locals.highLightArrows[Locals.editChoose].time += Locals.moveSpeed / 1000

def arrow_list_empty():
    Locals.arrows = []

def leftMove():
    Locals.thisTime -= Locals.moveSpeed

def rightMove():
    Locals.thisTime += Locals.moveSpeed


def highLightArrow():
    global lastArrowList
    if Locals.startIndexFlag:
        Locals.highLightArrows.clear()
        return
    for arrow in Locals.arrows:
        if arrow.if_highLight:
            arrow.drawHighLight(canvas)
            if not arrow in Locals.highLightArrows:
                Locals.highLightArrows.append(arrow)
        elif Locals.editFloor == 0:
            try:
                Locals.highLightArrows.remove(arrow)
            except:
                pass
    arrowInOrder(Locals.highLightArrows)

def drawBlank():
    for i in range(0, len(Locals.highLightArrows)):
        arrow = Locals.highLightArrows[i]
        arrow.draw_pos(canvas, (WIDTH - 50, 20 + i * 50))
        renderText(str(round(arrow.time, 2)), (WIDTH - 100, 20 + i * 50), canvas, leftLine=True)
    if Locals.editFloor == 1:
        drawBlank1()
    elif Locals.editFloor == 2:
        drawBlank1((255, 0, 0))
        drawBlank2()

def drawBlank1(color=(255, 255, 255)):
    if not len(Locals.highLightArrows) == 0:
        rect = Locals.highLightArrows[Locals.editChoose].img.get_rect()
        rect.move_ip(WIDTH - 50, 20 + Locals.editChoose * 50)
        pygame.draw.rect(canvas, color, rect, width=1)

editBackGround = pygame.Surface((200, 50))
editBackGround.fill((25,25,112))
def drawBlank2():
    # canvas.blit(editBackGround, ((WIDTH - 200 - editBackGround.get_width(),20 + Locals.editChoose * 50)))
    pass


def arrowInOrder(list, forSave=False):
    #冒泡排序
    if Locals.editFloor > 1 and not forSave:
        return
    length = len(list)
    for i in range(length - 1, -1, -1):
        for j in range(0, i):
            if list[j].time > list[j + 1].time:
                vartemp = list[j]
                list[j] = list[j + 1]
                list[j + 1] = vartemp


def save(exit=False):
    pygame.display.set_caption(Locals.thisCaption)
    # var = tkinter.filedialog.askopenfilename(title="选择谱面要使用的音乐",
    #                                          initialdir="E:/",
    #                                          filetypes=[("*MP3", ".mp3")]
    #
    #                                          )
    if exit:
        if tkinter.messagebox.askyesno("警告", "是否保存"):
            if not Locals.textPath:
                Locals.textPath = "./notes/autoSaves/AutoSave{0}.ehinote".format(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime()))
            else:
                save(exit)
                return
        else:
                return
    else:
        if not Locals.textPath:
            Locals.textPath = tkinter.filedialog.asksaveasfilename(title="选择保存谱面文件的位置",
                                                        filetypes=[("*EHINOTE", ".ehinote")],
                                                        initialdir = "./notes",
                                                        initialfile = "Untitled.ehinote"
                                                        )
            if tkinter.messagebox.askyesno("警告", "是否保存"):
                save(exit)
                return
            else:
                return

    arrowInOrder(Locals.arrows, forSave=True)
    with open(Locals.textPath, "w", encoding="UTF-8") as file:
        strGoingSave = ""
        for i in range(-1, len(Locals.arrows)):
            if i == -1:
                pathSplited = Locals.project_music_road.split("/")
                coverPathSplited = Locals.project_cover_road.split("/")
                songPath = "{0}/{1}/{2}".format(pathSplited[-3], pathSplited[-2], pathSplited[-1])
                coverPath = "{0}/{1}/{2}/{3}".format(coverPathSplited[-4], coverPathSplited[-3], coverPathSplited[-2], coverPathSplited[-1])
                author = Locals.project_author
                noteDesigner = Locals.project_noteDesigner
                line = "name : {0}\nlittleName : {1}\npath : {2}\ncover : {3}\nauthor : {4}\nnoteDesigner : {5}\n".format(Locals.project_name, Locals.project_littleName, songPath, coverPath, author, noteDesigner)
            else:
                arrow = Locals.arrows[i]
                line = "    ({0}, {1})\n".format(arrow.dire, round(arrow.time, 3))
            strGoingSave += line
        file.write(strGoingSave)

def load(path):
    arrow_list_empty()
    if path == "":
        return False
    with open(path, "r", encoding="UTF-8") as file:
        i = 0
        for line in file:
            if i == 0:
                Locals.project_name = infoHandle(line)
            elif i == 1:
                Locals.project_littleName = infoHandle(line)
            elif i == 2:
                Locals.project_music_road  = infoHandle(line)
            elif i == 3:
                Locals.project_cover_road = infoHandle(line)
            elif i == 4:
                Locals.project_author = infoHandle(line)
            elif i == 5:
                Locals.project_noteDesigner = infoHandle(line)
            else:
                data = eval(dataHandle(line))
                set_arrow(data[1], data[0])
            i += 1
    Locals.textPath = path
    return True

def infoHandle(resourse):
    result = resourse.split(":")[-1]
    result = result.rstrip()
    result = result.lstrip()
    return result


def dataHandle(resourse):
    result = resourse.rstrip()
    result = result.lstrip()
    return result

def beforeIndex():
    Locals.history.empty()
    Locals.history.append(Locals.arrows.copy())
    print (Locals.history.index)
    pygame.mixer.music.load(Locals.project_music_road)
    document = MP3(Locals.project_music_road)
    Locals.thisSongLong = document.info.length
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.play(start=50.0)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.pause()
    Locals.thisCaption = Locals.project_name
    pygame.display.set_caption(Locals.project_name)

def control():
    if shouldBeRecored:
        pygame.display.set_caption(Locals.thisCaption + "*")
    if checkState("HOME"):
        Locals.backGround.draw(canvas)
        button_main()
    elif checkState("OPEN"):
        if load(askForData()):
            beforeIndex()
            changeState("INDEX")
        else:
            changeState("HOME")
    elif checkState("CREATE") or checkState("INFO"):
        Locals.backGround.draw(canvas)
        button_main()
    elif checkState("LOAD"):
        arrow_list_empty()
        beforeIndex()
        changeState("INDEX")
    elif checkState("INDEX"):
        if LEFT_HOLD:
            leftMove()
        if RIGHT_HOLD:
            rightMove()
        move_arrow()
        if Locals.startIndexFlag:
            Locals.thisTime = pygame.mixer.music.get_pos() - MUSIC_OFFSET
        if Locals.thisTime < 0:
            Locals.thisTime = 0
        elif Locals.thisTime > Locals.thisSongLong * 1000:
            Locals.thisTime = Locals.thisSongLong * 1000
        Locals.backGround.draw(canvas)
        canvas.blit(middleLine, (0, HEIGHT / 2))
        canvas.blit(TimeLine, (WIDTH / 2, 0))
        draw_arrow()
        highLightArrow()
        drawBlank()
        renderText(str(Locals.thisTime), (0, 0), canvas)
        renderText(str(pygame.mixer.music.get_pos()), (0, 50), canvas)
        if LEFT_HOLD:
            renderText("LEFT_HOLD", (0, 100), canvas)
        elif RIGHT_HOLD:
            renderText("RIGHT_HOLD", (0, 100), canvas)
        elif aHOLD:
            renderText("a_HOLD", (0, 100), canvas)
        elif dHOLD:
            renderText("d_HOLD", (0, 100), canvas)
        # print(pygame.mixer.music.get_endevent())
    elif checkState("QUIT"):
        pygame.quit()
        # version = easygui.choicebox("选择要打开的版本", "版本选择", os.listdir("../beta_version"))
        os.system("python eightDirection.py")
        sys.exit()


while True:

    last_fps_time = Locals.clock.tick(Locals.fps)

    handleEvent()

    control()
    # renderText(str(Locals.history.history), (0, 400), canvas, font=Font.small_normal_text)

    pygame.display.update()


