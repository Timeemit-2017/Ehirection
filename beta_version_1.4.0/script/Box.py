import pygame,random

from script.items import *
from pygame.locals import *
from script.Animation import *
from script.Pool import *
from script.Account_Item import *


pygame.init()

def checkCoin(coin, GameVar):
    return coin < GameVar.coin

# 创建是否到了画组件时间的方法
def ifDoAction(lastTime, interval):
    if lastTime == 0:
        return True
    currectTime = time.time()
    return currectTime - lastTime >= interval
def writeText(text, position, canvas, color=(255, 255, 255, 255), alpha=255, font=None, is_middle=False,is_right_bottom=None, move_pos=None):
    text = font.render(text, True, color)
    if is_middle:
        pos = (position[0] - text.get_width() / 2, position[1] - text.get_height() / 2)
        position = pos
    elif is_right_bottom != None:
        pos = (
        position[0] + is_right_bottom[0] - text.get_width(), position[1] + is_right_bottom[1] - text.get_height())
        # pos = (position[0] - text.get_width(), position[1] - text.get_height())
        position = pos
    elif move_pos != None:
        pos = (position[0] + move_pos[0], position[1] + move_pos[1])
        position = pos
    if not alpha == 255:
        surface_under = pygame.Surface((text.get_width(), text.get_height()), SRCALPHA).convert()
        surface_under.blit(text, (0, 0))
        surface_under.set_alpha(alpha)
        canvas.blit(surface_under, position)
        return
    canvas.blit(text, position)

class Box():
    def __init__(self, hero, canvas):
        self.hero = hero
        self.canvas = canvas
        self.qua_list = [0, 1, 2, 3]
        self.qua_prob_list = []
        self.items = []
        self.this_item = 0

    def box_init(self, num, boxs):
        self.this_box = boxs[num]
        # print(self.this_box)
        # self.this_box.pop(0)
        self.index_prob = random.randint(0, 99)
        self.this_qua = self.qua_prob_list[self.index_prob]
        # print(self.this_qua)
        self.items = []
        for item in self.this_box:
            if item[0] == self.this_qua:
                self.items.append(item[1])
        self.this_item = random.randint(0, len(self.items) - 1)

    def set_prob(self, gold, purple, blue, green):
        self.qua_prob_list = []
        if not ((gold + purple + blue + green) == 100):
            return
            # print("return")
        prob_list = [gold, purple, blue, green]
        # for porb in prob_list:
        #     porb = porb * 10
        prob_i = 0
        for qua in self.qua_list:
            i = 0
            while i < prob_list[prob_i]:
                self.qua_prob_list.append(qua)
                i += 1
            prob_i += 1
        # print(self.qua_prob_list)

    def summon(self):
        items = Items(self.hero, self.canvas)
        self.real_items = []
        self.real_items.append(items.list[self.items[self.this_item]][0])
        return self.real_items

class Box_Animation():
    def __init__(self):
        self.times = 4
        t = self.times
        self.box_sprite = Sprite(pygame.transform.scale(pygame.image.load("images/box/boxes.png"), (183 * t, 45 * t)),
                                 (136 * t, 126 * t),
                                 [(0, 0), (61 * t, 0), (122 * t, 0)],
                                 (61 * t, 45 * t),
                                 0.2
                                 )
        t = 5
        self.buttons = \
            [
                PoolButton(
                    pygame.transform.scale(pygame.image.load("images/box/button/button1.png"), (80 * t, 16 * t)),
                    (1259, 952),
                    [(0, 0), (40 * t, 0)],
                    (40 * t, 16 * t),
                    "打开一次"
                ),
                PoolButton(
                    pygame.transform.scale(pygame.image.load("images/box/button/button1.png"), (80 * t, 16 * t)),
                    (1592, 952),
                    [(0, 0), (40 * t, 0)],
                    (40 * t, 16 * t),
                    "打开十次"
                )
            ]
        self.state = 0
        self.interval = 0
        self.lastTime = time.time()
        self.pools = [Pool(pygame.image.load("images/box/pools/1st/FallingStarLight.png"))]
        self.pool_index = 0
        self.pool_alpha = 0
        self.colors = []
        self.index = 0

    def main(self, canvas, VIDEOSIZE, font):
        WIDTH = VIDEOSIZE[0]
        HEIGHT = VIDEOSIZE[1]
        if self.state == 0:
            self.interval = 3 * self.box_sprite.interval
            self.box_sprite.animation(canvas, 0, 2)
            if not ifDoAction(self.lastTime, self.interval):
                return
            self.lastTime = time.time()
            self.state = 1
        elif self.state == 1:
            pool = self.pools[self.pool_index]
            pool.update()
            pool.set_size((WIDTH, HEIGHT))
            size = pool.img.get_size()
            for button in self.buttons:
                button.draw(pool.img)
                writeText(button.text,
                          (button.position[0] + button.size[0] / 2, button.position[1] + button.size[1] / 2),
                          canvas,
                          font=font,
                          is_middle=True)
            self.alpha_surface = pygame.Surface(size, SRCALPHA).convert()
            self.alpha_surface.blit(pool.img, (0, 0))
            self.alpha_surface.set_alpha(self.pool_alpha)
            canvas.blit(self.alpha_surface, (0, 0))
            self.pool_alpha += 30
            if self.pool_alpha >= 255:
                self.state = 2
                pool.update()
                pool.set_size((WIDTH, HEIGHT))
        elif self.state == 2:
            pool = self.pools[self.pool_index]
            pool.draw(canvas)
            for button in self.buttons:
                button.draw(canvas)
                writeText(button.text,
                          (button.position[0] + button.size[0] / 2, button.position[1] + button.size[1] / 2),
                          canvas,
                          font=font,
                          is_middle=True)

    def change_scale(self, SIZE):
        for pool in self.pools:
            pool.set_size(SIZE)
        self.box_sprite.set_pos(SIZE)

    def get_item(self, text, GameVar):
        price = 10
        if text == "打开一次":
            if not checkCoin(price, GameVar):
                GameVar.messageControl.message_summon("System", "金币不足！")
                return False
            GameVar.coin -= price
            data = GameVar.home.box(0, 1,)
            passer = False
            for item in GameVar.backpack:
                if item.name == data[0].name:
                    print("repeat" + item.name, data[0].name)
                    item.number += 1
                    item.update(GameVar)
                    passer = True
            if not passer:
                GameVar.backpack.append(Account_Item(GameVar.ITEMS.id_list[data[0].name], 1, GameVar.ITEMS))
            return True
        elif text == "打开十次":
            if not checkCoin(price * 10, GameVar):
                # message_summon("System", "金币不足！")
                return False
            GameVar.coin -= price * 10
            datas = GameVar.home.box(0, 10)
            for data in datas.copy():
                passer = False
                for item in GameVar.backpack:
                    if item.name == data.name:
                        # print("repeat" + item.name, data.name)
                        item.number += 1
                        item.update(GameVar)
                        passer = True
                if not passer:
                    GameVar.backpack.append(Account_Item(GameVar.ITEMS.id_list[data.name], 1, GameVar.ITEMS))
            # print(GameVar.home.list)
            return True
        GameVar.save()

    def start(self):
        self.lastTime = time.time()
        self.box_sprite.reset()
        self.pool_alpha = 0
        self.state = 0

class Box_result():
    def __init__(self,VIDEOSIZE):
        WIDTH = VIDEOSIZE[0]
        HEIGHT = VIDEOSIZE[1]
        self.state = 0
        # self.times = int(WIDTH / 320)
        self.times = 4
        t = self.times
        self.background = pygame.Surface((320, 180))
        self.box_sprite = Sprite(pygame.transform.scale(pygame.image.load("images/box/boxes.png"), (183, 45)),
                                 (135 - 5, 125),
                                 [(0, 0), (61, 0), (122, 0)],
                                 (61, 45),
                                 0.2
                                 )
        self.passer = False
        self.lastTime = time.time()
        self.lights = []
        self.index = 0
        self.light_cover = pygame.image.load("images/box/box_light_cover.png")
        self.light_cover_orgin = self.light_cover
        self.item_animations = []
        self.item_animations_orgin = []

    def append_light(self, colors, SIZE):
        mask = pygame.image.load("images/box/box_light_mask.png")
        # mask = pygame.transform.scale(mask, (320, 180))
        for color in colors:
            self.lights.append(Box_Light(color, mask, SIZE, self.background.get_size()))
            self.lights.append(Box_Light((0, 0, 0), mask, SIZE, self.background.get_size()))

    def draw_result(self, canvas, die, last_fps_time):
        canvas.blit(die, (0, 0))
        for item in self.item_animations:
            item.animation(canvas, last_fps_time)

    def draw_result_old(self, times, items):
        if times == 1:
            img = items[0].img
            canvas.blit(img, (WIDTH / 2 - img.get_width() / 2, HEIGHT / 2 - img.get_height() / 2))
            item_animation.animation(canvas)
        elif times == 10:
            pos = (WIDTH / 2 - 290, HEIGHT / 2 - 110)
            i = 0
            line = 0
            for item in items:
                img = item.img
                canvas.blit(img, (pos[0] + i * 120, pos[1] + line * 120))
                i += 1
                if i > 4:
                    i = 0
                    line += 1

    def summon_anime(self, GameVar, WIDTH, HEIGHT):
        self.item_animations_orgin = []
        # print(GameVar.home.list)
        length = len(GameVar.home.list)
        # message_summon("System", str(length))
        # print(length)
        if length == 1:
            img = GameVar.home.list[0].img
            pos = (WIDTH / 2 - img.get_width() / 2, HEIGHT / 2 - img.get_height() / 2)
            self.item_animations_orgin.append(Box_Item_Animation(img, pos, GameVar.home.list[0].get_color()))
        elif length == 10:
            pos = (WIDTH / 2 - 275, HEIGHT / 2 - 110)
            i = 0
            line = 0
            for item in GameVar.home.list:
                img = item.img
                this_pos = (pos[0] + i * 120, pos[1] + line * 120)
                self.item_animations_orgin.append(Box_Item_Animation(img, this_pos, item.get_color()))
                i += 1
                if i > 4:
                    i = 0
                    line += 1

    def draw_box(self):
        self.box_sprite.index = 2
        self.light_cover = self.light_cover_orgin
        self.lights[self.index].draw_bottom(self.background, self.light_cover)
        self.box_sprite.draw(self.background)
        self.background.blit(self.light_cover, (self.box_sprite.position))
        self.lights[self.index].draw_mask(self.background)

    def item_animation_join(self):
        if not ifDoAction(self.lastTime, self.interval):
            return
        self.lastTime = time.time()
        self.light_index += 1
        if self.light_index >= len(self.item_animations_orgin):
            return
        self.item_animations.append(self.item_animations_orgin[self.light_index])

    def skip(self, GameVar, VIDEOSIZE):
        WIDTH = VIDEOSIZE[0]
        HEIGHT = VIDEOSIZE[1]
        if self.state != 3:
            self.box_sprite.index = 2
            self.lastTime = time.time()
            self.light_index = 0
            if self.lights == []:
                colors = []
                for item in GameVar.home.list:
                    colors.append(item.get_color())
                self.append_light(colors, VIDEOSIZE)
            self.index = len(self.lights) - 1
            if self.item_animations == [] or self.item_animations_orgin == []:
                self.summon_anime(GameVar, WIDTH, HEIGHT)
            self.item_animations.append(self.item_animations_orgin[self.light_index])
            self.interval = 0.15
            self.state = 3
        else:
            pass

    def main(self, canvas, VIDEOSIZE, GameVar, die, last_fps_time):
        WIDTH = VIDEOSIZE[0]
        HEIGHT = VIDEOSIZE[1]
        WIDTH_2 = WIDTH / 2
        HEIGHT_2 = HEIGHT / 2
        if self.state == 0:
            self.background.fill((0, 0, 0))
            self.interval = 3 * self.box_sprite.interval
            self.box_sprite.animation(self.background, 0, 2)
            if ifDoAction(self.lastTime, self.interval):
                self.lastTime = time.time()
                self.state = 1
                self.summon_anime(GameVar, WIDTH, HEIGHT)
                self.passer = False
        elif self.state == 1:
            self.box_sprite.index = 2
            self.box_sprite.draw(self.background)
            self.interval = 2
            if ifDoAction(self.lastTime, self.interval):
                self.lastTime = time.time()
                lights = []
                colors = []
                for item in GameVar.home.list:
                    colors.append(item.get_color())
                self.append_light(colors, VIDEOSIZE)
                self.index = 0
                self.state = 2
        elif self.state == 2:
            self.draw_box()
            if len(self.lights) == 20:
                self.interval = 0.15
            elif len(self.lights) == 2:
                self.interval = 0.3
            # self.interval = 0.3
            if ifDoAction(self.lastTime, self.interval):
                self.lastTime = time.time()
                self.index += 1
                if self.index > len(self.lights) - 1:
                    self.state = 3
                    self.lastTime = time.time()
                    self.light_index = 0
                    # print(self.item_animations_orgin)
                    self.item_animations.append(self.item_animations_orgin[self.light_index])
        canvas.blit(pygame.transform.scale(self.background, (320 * self.times, 180 * self.times)),
                    (WIDTH_2 - 320 * self.times / 2, HEIGHT_2 - 180 * self.times / 2))
        if self.state == 3:
            self.index = len(self.lights) - 1
            self.draw_box()
            self.item_animation_join()
            self.draw_result(canvas, die, last_fps_time)

    def start(self):
        self.lastTime = time.time()
        self.state = 0
        self.passer = False
        self.lights = []
        self.index = 0
        self.light_index = 0
        self.item_animations_orgin = []
        self.item_animations = []
        self.box_sprite.reset()
        # message_summon("System", "box_get_reset")

class Box_Light():
    def __init__(self, color, mask, video_size, target_size):
        self.color = color
        self.mask_orgin = mask
        self.mask = self.mask_orgin
        self.video_size = video_size
        self.color_surface = pygame.Surface(target_size)
        self.color_surface.fill(self.color)
        # self.color_surface.set_alpha(125)
        self.color_surface_orgin = self.color_surface
        self.originScreenSize = (1280, 720)
        self.originPoint = (-5, 0)

    def draw_bottom(self, target, cover):
        target.blit(self.color_surface, self.originPoint)
        # cover.blit(self.color_surface, (0,0))

    def draw_mask(self, target):
        target.blit(self.mask, self.originPoint)

    def change_scale(self, size):
        self.color_surface = pygame.transform.scale(self.color_surface_orgin, size)
        self.mask = pygame.transform.scale(self.mask_orgin, size)
        # self.originPoint = (size[0] / 2 - self.originScreenSize[0] / 2, size[1] / 2 - self.originScreenSize[1] / 2)


class Box_Item_Animation():
    def __init__(self, img, end_pos, color):
        self.img = img
        self.light_mask_orgin = pygame.image.load("images/box/item_light_mask.png")
        self.light_mask = pygame.transform.scale(self.light_mask_orgin, (self.light_mask_orgin.get_size()[0] * 2,
                                                                         self.light_mask_orgin.get_size()[1] * 2))
        self.light_size = self.light_mask.get_size()
        self.mask_move = (self.img.get_width() / 2 - self.light_size[0] / 2,
                          self.img.get_height() / 2 - self.light_size[1] / 2)
        self.light = pygame.Surface(self.light_mask.get_size())
        self.color = color
        self.light.fill(self.color)
        self.end_pos = end_pos
        self.start_pos = (self.end_pos[0], self.end_pos[1] + self.img.get_height())
        self.pos = self.start_pos
        self.alpha_surface = pygame.Surface(self.img.get_size(), SRCALPHA).convert()
        self.alpha_surface_orgin = self.alpha_surface
        self.alpha = 0
        self.alpha_surface.set_alpha(self.alpha)
        self.speed = 400

    def animation(self, target, last_fps_time):
        self.alpha_surface.blit(self.light, (0, 0))
        self.alpha_surface.blit(self.light_mask, (0 + self.mask_move[0], 0 + self.mask_move[1]))
        self.alpha_surface.blit(self.img, (0, 0))
        target.blit(self.alpha_surface, self.pos)
        if self.pos[1] <= self.end_pos[1]:
            self.alpha_surface.set_alpha(255)
            self.pos = self.end_pos
            return
        self.alpha_surface.set_alpha(self.alpha)
        self.pos = (self.pos[0], self.pos[1] - self.speed * last_fps_time / 1000)
        self.alpha += 5
