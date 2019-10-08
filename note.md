# This is the note for TFT.py
Use the ST7735 library from [github.com/cskau/Python_ST7735](https://github.com/cskau/Python_ST7735)
## pin connection for TFT module
+ VCC 	==> 3.3V
+ GND 	==> GND
+ CS  	==> SPI1.CE0 (BCM 18, WiPI 1, physical 12)
+ RESET	==> TFT_RST (BCM 17, WiPi 0, physical 11)
+ AO 	==> (aka D/C) (BCM 27 WiPi 2, pysical 13)
+ SDA 	==> MOSI (SPI1) (BCM 20, WiPi 28, physical 38)
+ SCK 	==> SCLK (SPI1) (BCM 21, WiPi 29, physical 40)
+ LED 	==> 5V for lighter

## Raspberry Pi pin out for SPI section
![GITHUB](https://github.com/TinaHsing/QSS003_python/blob/master/Doc/spi_pinout.png)

## Modification for QSS003_PI_2
+ pin 12 is CTRL2 now need to change to SPI1.CE0



