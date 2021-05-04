

WIDTH = 1280
HEIGHT = 720
WIDTH_2 = WIDTH/2
HEIGHT_2 = HEIGHT/2

class EHRTObject():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class AnimateObject(EHRTObject):
    def __init__(self,x,y,width,height):
        EHRTObject.__init__(self,x,y,width,height)
        self.state = 0
        self.imgs = []
    def appendImg(self,img,position):
        img_list = [img,position]
        self.imgs.append(img_list)
    def draw(self,num="all"):
        if num == "all":
            for img in self.imgs:
                canvas.blit(img[0],img[1])
        else:
            canvas.blit(self.imgs[num][0],self.imgs[num][1])


class GameObject(EHRTObject):
    def __init__(self,life,defeat,x,y,width,height,img):
        EHRTObject.__init__(self,x,y,width,height)
        self.life = life
        self.defeat = defeat
        self.img = img
    def draw(self):
        from script.Images import canvas
        canvas.blit(self.img,(self.x,self.y))
    def hit(self, component):
        c = component
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
