from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT


SPI_PORT=1
SPI_CH =0
SPI_SPEED =4000000

AOPIN = 27
RSTPIN = 17
TFT_WIDTH = 128
TFT_HEIGHT = 128
TFT_SIZE = (TFT_WIDTH, TFT_HEIGHT)

COLOR_RED 	=(255,0,0)
COLOR_GREEN =(0,255,0)
COLOR_BLUE	=(0,0,255)
COLOR_WHITE	=(255,255,255)
COLOR_BLACK =(0,0,0)
COLOR_YELLOW =(255,255,0)
COLOR_PURPLE =(255,0, 255)
COLOR_CYAN = (0, 255,255)

FONT_SIZE =14
MAX_X = TFT_WIDTH/FONT_SIZE
MAX_Y = TFT_HEIGHT/FONT_SIZE

X_OFFSET =8
Y_OFFSET =8


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
		self.clear()
		self.bgcolor = bgcolor
		self.img = Image.new('RGB', TFT_SIZE, bgcolor)
		self.draw = ImageDraw.Draw(img)
		self.font = FONT_1
		self.color = COLOR_BLACK

	def setFontColor(self, font, color):
		self.font = font 
		self.color= color
		self.fontout = ImageFont.truetype(self.font, FONT_SIZE)

	def gotoPos(self, col, row):
		if col >=MAX_X or col < 0:
			col =0
		if row >=MAX_Y or col <0:
			row =0

		self.xpos = col*FONT_SIZE+X_OFFSET
		self.ypos = row*FONT_SIZE+Y_OFFSET
		self.cord =(self.xpos, self.ypos)

	def printText(self, outText):
		num =len(outText)
		if (self.ypos +num >= MAX_Y):
			num = MAX_Y-self.ypos-1
			outText = outText[0:num]	
		
		self.draw.rectangle((self.xpos, self.ypos, self.xpos+TFT_SIZE, self.ypos+TFT_SIZE*num), self.bgcolor) #erase target position with bgcolor
		self.draw.text(self.cord, outText, font= self.fontout, fill = self.color)
		self.disp.display(self.img)

	def clearScreen(self, bgcolor=COLOR_WHITE):
		self.draw.rectangle((0,0,TFT_WIDTH,TFT_HEIGHT),self.bgcolor)
		self.disp.display(slef.img)
