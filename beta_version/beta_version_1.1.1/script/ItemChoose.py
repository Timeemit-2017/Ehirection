from script.Images import *
from script.packs.writeText import *
import script.GameVar

class Item_choose():
    def __init__(self):
        self.state = 0
        self.this_item = -1
        self.item_ready = -1
        self.item_choose = item_choose
        self.choose = choose
        self.all_item = all_item
        self.item_choose_y=0
        self.index=0
        self.line=0
        self.start="Start"
        self.last_time=0
        self.intertal=0.5
    def init(self):
        self.state=0
        self.item_choose_y=0 + HEIGHT_2 - 360
    def main(self):
        if self.state == 0:
            if self.item_choose_y>0 + HEIGHT_2 - 360:
                self.animate_0()
                if self.item_choose_y < 0 + HEIGHT_2 - 360:
                    self.item_choose_y = 0
            #canvas.blit(die, (0, 0))
            canvas.blit(self.item_choose, (0,self.item_choose_y))
            if not self.item_ready == -1:
                canvas.blit(items[self.item_ready].img,(591,self.item_choose_y+311))
            self.write_start()
            if self.this_item == -1:
                return
            else:
                canvas.blit(items[self.this_item], (591, 311))
        elif self.state==1:
            if self.item_choose_y<134:
                GameVar.songChoose.draw()
                #canvas.blit(die, (0, 0))
                self.animate_1()
                canvas.blit(self.item_choose,(0, self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(items[self.item_ready].img, (591, self.item_choose_y + 311))
                return
            else:
                GameVar.songChoose.draw()
                #canvas.blit(die, (0, 0))
                canvas.blit(self.all_item,(0,0))
                canvas.blit(self.item_choose,(0,self.item_choose_y))
                if not self.item_ready == -1:
                    canvas.blit(items[self.item_ready].img, (591, self.item_choose_y + 311))
                self.item_draw_1_init()
                self.item_draw_1()
                GameVar.item_choose_highlight.draw()
    def state_change(self, dire):
        if dire:
            self.state += 1
        else:
            self.state -= 1
        if self.state>1:
            self.state=1
        elif self.state<0:
            self.state=0
    def item_draw_1_init(self):
        self.index=0
        self.line=0
    def item_draw_1(self):
        for item in items:
            canvas.blit(item.img,(335+self.index*(100+3),76+self.line*(100+3)))
            self.index+=1
            if self.index>5:
                self.index=0
                self.line+=1
            if self.line>2:
                return True
    def write_start(self):
        writeText(self.start, (WIDTH-226, HEIGHT-45))
        if not ifDoAction(self.last_time,self.intertal):
            return
        self.last_time = time.time()

        if self.start == "Start>>>":
            self.start = "Start"
        self.start = self.start + ">"
    def animate_1(self):
        self.item_choose_y+=37 *last_fps_time/134
    def animate_0(self):
        self.item_choose_y-=37 *last_fps_time/134

class Item_Choose_Highlight(Item_choose):
    def __init__(self):
        super().__init__()
        self.img=choose
    def move(self,dire):
        if self.this_item==-1:
            self.this_item=0
        elif dire=="up":
            if not self.this_item - 6 < 0:
                self.this_item-=6
        elif dire=="right":
            if not self.this_item + 1 > 17:
                self.this_item+=1
        elif dire=="down":
            if not self.this_item + 6 > 17:
                self.this_item+=6
        elif dire=="left":
            if not self.this_item - 1 < 0:
                self.this_item-=1
    def draw(self):
        if self.this_item==-1:
            return
        x = 332 + (self.this_item % 6) * 103 -1
        y = 73 + (self.this_item - self.this_item % 6)/6 * 103 -1
        canvas.blit(self.img,(x,y))