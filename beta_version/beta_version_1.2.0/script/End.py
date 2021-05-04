from script.Images import *
import script.GameVar
class End():
    def __init__(self):
        self.result=False
        self.score_img=score
        self.coin_img = coin
        self.dieImg=die
        self.speed=20
        self.coin_plus = 0
    def draw(self):
        canvas.blit(self.dieImg,(0,0))
        canvas.blit(self.result_img,(self.result_x,self.result_y))
        canvas.blit(self.score_img,(self.score_x,self.score_y))
        canvas.blit(self.coin_img, (self.score_x, self.score_y))
    def init(self):
        self.score = GameVar.hero.score
        if GameVar.hero.life>0:
            self.result_x = 0 - 362
            self.result_img=win
        else:
            self.result_x = 0 - 316
            self.result_img=lose
        self.result_y=0
        self.score_x=self.result_x-162
        self.score_y=0
    def animate(self):
        self.result_x+=self.speed
        self.score_x+=self.speed
    def animateOver(self):
        if self.result_x>=0:
            self.result_x=0
        if self.score_x>=0:
            self.score_x=0
