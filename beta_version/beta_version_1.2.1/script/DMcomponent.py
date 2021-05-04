import script.GameVar

#创建判子类
class DMcomponent():
    def __init__(self,number,iflighted):
        #基础数值
        self.number=number
        self.iflighted=iflighted
        self.if_lighted=False
        if self.number==0:
            self.x=GameVar.hero.x
            self.y=GameVar.hero.y-85
        elif self.number==1:
            self.x=GameVar.hero.x+85
            self.y=GameVar.hero.y
        elif self.number==2:
            self.x=GameVar.hero.x
            self.y=GameVar.hero.y+85
        elif self.number==3:
            self.x=GameVar.hero.x-85
            self.y=GameVar.hero.y
        self.x=self.x
        self.y=self.y
        self.width=50
        self.height=50
        self.img=yellowDM
        self.imgLighted=yellow
        self.color=self.img
    def checkLighted(self):
            if self.if_lighted:
                self.color=self.imgLighted
            else:
                self.color=self.img
    def draw(self):
        self.checkLighted()
        canvas.blit(self.color,(self.x,self.y))
    def lighten(self):
        if self.iflighted==True:
            self.iflighted=False

        else:
            self.iflighted=True
    def hit(self,component):
        c=component
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
    def bang(self):
        if self.hit==True:
            GameVar.hero.score+=1