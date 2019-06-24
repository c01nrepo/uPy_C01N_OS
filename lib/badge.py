import network
import ssd1306
from neopixel import NeoPixel
from machine import Pin,I2C,ADC

class btn:
	U=Pin(15,Pin.IN,Pin.PULL_UP)
	D=Pin(4,Pin.IN,Pin.PULL_UP)
	L=Pin(0,Pin.IN,Pin.PULL_UP)
	R=Pin(2,Pin.IN,Pin.PULL_UP)
	A=Pin(33,Pin.IN,Pin.PULL_UP)
	B=Pin(32,Pin.IN,Pin.PULL_UP)

i2c = I2C(scl=Pin(22),sda=Pin(21),freq=10000000)
oled = ssd1306.SSD1306_I2C(128,64,i2c,0x3c)

np = NeoPixel(Pin(13), 1)

def readConfig():
	import ujson
	config = ujson.load(open('/config.json'))
	return config

def writeConfig(config): # Use responsibly
	cfile = open('/config.json','w')
	import ujson
	ujson.dump(config, cfile)
	cfile.close()

wlanSTA = network.WLAN(network.STA_IF)
wlan = wlanSTA
def connectWifi(creds=-1):
	if creds == -1: creds = readConfig()['wifi']
	wlan.active(True)
	wlan.connect(creds[0],creds[1])
	return wlan

wlanAP = network.WLAN(network.AP_IF)
class battery:
	def __init__(self,vadc=35):
		self.VBAT = ADC(Pin(vadc))
		self.VBAT.width(ADC.WIDTH_12BIT)
		self.VBAT.atten(ADC.ATTN_11DB)
		self.CALIB = 3.6 * 2
		self.VMIN = round(3.4 / self.CALIB * 4096)
		self.VMAX = round(4.3 / self.CALIB * 4096)
	def voltage(self): return self.VBAT.read() / 4096 * self.CALIB
	def percentage(self): return (self.VBAT.read() - self.VMIN) / (self.VMAX - self.VMIN)

BAT = battery()
