import pygame
from script.basic import *

pygame.init()


class SongChoose:
    def __init__(self, cph, SIZE, canvas):
        HEIGHT = SIZE[1]
        HEIGHT_2 = HEIGHT / 2
        self.cph = cph  # 唱片环图片
        self.cphSize = self.cph.get_size()
        self.cphWidth = self.cphSize[0]
        self.cphWidth_2 = self.cphSize[0] / 2
        self.cphHeight = self.cphSize[1]
        self.cphHeight_2 = self.cphSize[1] / 2
        self.imgs = []
        self.imgs_road = []
        # 三个唱片
        self.record_dis = self.cphHeight + 100  # 两个唱片之间的距离
        if self.record_dis < self.cphHeight:
            self.record_dis = self.cphHeight
        self.recordMain_orgin = (0, 0)  # record_main的初始位置
        self.record_m = Record(self.cph, None)  # 中间的唱片
        self.record_u = Record(self.cph, None)  # 上方的唱片
        self.record_d = Record(self.cph, None)  # 下方的唱片
        self.record_uu = Record(self.cph, None)  # 上方的上方的唱片
        self.record_dd = Record(self.cph, None)  # 下方的下方的唱片
        self.records = {"uu": self.record_uu, "up": self.record_u, "main": self.record_m,
                        "down": self.record_d, "dd": self.record_dd}  # 唱片字典
        self.number = 0  # 封面索引
        self.speed = 0  # 移动速度
        self.dire = False  # 此时的运动方向 False表向下移动，往上切换谱面
        self.life = 0
        self.start = False
        # 描述
        self.info_name = []
        self.info_time = []
        self.info_little_name = []
        self.info_thisLittleName = ""
        self.info_thisName = ""
        self.info_thisTime = ""
        self.info_pass = False
        self.info_x = 300
        self.info_y = 95
        self.canvas = canvas

    def recordInit(self, SIZE, localNumber=0):
        WIDTH_2 = SIZE[0] / 2
        HEIGHT_2 = SIZE[1] / 2
        records_set = [self.record_uu, self.record_u, self.record_m, self.record_d, self.record_dd]
        for i in range(0, len(records_set)):
            rec = records_set[i]
            this_pos = (WIDTH_2 - self.cphWidth_2, HEIGHT_2 - self.cphHeight_2 - (2- i) * self.record_dis)
            rec.set_pos(this_pos)
            index = localNumber - 2 + i
            if index > len(self.imgs) - 1:
                index = index - len(self.imgs)
            rec.changeCover(self.imgs[index])
            if i == 2:
                self.recordMain_orgin = this_pos

    def recordDraw(self):
        for record in self.records:
            self.records[record].draw(self.canvas)

    def changeNumber(self, dire):
        dire = turnInt(dire)
        self.number += dire

    def checkNumber(self):
        if self.number < 0:
            self.number = len(self.imgs) - 1
        elif self.number > len(self.imgs) - 1:
            self.number = 0

    def set(self, SIZE, ifCleanSpeed=True):
        if ifCleanSpeed:
            self.speed = 0
        self.recordInit(SIZE, self.number)

    def forceControl(self, last_fps_time, acceleration=50, maxSpeed=70):
        self.speed = self.speed + acceleration * last_fps_time / 1000
        if self.speed > maxSpeed:
            self.speed = maxSpeed
        return self.speed

    def recordUpdate(self):
        # 使除了uuRecord，其余的record跟随uu的方法
        records_set = [self.record_u, self.record_m, self.record_d, self.record_dd]
        for i in range(len(records_set)):
            rec = records_set[i]
            rec.set_pos((self.record_uu.pos[0], self.record_uu.pos[1] + (i + 1) * self.record_dis))

    def recordStep(self, dire, last_fps_time):
        dire = -turnInt(dire)
        self.records["uu"].set_pos(plus=(0, dire * self.forceControl(last_fps_time)))
        self.recordUpdate()

    def recordCheck(self, SIZE):
        HEIGHT_2 = SIZE[1] / 2
        if self.records["main"].pos[1] < HEIGHT_2 - self.cphHeight_2 - self.record_dis or self.records["main"].pos[1] > HEIGHT_2 - self.cphHeight_2 + self.record_dis:
            # GameVar.messageControl.message_summon("System", str(self.record_m.pos) + " 判定时")
            list_temp = []
            for rec in self.records:
                list_temp.append(self.records[rec])
            print(list_temp)
            if self.dire:
                temp = list_temp[0]
                list_temp[0] = list_temp[-1]
                list_temp.insert(1, temp)
                list_temp.pop(-1)
            else:
                temp = list_temp[-1]
                list_temp[-1] = list_temp[0]
                list_temp.insert(-1, temp)
                list_temp.pop(0)
            resource = ["uu", "up", "main", "down", "dd"]
            for i in range(0, len(resource)):
                self.records[resource[i]] = list_temp[i]
            self.record_uu = self.records["uu"]
            self.record_u = self.records["up"]
            self.record_m = self.records["main"]
            self.record_d = self.records["down"]
            self.record_dd = self.records["dd"]
            self.changeNumber(self.dire)
            self.checkNumber()
            self.info_update()
            self.set(SIZE, ifCleanSpeed=False)

    def checkMiddle(self):
        # 检测record_main是否已经超过中间，是的话直接切换下一个
        if self.dire:
            if self.record_m.pos[1] < self.recordMain_orgin[1] - self.cphHeight / 2:
                self.changeNumber(self.dire)
                self.checkNumber()
                self.info_update()
        else:
            if self.record_m.pos[1] > self.recordMain_orgin[1] + self.cphHeight / 2:
                self.changeNumber(self.dire)
                self.checkNumber()
                self.info_update()

    def checkLife(self):
        # 检测生命值是不是低于等于0
        if self.life <= 0:
            self.start = False
            self.life = 0

    def infoInit(self):
        i = 0
        # 旧谱面导入
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

    def info(self):
        self.draw_info()

    def info_update(self):
        self.info_thisName = self.info_name[self.number]
        self.info_thisLittleName = self.info_little_name[self.number]
        self.info_thisTime = self.info_time[self.number]

    def draw_info(self):
        writeText(self.info_thisName, (self.info_x - 5, self.info_y), self.canvas, (255, 255, 255), 255, Font.song_name)
        writeText(self.info_thisLittleName, (self.info_x, self.info_y + 100), self.canvas, (255, 255, 255), 255, Font.text)
        writeText("时长：" + self.info_thisTime, (self.info_x, self.info_y + 150), self.canvas, (255, 255, 255), 255,
                  Font.little_text)

    def set_imgs(self):
        # with open("data/songs.txt", encoding="gbk") as file:
        #     for line in file:
        #         self.imgs_road = eval(line.rstrip())
        #         break
        basic_road = "images/start/songs/"
        for img_road in self.imgs_road:
            self.imgs.append(pygame.image.load(basic_road + img_road).convert())

    def draw(self, if_message):
        self.recordDraw()
        if if_message:
            pygame.draw.rect(self.canvas, (255, 255, 255), (self.record_m.pos[0], self.record_m.pos[1], 360, 360), width=1)
            pygame.draw.rect(self.canvas, (255, 0, 255), (self.record_uu.pos[0], self.record_uu.pos[1], 360, 360), width=1)
            pygame.draw.rect(self.canvas, (255, 0, 0), (self.record_u.pos[0], self.record_u.pos[1], 360, 360), width=1)
            writeText("Record_Main: " + str(self.record_m.pos), (0, 300), self.canvas)
            writeText("SongChoose.start: " + str(self.start), (0, 50), self.canvas)

    def init(self, SIZE):
        self.set(SIZE)
        self.info_update()

    def step(self, SIZE, last_fps_time):
        self.recordStep(self.dire, last_fps_time)
        self.recordCheck(SIZE)

    def main(self, SIZE, last_fps_time, if_message):
        # 主函数
        if self.start:
            self.step(SIZE, last_fps_time)
        else:
            self.set(SIZE)
        self.draw(if_message)
        self.info()


class Record:
    def __init__(self, cph, cover):
        self.cph = cph
        if not cover is None:
            self.cover = pygame.transform.scale(cover, (250, 250))
        else:
            self.cover = None
        self.pos = (0, 0)

    def set_pos(self, target=None, plus=None):
        if plus is None:
            self.pos = target
        else:
            self.pos = (self.pos[0] + plus[0], self.pos[1] + plus[1])

    def changeCover(self, target):
        self.cover = pygame.transform.scale(target, (250, 250))

    def draw(self, canvas):
        canvas.blit(self.cover, (self.pos[0] + 55, self.pos[1] + 55))
        canvas.blit(self.cph, self.pos)


def turnInt(target):
    if target:
        return 1
    else:
        return -1
