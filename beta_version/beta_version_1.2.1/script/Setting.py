import pygame,time
from pygame.locals import *
class SettingVar():
    font_load = "ttfs/noto/NotoSansHans-Light.otf"
    font_size = 50
    font_color = (255,255,255)
    font = 0
    times = 20
    keys_default = {"yellow_up": K_UP, "yellow_right": K_RIGHT, "yellow_down": K_DOWN, "yellow_left": K_LEFT,
            "songc_up": K_UP,"songc_down": K_DOWN,
            "itemc_develop":K_RSHIFT, "itemc_back":K_RSHIFT, "itemc_up": K_UP, "itemc_right": K_RIGHT, "itemc_down": K_DOWN,
            "lobby_left": K_LEFT, "lobby_right": K_RIGHT,
            "game_exit": K_F1, "switch_message":K_m
            }
    keys = keys_default

class Setting():
    def __init__(self, video_size):
        self.settings = []
        self.setting_index = 0
        self.image_index = 0
        self.pictures = []
        self.pictures_resourse = []

        self.lastTime = 0
        self.interval = 0.5
        SettingVar.font = pygame.font.Font(SettingVar.font_load, SettingVar.font_size)
        self.position = [8 * SettingVar.times, 8 * SettingVar.times]
        self.position_ratio = [self.position[0] / video_size[0], self.position[1] / video_size[1]]
        self.video_size = video_size
        for i in range(0, 4):
            image_resourse = pygame.image.load("images/setting/main" + str(i) + ".png")
            image = pygame.transform.scale(image_resourse, (64 * SettingVar.times, 36 * SettingVar.times))
            self.pictures_resourse.append(image_resourse)
            self.pictures.append(image)
    def draw(self,canvas):
        self.drawBg(canvas)
        self.settings[self.setting_index].draw(canvas, self.position)
    def drawBg(self, canvas):
        canvas.blit(self.pictures[self.image_index], (0,0))
    def backGroundSwitch(self):
        if not self.ifDoAction(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        self.image_index += 1
        if self.image_index >= len(self.pictures):
            self.image_index = 0
    def setting_index_switch(self,dire):
        self.setting_index += dire * 1
        if self.setting_index >= len(self.settings):
            self.setting_index = 0
        elif self.setting_index < 0:
            self.setting_index = len(self.settings) - 1
    def ifDoAction(self,lastTime, interval):
        if lastTime == 0:
            return True
        currectTime = time.time()
        return currectTime - lastTime >= interval
    def change_scale(self, screen_size):
        for i in range(0,4):
            self.pictures[i] = pygame.transform.scale(self.pictures_resourse[i], (screen_size))
        self.position[0] = screen_size[0] * self.position_ratio[0]
        self.position[1] = screen_size[1] * self.position_ratio[1]
        for set in self.settings:
            if hasattr(set,"button"):
                set.button.x = screen_size[0] * set.button.pos_ratio[0]
                set.button.y = screen_size[1] * set.button.pos_ratio[1]
    def load_settings(self):
        with open("data/settings.txt", encoding="UTF-8") as file:
            i = 0
            for line in file:
                if i == 0:
                    setting = eval(line.rstrip())
                elif i == 1:
                    key_set_titles = eval(line.rstrip())
                i += 1
        SettingVar.keys = setting
        i = 0
        for key in SettingVar.keys:
            self.settings.append(KeySet(key_set_titles[i],key,True,self.video_size))
            i += 1
    def main(self,canvas):
        for set in self.settings:
            set.textRender()
        self.draw(canvas)
        self.backGroundSwitch()

class Set(object):
    def __init__(self,title,target,screen_size):
        self.title = title
        self.target = target
        self.attribute = 0
        self.number = 0
        self.text = 0
    def textRender(self):
        self.text = SettingVar.font.render(self.title, True, SettingVar.font_color)
    def pack(self):
        self.textRender()
    def set(self,target_dict):
        target_dict[self.target] = self.attribute
    def set_attribute(self, target_dict):
        self.attribute = target_dict[self.target]
    def ifDoAction(self, lastTime, interval):
        if lastTime == 0:
            return True
        currectTime = time.time()
        return currectTime - lastTime >= interval
    def draw(self, canvas, position):
        canvas.blit(self.text, postion)

class KeySet(Set):
    def __init__(self, title, target, button_type, screen_size):
        Set.__init__(self,title,target,screen_size)
        self.set_attribute(SettingVar.keys)
        self.button = KeySetButton(button_type,screen_size)
        self.lastTime = 0
        self.interval = 0.3
        self.key_text_resourse = pygame.key.name(self.attribute)
        self.key_text_resourse_state = False
        self.select = False
    def input(self,key):
        self.attribute = key
        self.set(SettingVar.keys)
        if self.key_text_resourse_state:
            self.key_text_resourse = pygame.key.name(self.attribute) + "_"
        elif not self.key_text_resourse_state:
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
    def checkRange(self, x, y, width, height):
        return self.button.checkRange(x, y, width, height)
    def draw(self,canvas, position):
        text_size = self.text.get_size()
        key_text_size = self.key_text.get_size()
        self.button.draw(canvas)
        canvas.blit(self.text, (position[0], position[1]+ text_size[1] / 2))
        canvas.blit(self.key_text, (self.button.x + self.button.width/2 - key_text_size[0] / 2,
                                    self.button.y + self.button.height/2 - key_text_size[1] / 2 - 4))

class KeySetButton():
    def __init__(self,type,screen_size):
        self.type = type
        if self.type == "small" or self.type == False:
            self.img_resourse = pygame.image.load("images/setting/buttons/small_button.png")
            self.x = 51
            self.y = 10
            self.width = 9
            self.height = 4
        elif self.type == "big" or self.type == True:
            self.img_resourse = pygame.image.load("images/setting/buttons/big_button.png")
            self.x = 42
            self.y = 8
            self.width = 16
            self.height = 6
        times = SettingVar.times
        self.x = self.x * times
        self.y = self.y * times
        self.width = self.width * times
        self.height *= times
        self.pos_ratio = (self.x / screen_size[0], self.y / screen_size[1])
        self.img = pygame.transform.scale(self.img_resourse, (self.width, self.height))
    def draw(self,canvas):
        canvas.blit(self.img, (self.x, self.y))
    def checkRange(self, x, y, width, height):
        return x > self.x and x < self.x + self.width and \
               y > self.y and y < self.y + self.height


