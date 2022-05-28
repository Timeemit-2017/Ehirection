import time


class Animation(object):
    def __init__(self, index, arguments):
        self.state = 0
        self.indexs = index  # [[1,2]]
        self.arguments = arguments  # [[(True, True), (True, True)]]
        self.sprites = []

    def main(self, canvas):
        if self.state == 0:
            index = self.indexs[self.state]
            arguments = self.arguments[self.state]
            for i in index:
                self.sprites[i].animation(arguments[i])

    def set(self, arguments):
        for arg in arguments:
            self.sprites.append(Sprite(arg[0], arg[1], arg[2], arg[3]))


class MoveObject(object):
    def __init__(self, img, pos, speed):
        self.img = img
        self.pos = pos
        self.orginal_pos = pos
        self.speed = speed  # pixel/sec

    def reset(self):
        self.pos = self.orginal_pos


class Sprite(object):
    def __init__(self, source, position, pos, size, interval):
        self.source = source
        self.position = position
        self.position_origin = self.position
        self.pos = pos  # List
        self.size = size  # turple
        self.index = 0
        self.interval = interval
        self.lastTime = time.time()
        # self.minus_size = (self.position[0] / 1280, self.position[1] / 720)
        self.originScreenSize = (1280, 720)
        self.originPoint = (0, 0)

    def draw(self, target):
        draw_range = (self.pos[self.index][0], self.pos[self.index][1], self.size[0], self.size[1])
        target.blit(self.source, (self.position[0] + self.originPoint[0], self.position[1] + self.originPoint[1]), draw_range)

    def animation(self, target, start, end, if_set=True):
        self.draw(target)
        if not self.ifDoAction(self.interval, self.lastTime):
            return
        self.lastTime = time.time()
        self.index += 1
        if if_set and self.index > end or self.index < start:
            self.index = start
            return "Done"
        if self.index > len(self.pos):
            self.index = 0
            return "Done"

    def reset(self):
        self.state = 0
        self.index = 0
        self.lastTime = time.time()

    def set_pos(self, screen_size):
        # 要求：screen_size必须大于 (1280, 720)，否则会有兼容性问题
        #self.position = (screen_size[0] * self.minus_size[0], screen_size[1] * self.minus_size[1])

        self.originPoint = (screen_size[0] / 2 - self.originScreenSize[0] / 2, screen_size[1] / 2 - self.originScreenSize[1] / 2)

    def ifDoAction(self,lastTime, interval):
        if lastTime == 0:
            return True
        currectTime = time.time()
        return currectTime - lastTime >= interval
