from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT


SPI_PORT = 1
SPI_CH = 0
SPI_SPEED = 4000000

AOPIN = 27
RSTPIN = 17
TFT_WIDTH = 128
TFT_HEIGHT = 128
TFT_SIZE = (TFT_WIDTH, TFT_HEIGHT)

COLOR_RED 	= (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE	= (0,0,255)
COLOR_WHITE	= (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_YELLOW = (255,255,0)
COLOR_PURPLE = (255,0, 255)
COLOR_CYAN = (0, 255,255)

FONT_SIZE = 14
MAX_X = TFT_WIDTH/FONT_SIZE
MAX_Y = TFT_HEIGHT/FONT_SIZE

X_OFFSET = 8
Y_OFFSET = 8

FONT_1 = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_2 = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_3 = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_4 = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_5 = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_6 = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

class TFT_TEXT():
	def __init__(self, bgcolor = COLOR_WHITE):
		self.spi = SPI.SpiDev(SPI_PORT, SPI_CH, max_speed_hz = SPI_SPEED)
		self.disp = TFT.ST7735(dc=AOPIN, rst = RSTPIN, spi = self.spi, width = TFT_WIDTH, height = TFT_HEIGHT)
		self.disp.begin()
		self.disp.clear()
		self.bgcolor = bgcolor
		self.img = Image.new('RGB', TFT_SIZE, bgcolor)
		self.draw = ImageDraw.Draw(self.img)
		self.font = FONT_1
		self.color = COLOR_BLACK
		self.col = 0
		self.row = 0

	def setFontColor(self, font, color):
		self.font = font 
		self.color = color
		self.fontout = ImageFont.truetype(self.font, FONT_SIZE)

	def gotoPos(self, col, row):
		if (self.col >= MAX_X) or (self.col < 0):
			self.col = 0
		if (self.row >= MAX_Y) or (self.row < 0):
			self.row = 0

		tmp = "col = " + str(self.col) + " , row = " + str(self.row) 
		print(tmp)
		self.xpos = self.col * FONT_SIZE + X_OFFSET
		self.ypos = self.row * FONT_SIZE + Y_OFFSET
		self.cord = (self.xpos, self.ypos)

	def printText(self, outText):
		num = len(outText)
		if (self.col + num >= MAX_X):
			num = MAX_X - self.col - 1
			outText = outText[0:num]

		tmp = "X = " + str(self.xpos) + " , Y = " + str(self.ypos) 
		print(tmp)
		self.draw.rectangle((self.xpos, self.ypos, self.xpos + FONT_SIZE * num, self.ypos + FONT_SIZE), self.bgcolor) #erase target position with bgcolor
		self.draw.text(self.cord, outText, font = self.fontout, fill = self.color)
		self.disp.display(self.img)

	def clearScreen(self, bgcolor=COLOR_WHITE):
		self.draw.rectangle((0,0,TFT_WIDTH,TFT_HEIGHT),self.bgcolor)
		self.disp.display(slef.img)


if __name__ == '__main__':
	tft = TFT_TEXT()
	tft.setFontColor(FONT_1, COLOR_RED)
	tft.gotoPos(0,0)
	tft.printText("Hello")

	tft.setFontColor(FONT_2, COLOR_GREEN)
	tft.gotoPos(1,1)
	tft.printText("Hello")

	tft.setFontColor(FONT_3, COLOR_BLUE)
	tft.gotoPos(2,2)
	tft.printText("Hello")

	tft.setFontColor(FONT_4, COLOR_YELLOW)
	tft.gotoPos(3,3)
	tft.printText("Hello")

	tft.setFontColor(FONT_5, COLOR_PURPLE)
	tft.gotoPos(4,4)
	tft.printText("Hello")

	tft.setFontColor(FONT_6, COLOR_CYAN)
	tft.gotoPos(5,5)
	tft.printText("Hello")

