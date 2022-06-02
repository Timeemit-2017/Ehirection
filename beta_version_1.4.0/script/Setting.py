import pygame, time
from pygame.locals import *


class SettingVar():
    font_load = "ttfs/noto/NotoSansHans-Light.otf"
    font_size = 50
    font_color = (255, 255, 255)
    font = 0
    times = 20
    keys_default = {"yellow_up": K_UP, "yellow_right": K_RIGHT, "yellow_down": K_DOWN, "yellow_left": K_LEFT,
                    "songc_up": K_UP, "songc_down": K_DOWN,
                    "itemc_develop": K_RSHIFT, "itemc_back": K_RSHIFT, "itemc_up": K_UP, "itemc_right": K_RIGHT,
                    "itemc_down": K_DOWN, "itemc_left": K_LEFT,
                    "lobby_left": K_LEFT, "lobby_right": K_RIGHT,
                    "game_exit": K_F1, "switch_message": K_m,
                    "start_indexDesigner": K_F2
                    }
    keys = keys_default
    bools_default = {"if_message": False, "setting_style": False, "if_full_screen": False}
    bools = bools_default
    blanks_default = {"email": "*custom"}
    blanks = blanks_default
    choosing_default = {"songchoose_distance": ["HEIGHT_2", "HEIGHT", "*custom"], "screen_size": ["*system"]}
    choosing = choosing_default

class Setting:
    def __init__(self, video_size, orginDisplayType):
        self.page = 0
        self.settings = []
        self.setting_index = 0
        self.image_index = 0
        self.pictures = []
        self.pictures_resourse = []
        self.video_size = video_size
        self.lastTime = 0
        self.interval = 0.5
        SettingVar.font = pygame.font.Font(SettingVar.font_load, SettingVar.font_size)
        self.changeDisplayType(orginDisplayType)
        self.space = 40
        self.moveSpace = 50
        self.up = 40 #上边距
        self.down = 40 #下边距
        self.textHeight = 0
        self.position_orgin = []
        self.sets = []
        # self.position = None
        # self.position_ratio = None
        for i in range(0, 4):
            image_resourse = pygame.image.load("images/setting/main" + str(i) + ".png")
            image = pygame.transform.scale(image_resourse, (64 * SettingVar.times, 36 * SettingVar.times))
            self.pictures_resourse.append(image_resourse)
            self.pictures.append(image)

    def changeDisplayType(self, target):
        if target == "Old":
            self.position = [8 * SettingVar.times, 8 * SettingVar.times]
        else:
            self.position = [8 * SettingVar.times, 1 * SettingVar.times]
        self.position_ratio = [self.position[0] / self.video_size[0], self.position[1] / self.video_size[1]]

    def draw(self, canvas, mousePos="Old"):
        if mousePos == "Old":
            self.drawBg(canvas)
            self.getSet(self.setting_index).draw(canvas, self.position, self.position_orgin)
        else:
            offset = 0
            for i in range(len(self.settings)):
                for j in range(len(self.settings[i])):
                    self.settings[i][j].draw(canvas,
                          (self.position[0], self.position[1] + (offset + j) * (self.space + self.textHeight)),
                          self.position_orgin,
                          mousePos
                          )
                offset += len(self.settings)
        # self.settings[self.setting_index].draw(canvas, self.position)

    def drawButton(self, canvas):
        pass

    def step(self, dire, HEIGHT):
        # dire为-1, 向上， 为1， 向下
        pos1 = self.getSet(0).pos[1] + dire * self.moveSpace
        pos2 = self.getSet(-1).pos[1] + dire * self.moveSpace
        if pos1 > self.up:
            self.position[1] = self.up
            return "已到顶部 pos1:" + str(pos1)
        elif pos2 < HEIGHT - self.down - self.textHeight:

            self.position[1] = HEIGHT - self.down - (self.getAllLength()) * (self.space + self.textHeight)
            return "已到底部 pos2:" + str(pos2)
        else:
            self.position[1] = pos1

    def drawBg(self, canvas):
        canvas.blit(self.pictures[self.image_index], (0, 0))

    def backGroundSwitch(self):
        if not self.ifDoAction(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        self.image_index += 1
        if self.image_index >= len(self.pictures):
            self.image_index = 0

    def setting_index_switch(self, dire):
        self.setting_index += dire * 1
        if self.setting_index >= self.getAllLength():
            self.setting_index = 0
        elif self.setting_index < 0:
            self.setting_index = self.getAllLength() - 1

    def ifDoAction(self, lastTime, interval):
        if lastTime == 0:
            return True
        currectTime = time.time()
        return currectTime - lastTime >= interval

    def change_scale(self, screen_size):
        for i in range(0, 4):
            self.pictures[i] = pygame.transform.scale(self.pictures_resourse[i], (screen_size))
        self.position[0] = screen_size[0] * self.position_ratio[0]
        self.position[1] = screen_size[1] * self.position_ratio[1]
        self.position_orgin = self.position.copy()  # bug:这里虽然有这一个变量，但是没有作用。
        print(self.position_orgin)
        self.up = self.position[1]
        self.down = self.position[1]
        for set in self.settings:
            if hasattr(set, "button"):
                set.button.x = screen_size[0] * set.button.pos_ratio[0]
                set.button.y = screen_size[1] * set.button.pos_ratio[1]

    def load_settings(self, settingType):
        with open("data/settings.txt", encoding="UTF-8") as file:
            i = 0
            for line in file:
                if i == 0:
                    setting = eval(line.rstrip())
                elif i == 1:
                    key_set_titles = eval(line.rstrip())
                elif i == 2:
                    bool_sets = eval(line.rstrip())
                elif i == 3:
                    bool_sets_titles = eval(line.rstrip())
                elif i == 4:
                    str_sets = eval(line.rstrip())
                elif i == 5:
                    str_sets_titles = eval(line.rstrip())
                elif i == 6:
                    choosing_sets = eval(line.rstrip())
                elif i == 7:
                    choosing_sets_titles = eval(line.rstrip())
                i += 1
        for j in range(int(i / 2)):
            self.settings.append([])
        SettingVar.keys = setting
        i = 0
        for key in SettingVar.keys:
            temp = KeySet(key_set_titles[i], key, settingType, self.video_size)
            self.settings[0].append(temp)
            self.sets.append(temp)
            i += 1
        print(self.settings[0])
        self.settings[0][0].textRender()
        self.textHeight = self.settings[0][0].text.get_height()

    def mainBeforeDie(self, canvas):
        for i in range(len(self.settings)):
            for set in self.settings[i]:
                set.textRender()
        self.drawBg(canvas)

    def mainAfterDie(self, canvas, mousePos):
        self.draw(canvas, mousePos)
        self.backGroundSwitch()

    def main_old(self, canvas):
        for i in range(len(self.settings)):
            for set in self.settings[i]:
                set.textRender()
        self.draw(canvas)
        self.backGroundSwitch()

    def getSet(self, index):
        # temp = []
        # for i in range(len(self.settings)):
        #     for set in self.settings[i]:
        #         temp.append(set)
        # return temp[index]
        return self.sets[index]

    def getAllLength(self):
        # length = 0
        # for i in range(len(self.settings)):
        #     length += len(self.settings[i])
        # return length
        return len(self.sets)


class Set(object):
    def __init__(self, title, target, screen_size):
        self.title = title
        self.target = target
        self.attribute = 0
        self.number = 0
        self.text = 0
        self.pos = (0, 0)

    def textRender(self):
        self.text = SettingVar.font.render(self.title, True, SettingVar.font_color)

    def pack(self):
        self.textRender()

    def set(self, target_dict):
        target_dict[self.target] = self.attribute

    def set_attribute(self, target_dict):
        self.attribute = target_dict[self.target]

    def ifDoAction(self, lastTime, interval):
        if lastTime == 0:
            return True
        currectTime = time.time()
        return currectTime - lastTime >= interval

    def draw(self, canvas, position, position_orgin, mousePos=(0, 0)):
        self.pos = position
        canvas.blit(self.text, self.pos)


class KeySet(Set):
    def __init__(self, title, target, button_type, screen_size):
        Set.__init__(self, title, target, screen_size)
        self.set_attribute(SettingVar.keys)
        self.button = KeySetButton(button_type, screen_size)
        self.lastTime = 0
        self.interval = 0.3
        self.key_text_resourse = pygame.key.name(self.attribute)
        self.key_text_resourse_state = False
        self.select = False
        self.pos = (0, 0)

    def input(self, key):
        self.attribute = key
        self.set(SettingVar.keys)
        self.is_setting = True
        if self.key_text_resourse_state:
            self.key_text_resourse = pygame.key.name(self.attribute) + "_"
        else:
            self.key_text_resourse = pygame.key.name(self.attribute)


    def select_anime(self):
        if not self.select:
            self.key_text_resourse = pygame.key.name(self.attribute)
            return
        if not self.ifDoAction(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        if self.key_text_resourse_state:
            self.key_text_resourse = pygame.key.name(self.attribute) + "_"
            self.key_text_resourse_state = False
        else:
            self.key_text_resourse = pygame.key.name(self.attribute)
            self.key_text_resourse_state = True

    def textRender(self):
        self.select_anime()
        self.text = SettingVar.font.render(self.title, True, SettingVar.font_color)
        self.key_text = SettingVar.font.render(self.key_text_resourse, True, SettingVar.font_color)

    def checkRange(self, x, y):
        return self.button.checkRange(x, y)

    def draw(self, canvas, position, position_orgin, mousePos="Old"):
        text_size = self.text.get_size()
        key_text_size = self.key_text.get_size()
        if mousePos == "Old":
            self.pos = (position_orgin[0], position_orgin[1] + text_size[1] / 2)
            self.button.draw(canvas, is_setting=self.select)
        else:
            self.pos = (position[0], position[1] + text_size[1] / 2)
            self.button.draw(canvas, (self.pos[0] + 740, self.pos[1]), mousePos, is_setting=self.select)
        canvas.blit(self.text, self.pos)
        canvas.blit(self.key_text, (self.button.x + self.button.width / 2 - key_text_size[0] / 2,
                                    self.button.y + self.button.height / 2 - key_text_size[1] / 2 - 4))


class KeySetButton:
    def __init__(self, type, screen_size):
        times = SettingVar.times
        self.smallImg = pygame.transform.scale(pygame.image.load("images/setting/buttons/small_button.png"), (9 * times, 4 * times))
        self.smallIsSetting = self.smallImg.copy()
        self.bigImg = pygame.transform.scale(pygame.image.load("images/setting/buttons/big_button.png"), (16 * times, 6 * times))
        self.bigIsSetting = self.bigImg.copy()

        shade_strength = 75
        s = shade_strength
        for y in range(4 * times):
            for x in range(9 * times):
                r, g, b, a = tuple(self.smallIsSetting.get_at((x, y)))
                self.smallIsSetting.set_at((x, y), (r - s / 2, g - s / 2, b - s))
        for y in range(6 * times):
            for x in range(16 * times):
                r1, g1, b1, a1 = tuple(self.bigIsSetting.get_at((x, y)))
                self.bigIsSetting.set_at((x, y), (r1 - s / 2, g1 - s / 2, b1 - s))
        self.alpha = 0

        self.type = None
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.pos_ratio = None
        self.img = None
        self.img_is_settting = None
        self.reset(type, screen_size)

    def changeType(self, target, screen_size):
        if target == "Old":
            target = "big"
        else:
            target = "small"
        self.reset(target, screen_size)

    def reset(self, type, screen_size):
        self.type = type
        if type == "small" or not type:
            self.img = self.smallImg
            self.img_is_settting = self.smallIsSetting
            self.x = 51
            self.y = 10
            self.width = 9
            self.height = 4
        elif type == "big" or type:
            self.img = self.bigImg
            self.img_is_settting  = self.bigIsSetting
            self.x = 42
            self.y = 8
            self.width = 16
            self.height = 6
        times = SettingVar.times
        self.x *= times
        self.y *= times
        self.width *= times
        self.height *= times
        self.pos_ratio = (self.x / screen_size[0], self.y / screen_size[1])

    def draw(self, canvas, pos="Old", mousePos="Old", is_setting=False):
        if pos == "Old" and mousePos == "Old":
            if is_setting:
                canvas.blit(self.img_is_settting, (self.x, self.y))
                return
            canvas.blit(self.img, (self.x, self.y))
        else:
            self.x = pos[0]
            self.y = pos[1]
            if is_setting:
                canvas.blit(self.img_is_settting, (self.x, self.y))
                return
            if self.checkRange(mousePos[0], mousePos[1]):
                self.alpha += 25
                if self.alpha >= 255:
                    self.alpha = 255
                    canvas.blit(self.img, pos)
                    return
            else:
                self.alpha = 122
            surface_under = pygame.Surface((self.img.get_width(), self.img.get_height()), SRCALPHA).convert()
            surface_under.blit(self.img, (0, 0))
            surface_under.set_alpha(self.alpha)
            canvas.blit(surface_under, pos)

    def checkRange(self, x, y):
        return self.x < x < self.x + self.width and \
               self.y < y < self.y + self.height


class ChooseSetButton(KeySetButton):
    def __init__(self, buttontype, screen_size):
        KeySetButton.__init__(self, buttontype, screen_size)


class ValueSetButton(KeySetButton):
    def __init__(self, buttontype, screen_size):
        KeySetButton.__init__(self, buttontype, screen_size)
