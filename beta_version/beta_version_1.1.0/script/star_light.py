import time,pygame
from script.packs.item_foundation import Font,writeText,ifDoAction
from sprite import Sprite


class Star_light():
    def __init__(self,hero,sprite,canvas):
        # self.name = name
        # self.type = type
        # self.img = img
        self.lastTime = 0
        self.cd = 30
        self.time = 15
        self.can_use = False
        self.is_using = False
        self.if_auto = True
        self.hero = hero
        self.canvas = canvas
        self.time_left_color = (255, 0, 0)
        self.sprite = sprite
        self.star_light_effect = Sprite(self.canvas,self.sprite,50,50)
        self.hero_defeat_normal = 0
    def buff(self):
        self.hero.defeat += 1
        self.hero_defeat_normal = self.hero.defeat
    def skill_main(self):
        if self.if_auto:
            if self.is_using:
                self.using()
                writeText("skill", (0, 400), (0, 255, 0), Font.text, self.canvas)

            elif self.can_use or self.intertal():
                self.can_use = False
                self.is_using = True
                self.use_skill()
            else:
                self.hero.defeat = self.hero_defeat_normal
                self.star_light_effect.animation(640 - 25, 360 - 25,1,1,1, 6, "over")
            self.time_left = time.time() - self.lastTime
            writeText(str(round(self.time_left, 1)), (0, 350), self.time_left_color, Font.text, self.canvas)
        else:
            writeText("施工中，非自动技能暂无法释放",(0,400),(0,255,0),Font.text,self.canvas)
    def use_skill(self):
        print("skill")

        self.hero.defeat += 2
        self.hero.defeat = self.hero.defeat * 1.25
    def intertal(self):
        self.time_left_color = (255, 0, 0)
        if self.lastTime == 0:
            self.lastTime = time.time()
            return False
        if not ifDoAction(self.lastTime,self.cd):
            return False
        self.lastTime=time.time()
        return True
    def using(self):
        self.time_left_color = (255, 255, 0)
        self.star_light_effect.animation(640 - 25, 360 - 25,1,1,1,6,"running")
        if self.lastTime == 0:
            self.lastTime = time.time()
            return False
        if not ifDoAction(self.lastTime, self.time):
            return
        self.lastTime = time.time()
        self.is_using = False
        self.hero.defeat = 0

