
class Sprite():
    def __init__(self,canvas,source,width,height):
        self.canvas = canvas
        self.source = source
        self.width = width
        self.height = height
        self.animation_index = 0
        self.animation_running = False
    def draw(self,index,x,y,index_width,index_height,source_width=500,source_height=500):
        source_width_index = source_width / self.width
        source_height_index = source_height / self.height
        index_column = index % source_width_index
        index_line = (index - index_column) / source_height_index
        img_x = index_column * self.width
        img_y = index_line * self.height
        width = index_width * self.width
        height = index_height * self.height
        self.canvas.blit(self.source,(x,y),(img_x,img_y,width,height))
    def animation(self,x,y,index_width,index_height,start_index,over_index,state):
        if state == "over":
            self.animation_running = False
            return

        if not self.animation_running:
            self.animation_index = start_index
            self.animation_running = True
        self.draw(self.animation_index,x,y,index_width,index_height)
        self.animation_index += 1
        if self.animation_index > over_index:
            self.animation_index = start_index
