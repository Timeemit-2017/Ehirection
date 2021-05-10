import pygame
pygame.init()

error = "init"

class Lobby():
    def __init__(self,objects):
        self.page = 0
        self.objects = objects
        self.objects_number = len(self.objects)
        self.x = 0
        self.y = 0
        self.this_page_y = 0
        self.width = 1280
        self.height = 720
        self.color = (42,42,63)

class Lobby_object():
    def __init__(self,name,x,y,hl_x,hl_y,width,height,page,imgs,highlight_img,img_num=0):
        self.name = name
        self.x = x
        self.y = y
        self.x_num = self.x / 1280
        self.y_num = self.y / 720
        if not (hl_x == None or hl_y == None):
            self.hl_x = hl_x
            self.hl_y = hl_y
            self.hl_x_num = self.hl_x / 1280
            self.hl_y_num = self.hl_y / 720
        self.width = width
        self.height = height
        if name == "宝箱":
            self.width = 239
            self.height = 327
        self.width_num = width / 1280
        self.height_num = height / 720
        self.imgs = imgs
        self.len_of_imgs = len(self.imgs)
        self.page = page
        self.img_num = img_num
        self.scale_num = 0
        if self.len_of_imgs == 0:
            self.imgs.append(error)
            self.img = error
        elif self.len_of_imgs == 1:
            self.img = self.imgs[0]
        else:
            self.img = self.imgs[self.img_num]
        self.is_lighted = False
        self.highlight_img = highlight_img
    def draw(self,width,screen_x,canvas):
        this_screen_x = screen_x - self.page * width
        x = self.x - self.page * width - this_screen_x
        y = self.y
        canvas.blit(self.img, (x,y))
        if self.is_lighted:
            if self.highlight_img == None:
                return
            hl_x = self.hl_x - self.page * width - this_screen_x
            hl_y = self.hl_y
            canvas.blit(self.highlight_img, (hl_x,hl_y))
    def check_page(self,WIDTH):
        if self.x + self.width < 0 or self.x > WIDTH:
            return False
        else:
            return True
    def change_scale(self,targetXY):
        # if self.scale_num == 0:
        #     self.scale_num += 1
        #     return
        target_x = targetXY[0]
        target_y = targetXY[1]
        # width_and_height = (target_x / 1280, target_y / 720)
        # self.x = self.x * width_and_height[0]
        # self.y = self.y * width_and_height[1]
        # self.width = self.width * width_and_height[0]
        # self.height = self.height * width_and_height[1]
        self.x = target_x * self.x_num
        self.y = target_y * self.y_num
        try:
            self.hl_x = target_x * self.hl_x_num
            self.hl_y = target_y * self.hl_y_num
        except:
            pass
        self.width = target_x * self.width_num
        self.height = target_y * self.height_num
        self.width = int(self.width)
        self.height = int(self.height)
        for img in self.imgs:
            img = pygame.transform.scale(img,(self.width,self.height))
        if self.len_of_imgs == 0:
            self.imgs.append(error)
            self.img = error
        elif self.len_of_imgs == 1:
            self.img = self.imgs[0]
        else:
            self.img = self.imgs[self.img_num]
        if self.name == "宝箱":
            self.x = 506-88
            self.hl_x = self.x - 13
            self.hl_y = self.y - 10
    def checkHit(self,component):
        c = component
        if self.name == "宝箱":
            self.x = 506
            result = c.x > self.x - c.width and c.x < self.x + self.width and c.y > self.y - c.height and c.y < self.y + self.height
            self.x = 418
            return result
        return c.x > self.x - c.width and c.x < self.x + self.width and \
               c.y > self.y - c.height and c.y < self.y + self.height
    def checkRange(self,x,y,width,height):
        return x > self.x - width and x < self.x + width and \
               y > self.y - height and y < self.y + self.height
    def checkMouse(self,events):
        for event in events:
            if event.type == pygame.MOUSEMOTION and self.checkRange(event.pos[0],event.pos[1],1,1):
                return True
            else:
                return False


