import sys
import time
import smbus2
 
sys.modules['smbus'] = smbus2
 
from RPLCD.i2c import CharLCD
 
lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
 
index = 0
str1 = "ABCDEFGHIJKLMNOP"
str2 = "abcdefghijklmnop"
try:
    print('按下 Ctrl-C 可停止程式')
    lcd.clear()
    while True:
        if (index > 15):
            lcd.clear()
            index = 0
        lcd.cursor_pos = (0, index)
        #lcd.write_string("Date: {}".format(time.strftime("%Y/%m/%d")))
        lcd.write_string(str1[index])
        lcd.cursor_pos = (1, index)
        #lcd.write_string("Time: {}".format(time.strftime("%H:%M:%S")))
        lcd.write_string(str2[index])
        index = index + 1
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    lcd.clear()

