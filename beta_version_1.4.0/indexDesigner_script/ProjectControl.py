from indexDesigner_script.Arrow import *


class ProjectControl:
    def __init__(self, canvas, SIZE):

        self.SIZE = SIZE
        self.WIDTH = self.SIZE[0]
        self.HEIGHT = self.SIZE[1]

        self.name = "UnNamed"
        self.littleName = "UnNamed"
        self.music_road = "Undefined"
        self.cover_road = "Undefined"
        self.author = "None"
        self.noteDesigner = "None"

        self.arrowControl = ArrowControl(canvas)
        self.thisTime = 0
        self.editFloor = 0
        self.editChoose = 0
        self.canvas = canvas
        self.startIndexFlag = False
        self.aHOLD = False
        self.dHOLD = False
        self.moveSpeed = 40
        self.is_append = False
        self.thisSongLong = 50000

        self.mode = "yellow"

        self.middleLine = pygame.Surface((self.WIDTH, 1))
        self.middleLineColor = (255, 0, 255)
        self.middleLine.fill((255, 0, 255))
        self.TimeLine = pygame.Surface((1, self.HEIGHT))
        self.TimeLineColor = (0, 0, 255)
        self.TimeLine.fill(self.TimeLineColor)

    def arrowMain(self):
        if self.editFloor == 2:
            self.arrowControl.move_arrow(self.aHOLD, self.dHOLD, self.editChoose, self.moveSpeed)
        self.arrowControl.draw_arrow(self.thisTime)
        self.arrowControl.highLight_arrow(self.editFloor, self.editChoose)
        self.arrowControl.highLightArrow(self.editFloor, self.startIndexFlag)
        self.arrowControl.noticeArrow(self.startIndexFlag, self.is_append)
        self.arrowControl.drawBlank(self.WIDTH, self.editFloor, self.editChoose)

    def attributeMain(self, MUSIC_OFFSET):
        if self.startIndexFlag:
            self.thisTime = pygame.mixer.music.get_pos() - MUSIC_OFFSET
        if self.thisTime < 0:
            self.thisTime = 0
        # elif self.thisTime > self.thisSongLong * 1000:
        #     self.thisTime = self.thisSongLong * 1000
        if self.editChoose < 0:
            self.editChoose = 0
        elif self.editChoose >= len(self.arrowControl.highLightArrows):
            self.editChoose = len(self.arrowControl.highLightArrows) - 1

    def basicStuffMain(self):
        self.canvas.blit(self.middleLine, (0, self.HEIGHT / 2))
        self.canvas.blit(self.TimeLine, (self.WIDTH / 2, 0))
        renderText(str(round(self.thisTime / 1000, 3)), (self.canvas.get_width(), 20), self.canvas, font=Font.time_font, rightLine=True)

    def indexMain(self, MUSIC_OFFSET):
        self.attributeMain(MUSIC_OFFSET)
        self.basicStuffMain()
        self.arrowMain()

    def changeWindowSize(self, newSIZE):
        self.SIZE = newSIZE
        self.WIDTH = self.SIZE[0]
        self.HEIGHT = self.SIZE[1]
        self.middleLine = pygame.Surface((self.WIDTH, 1))
        self.middleLine.fill(self.middleLineColor)
        self.TimeLine = pygame.Surface((1, self.HEIGHT))
        self.TimeLine.fill(self.TimeLineColor)

