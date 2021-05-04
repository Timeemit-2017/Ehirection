from script.Objects import *
import script.GameVar

class Home(AnimateObject):
    def __init__(self):
        AnimateObject.__init__(self,0,0,1280,720)
        self.list = []
    def draw(self):
        pass
    def box(self,box,times):
        GameVar.box.set_prob(1.5, 5, 45, 40)
        i = 0
        while i < times:
            GameVar.box.box_init(0)
        self.list = GameVar.box.summon()
        self.print()
    def print(self):
        for item in self.list:
            print(item.name)