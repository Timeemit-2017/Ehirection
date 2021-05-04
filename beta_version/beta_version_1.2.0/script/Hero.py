from script.Objects import *
from script.Images import *
import script.GameVar
#创建Hero类
class Hero(GameObject):
    def __init__(self,life,defence):
        GameObject.__init__(self,life,defence,WIDTH_2 - 25,HEIGHT_2 -25,50,50,"null")
        self.score=0
        self.mainImg=yellowM
        self.CImg=yellowC
        self.Cy=self.y
        self.rect=self.mainImg.get_rect()
        self.rect.topleft=(self.x,self.y+self.height)
        self.is_button_press = False
    def draw(self):
        canvas.blit(self.CImg,(WIDTH/2 - 25,self.Cy))
        pygame.draw.rect(canvas,(0,0,0),self.rect)
        canvas.blit(self.mainImg, (self.x, self.y))
    def lifeErase(self):
        hurt = GameVar.enemy_damage - self.defeat
        if hurt <=0:
            hurt = 0.1
        self.life -= hurt
    def Cstep(self):
        if self.Cy<self.y+self.height:
            self.Cy+=2
            return False
        else:
            self.Cy=self.y+self.height
            return True
    def bang(self):
        self.lifeErase()