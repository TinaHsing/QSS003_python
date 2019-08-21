#import sys
import time
import subprocess
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)

ip = subprocess.check_output(["hostname","-I"])
ip = str(ip)
#print(ip)
ip = ip[2:-4]
#print(ip)
lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string(ip)
time.sleep(5)