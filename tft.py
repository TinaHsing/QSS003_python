from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import ST7735 as TFT

spi = SPI.SpiDev(1, 0, max_speed_hz = 1000000)

disp =TFT.ST7735(dc=2, rst = 0, spi = spi, width = 128, height =128)
disp.begin()

bk = Image.new('RGB', (128,128), (255,0,0))
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",30)
draw = ImageDraw.Draw(bk)
draw.text((10,10),"Hello", font=font, fill =(0,255,0))

disp.display(bk)
