import pygame

class Button():
    def __init__(self, pos, size, command, this_state=None, color=(0,0,0),text=None, title=None,text_color=(255,255,255),font=None,is_backGround=False,video_size=(1280,720),to=None):
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.pos_ratio = (self.x / video_size[0], self.y / video_size[1])
        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        self.color = color
        self.to = to
        if is_backGround:
            self.backGround = pygame.Surface((self.width, self.height))
        else:
            self.backGround = None
        self.highLight = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_hightLight = False
        self.text = text
        self.text_color = text_color
        self.title = title
        if not self.title == None:
            self.text = self.title + ": " + self.text
        self.font = font
        self.this_state = this_state
        self.command = command
        if not text == None:
            self.word = self.font.render(self.text, True, self.text_color)
            self.word_size = (self.word.get_width(), self.word.get_height())
    def checkRange(self, pos, size=(1, 1)):
        x = pos[0]
        y = pos[1]
        width = size[0]
        height = size[1]
        return x > self.x - width and x < self.x + self.width and \
               y > self.y - height and y < self.y + self.height
    def video_change(self, video_size):
        self.x = video_size[0] * self.pos_ratio[0]
        self.y = video_size[1] * self.pos_ratio[1]
        self.pos = (self.x, self.y)
        self.highLight = pygame.Rect(self.x, self.y, self.width, self.height)
    def click(self, state):
        if not state == self.this_state:
            return
        if type(self.command) == str:
            return self.command
        # elif type(self.command) == str:
        #     self.change_text(self.command)
        #     return

    def change_text(self, text):
        self.text = str(text)
    def draw(self, canvas, state=None):
        if not self.text == None and not self.title == None:
            self.word = self.font.render(self.text, True, self.text_color)
            self.word_size = (self.word.get_width(), self.word.get_height())
        elif not self.text == None:
            self.word = self.font.render(self.text, True, self.text_color)
            self.word_size = (self.word.get_width(), self.word.get_height())
        if not state == self.this_state:
            return
        if not self.backGround == None:
            canvas.blit(self.backGround, (self.pos))
        if not self.text == None:
            canvas.blit(self.word,
                        (self.x + self.width / 2 - self.word_size[0] / 2,
                         self.y + self.height / 2 - self.word_size[1] / 2)
                        )
        if self.is_hightLight:
            pygame.draw.rect(canvas, self.text_color, self.highLight, 1)

class FunctionButton(Button):
    def __init__(self, pos, size, command, this_state=None, color=(0,0,0),text=None, title=None,text_color=(255,255,255),font=None,is_backGround=False,video_size=(1280,720),to=None):
        Button.__init__(self, pos, size, command, this_state=this_state, color=color,text=text, title=title,text_color=text_color,font=font,is_backGround=is_backGround,video_size=video_size,to=to)
    def click(self, state):
        if not state == self.this_state:
            return "StateNotMatch"
        print("click funcation")
        var = self.command()
        if type(var) == str and not self.title == None:
            self.text = self.title + ": " + var