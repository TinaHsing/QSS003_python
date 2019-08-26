import time
import subprocess
from RPLCD.i2c import CharLCD

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
HOME_DIR = "/home/pi/QSS003_python/"
IP_FILENAME = HOME_DIR + "IP.txt"

ip = subprocess.check_output(["hostname","-I"])
ip = str(ip)	# only for python3

fp = open(IP_FILENAME, "w+")
while (len(ip) < 5):
	fp.writelines("NO IP\n")
	time.sleep(1)
	ip = subprocess.check_output(["hostname","-I"])
	ip = str(ip)	# only for python3

print(ip)
fp.writelines(ip)
fp.writelines("\n")
fp.close()

ip = ip[2:-4]	# only for python3
#print(ip)
lcd.clear()
lcd.cursor_pos = (0, 0)
lcd.write_string(ip)
time.sleep(5)
