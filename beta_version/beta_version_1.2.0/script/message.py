import sys
# from script.Objects import *

sys.path.append("../eightDirection.py")
#from eightDirection import GameVar

def message_summon(come,message):
    GameVar.messages.append(Message(0,0,None,None,come,message))

def message_state_change():
    if not GameVar.last_state == GameVar.states:
        message_summon("System","StateChange( " + GameVar.States[GameVar.last_state] + " to " + GameVar.States[GameVar.states] + " )")
        GameVar.last_state = GameVar.states
def message_check_y():
    i = 0
    for message in GameVar.messages:
        if message.can_delete == False:
            message.y = i * 15
        i += 1
def message_draw():
    for message in GameVar.messages:
        message.draw()

def message_delete():
    for message in GameVar.messages:
        message.check_time()
        message.delete()

def message_main():
    if GameVar.if_message:
        message_state_change()
        message_check_y()
        message_draw()
        message_delete()

# #创建提示类
# class Message(EHRTObject):
#     def __init__(self,x,y,width,height,_from_,message):
#         EHRTObject.__init__(self,x,y,width,height)
#         self._from_ = _from_
#         self.from_display = "<" + self._from_ + ">"
#         self.message = message
#         self.alpha = 255
#         self.can_delete = False
#         self.summon_time = time.time()
#     def set_y(self):
#         index = GameVar.messages.index(self)
#     def draw(self):
#         writeText(self.from_display + self.message,(self.x,self.y),(255,255,255),self.alpha,Font.console)
#     def check_time(self):
#         if not ifDoAction(self.summon_time,1):
#             return
#         self.can_delete = True
#     def delete(self):
#         #消失特效
#         if self.can_delete:
#             self.y -= 1
#             if self.y <= -15:
#                 GameVar.messages.remove(self)