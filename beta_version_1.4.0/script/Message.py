import time
from script.basic import writeText, ifDoAction, Font


# 创建提示类
class Message:
    def __init__(self, x, y, width, height, _from_, message, canvas, GameVar):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._from_ = _from_
        self.from_display = "<" + self._from_ + ">"
        self.message = message
        self.alpha = 255
        self.can_delete = False
        self.summon_time = time.time()
        self.GameVar = GameVar
        self.speed = len(GameVar.messages) + 1
        self.canvas = canvas

    def set_y(self):
        index = self.GameVar.messages.index(self)

    def draw(self):
        writeText(self.from_display + self.message, (self.x, self.y), self.canvas, (255, 255, 255), self.alpha, Font.console)

    def check_time(self):
        if not ifDoAction(self.summon_time, 1):
            return
        self.can_delete = True

    def delete(self, delete_by_alpha_or_move=False):
        # 消失特效
        if delete_by_alpha_or_move: # 为False为用透明度消失，True则用上移消失。
            if self.can_delete:
                # self.y -= len(self.GameVar.messages)
                self.y -= 2
                if self.y <= -15:
                    self.GameVar.messages.remove(self)
        else:
            self.alpha -= 2
            if self.alpha <= 20:
                self.GameVar.messages.remove(self)


class MessageControl:
    def __init__(self, canvas):
        self.messages = []
        self.if_message = True
        self.canvas = canvas

    def message_summon(self, come, message):
        self.messages.append(Message(0, 0, None, None, come, message, self.canvas, self))

    def message_check_y(self):
        i = 0
        for message in self.messages:
            message.y = i * 15
            i += 1

    def message_draw(self):
        for message in self.messages:
            message.draw()

    def message_delete(self):
        for message in self.messages:
            message.check_time()
            message.delete()

    def message_main(self):
        self.message_delete()
        if not self.if_message:
            self.messages = []
            return
        if not self.messages:
            return
        self.message_check_y()
        self.message_draw()
