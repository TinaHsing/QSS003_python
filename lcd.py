import RPi.GPIO as GPIO
import time

#Pin define
LCD_RS = 5
LCD_E = 7
LCD_D4 =15
LCD_D5 = 11
LCD_D6 = 29
LCD_D7 = 13

#device constant

LCD_CHR = True
LCD_CMD = False



#timing
E_PULSE = 0.0005
E_DELAY = 0.0005
INIT_DELAY = 0.005
D_DELAY = 0.0002
CLEAR_DELAY = 0.002

class LCD:
	def __init__(self,pin_rs, pin_e, pins_data4):
		#GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		self.rs_pin = pin_rs
		self.e_pin = pin_e
		self.d_pin=pins_data4
		self.pin_init()	
		self.dev_init()	

	def pin_init(self):
		GPIO.setup(self.rs_pin, GPIO.OUT)
		GPIO.setup(self.e_pin, GPIO.OUT)
		GPIO.setup(self.d_pin[0], GPIO.OUT)
		GPIO.setup(self.d_pin[1], GPIO.OUT)
		GPIO.setup(self.d_pin[2], GPIO.OUT)
		GPIO.setup(self.d_pin[3], GPIO.OUT)
		GPIO.output(self.e_pin,False)
		GPIO.output(self.rs_pin, False)
		GPIO.output(self.d_pin[0], False)
		GPIO.output(self.d_pin[1], False)
		GPIO.output(self.d_pin[2], False)
		GPIO.output(self.d_pin[3], False)

	def enable_pulse(self):
		time.sleep(E_DELAY)
		GPIO.otuput(self.e_pin, True)
		time.sleep(E_PULSE)
		GPIO.output(self.e_pin, False)
		time.sleep(E_DELAY)
	
	def clear(self):
		self.write_byte(0x01, LCD_CMD) # 
		time.sleep(CLEAR_DELAY)

	def dev_init(self):
		self.write_4bits(0x03, LCD_CMD) # set device to 4 bit mode from datasheet
		time.sleep(INIT_DELAY)
		self.write_4bits(0x03, LCD_CMD)
		time.sleep(INIT_DELAY)
		self.write_4bits(0x03, LCD_CMD)
		time.sleep(D_DELAY)
		self.write_4bits(0x02, LCD_CMD) # after this line no need dealy

		self.write_byte(0x28, LCD_CMD) # set 2lines and 5x8 font size
		self.write_byte(0x0C, LCD_CMD) # set display on, cursor off, blink off
		self.clear()
		self.wirte_byte(0x06, LCD_CMD) #set the entry mode
		time.sleep(E_DELAY)

	def goto(self,col,row):
		data = col +row*0x40
		data = data|0x80 
		self.write_byte(data, LCD_CMD)

	def write_string(self,input_string):

		total = len(input_string)
		for i in range(total):
			write_byte(ord(input_string[i]), LCD_CHR)

	def write_4bits(self,data, mode):
		GPIO.output(self.rs_pin, mode)
		
		for i in range (0,4):	
			GPIO.output(d_pin[i],data&0x01)
			data = data>>1
		self.enable_pulse()

	def write_byte(self,data,mode):
		high = data >>4
		self.write_4bits(high,mode)
		self.write_4bits(data,mode)

if __name__ == '__main__':
	lcd = LCD(pin_rs=LCD_RS, pin_e=LCD_E, pins_data4=[LCD_D4, LCD_D5, LCD_D6, LCD_D7])

	a ="0123456789ABCDEF"
	b ="abcdefghijklmnop"
	
	for i in range(10):
		lcd.goto(0,0)
		lcd.write_string(a)
		lcd.goto(0,1)
		lcd.write_string(b)
		a=a[-1]+a[:-1]
		b=b[-1]+b[:-1]










		

