import time,pygame
#from script.packs.item_foundation import Font,writeText,ifDoAction,Item
from sprite import Sprite
from pygame.locals import *
pygame.init()
def ifDoAction(lastTime, interval):
    if lastTime == 0:
        return True
    currectTime = time.time()
    return currectTime - lastTime >= interval

def textInit(size,font):
    font = pygame.font.Font(font, size)
    return font

def writeText(text, position, color, font,canvas):
    text = font.render(text, True, color)
    canvas.blit(text, position)

class Font():
    text = textInit(30,"ttfs/noto/NotoSansHans-Light.otf")
    score = textInit(40,"ttfs/noto/NotoSansHans-Light.otf")

#父类-------------------------------------------------------------------------------------------------------------------

class Item():
    def __init__(self,name,quality,description,img,GameVar):
        self.name = name
        self.quality = quality
        self.description = description
        self.img = img
        self.GameVar = GameVar
class Pendant(Item):
    def __init__(self,name,quality,description,img,GameVar,canvas,r_width,r_height,sprite="null"):
        Item.__init__(self,name,quality,description,img,GameVar)
        self.canvas = canvas
        self.sprite = sprite
        if not self.sprite == "null":
            self.effect = Sprite(self.canvas,self.sprite,r_width,r_height)
    def buff(self):
        pass

class Skill_P(Pendant):
    def __init__(self,name,quality,cd,time,if_auto,r_width,r_height,description,img,GameVar,canvas,sprite="null"):
        Pendant.__init__(self,name,quality,description,img,GameVar,canvas,r_width,r_height,sprite)
        self.cd = cd
        self.time = time
        self.if_auto = if_auto
        self.lastTime = 0
        self.time_left_color = (255, 0, 0)
        self.can_use = False
        self.is_using = False
        self.key_down = False
    def intertal(self):
        self.time_left_color = (255, 0, 0)
        if self.lastTime == 0:
            self.lastTime = time.time()
            return False
        if not ifDoAction(self.lastTime,self.cd):
            return False
        self.lastTime=time.time()
        return True
    def skill_time(self):
        if self.lastTime == 0:
            self.lastTime = time.time()
            return False
        if not ifDoAction(self.lastTime, self.time):
            return False
        self.lastTime = time.time()
        return True
    def check_key(self,key_num):
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == key_num:
                self.key_down = True
            else:
                self.key_down = False

class NonSkill_P(Pendant):
    def __init__(self,name,quality,description,img,GameVar,r_width,r_height,canvas):
        Pendant.__init__(self,name,quality,description,img,GameVar,r_width,r_height,canvas)

class Prop(Item):
    def __init__(self,name,quality,description,img,GameVar,canvas):
        Item.__init__(self,name,quality,description,img,GameVar)
        self.canvas = canvas

class Material(Item):
    def __init__(self,name,quality,description,img,GameVar):
        Item.__init__(self,name,quality,description,img,GameVar)

class Effect_M(Material):
    def __init__(self,name,quality,description,img,GameVar,canvas):
        Material.__init__(self,name,quality,description,img,GameVar)
        self.canvas = canvas

class NonEffect_M(Material):
    def __init__(self,name,quality,description,img,GameVar):
        Material.__init__(self,name,quality,description,img,GameVar)

#以下为单个物品---------------------------------------------------------------------------------------------------------

class Star_light(Skill_P):
    def __init__(self,GameVar,sprite,canvas):
        Skill_P.__init__(self,"Star_light","green",30,15,50,50,True,"None",pygame.image.load("images/items/ehi1st_/star_light.png"),GameVar,canvas,sprite)
        self.hero_defeat_normal = 0
    def buff(self):
        self.GameVar.hero.defeat += 1
        self.hero_defeat_normal = self.GameVar.hero.defeat
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
                self.GameVar.hero.defeat = self.hero_defeat_normal
                self.effect.animation(640 - 25, 360 - 25,1,1,1, 6, "over")
            self.time_left = time.time() - self.lastTime
            writeText(str(round(self.time_left, 1)), (0, 350), self.time_left_color, Font.text, self.canvas)
        else:
            writeText("施工中，非自动技能暂无法释放",(0,400),(0,255,0),Font.text,self.canvas)
    def use_skill(self):
        print("skill")
        self.GameVar.hero.defeat += 2
        self.GameVar.hero.defeat = self.GameVar.hero.defeat * 1.25
    def using(self):
        self.time_left_color = (255, 255, 0)
        self.effect.animation(640 - 25, 360 - 25,1,1,1,6,"running")
        if not self.skill_time():
            return
        self.is_using = False
        self.GameVar.hero.defeat = self.hero_defeat_normal

class Diamond(NonSkill_P):
    def __init__(self,GameVar,sprite,canvas):
        NonSkill_P.__init__(self,"Diamond","purple","None",pygame.image.load("images/items/ehi1st_/diamond.png"),GameVar,50,50,canvas)
    def buff(self):
        self.GameVar.enemy_damage = self.GameVar.enemy_damage * 2
        self.GameVar.score_to_coin = self.GameVar.score_to_coin * 0.8
    def skill_main(self):
        pass

class Apple(Skill_P):
    def __init__(self,GameVar,sprite,canvas):
        Skill_P.__init__(self,"Apple","blue",20,10,False,50,50,"None",pygame.image.load("images/items/ehi1st_/star_light.png"),GameVar,canvas)
        self.life_plus_lastTime = 0
        self.life_plus_interval = 1
        self.skill_start = 0
        self.skill_over = time.time()
    def skill_main(self):
        if self.can_use and self.GameVar.hero.is_button_press:
            self.is_using = True
            self.skill_start = time.time()
            time_left_ = "ready"
        elif self.is_using:
            self.using()
            if self.skill_time():
                self.is_using = False
                self.skill_over = time.time()
            self.time_left = time.time() - self.skill_start
            time_left_ = str(round(self.time_left, 1))
        else:
            if self.intertal():
                self.can_use = True
                time_left_ = "ready"
            else:
                self.can_use = False
                self.time_left_color = (255, 0, 0)
                self.time_left = time.time() - self.skill_over
                time_left_ = str(round(self.time_left, 1))

        writeText(time_left_, (0, 350), self.time_left_color, Font.text, self.canvas)
    def using(self):
        self.time_left_color = (255, 255, 0)
        if not ifDoAction(self.life_plus_lastTime, self.life_plus_interval):
            return
        self.life_plus_lastTime = time.time()
        self.GameVar.hero.life += 0.5
    def intertal(self):
        if self.skill_over == 0:
            return False
        if not ifDoAction(self.skill_over,self.cd):
            return False
        return True

class Bandage(Prop):
    def __init__(self, GameVar, sprite, canvas):
        Prop.__init__(self,"Bandage",3,"None",None,GameVar,canvas)

#物品的字典类
class Items():
    def __init__(self,gameVar,canvas):
        self.resource1st = pygame.image.load("images/items/ehi1st_/item_effect_sprite.png")
        self.star_light = Star_light(gameVar,self.resource1st,canvas)
        self.diamond = Diamond(gameVar,self.resource1st,canvas)
        self.apple = Apple(gameVar,self.resource1st,canvas)
        self.bandage = Bandage(gameVar,self.resource1st,canvas)
        self.list = [[self.star_light,0],[self.diamond,1],[self.apple,2],[self.bandage,2]]
    def get_item(self,id):
        return self.list[id][0]
