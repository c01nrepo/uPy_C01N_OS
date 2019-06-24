from time import sleep_ms,time
from badge import oled,np,connectWifi,btn,BAT
from utils import hsv_to_rgb,loadPBM
from random import random,randint
import machine

import sys
sys.path.append('/systemapps')

#Check for battery level
avg = 0
for i in range(100): avg += BAT.voltage()
if avg/100 < 3.2:
	bypass = False
	for i in range(50):
		oled.fill(0)
		oled.hctext("BATTERY LOW", 0, 1)
		oled.fill_rect(0,32-8,int(128*((50-i)/50)),16,1)
		#TODO: bypass warning
		oled.show()
		sleep_ms(100)
	oled.fill(0)
	oled.hctext("Deep Sleeping", 32-4, 1)
	oled.show()
	sleep_ms(1000)
	oled.poweroff()
	machine.deepsleep()

print('C01N Started!')
connectWifi()
oled.fill(0)

badgelogo = loadPBM('/badge.pbm')
hue = 0
particles = []
for i in range(20): particles.append([64,32,randint(-5,5),randint(-5,5)]) # x,y,vx,vy
while btn.B.value():
	hue = hue + (1/100) % 1
	np[0] = hsv_to_rgb(hue,1,15)
	np.write()
	oled.fill(0)
	for p in particles:
		if (p[0]-64)**2 + (p[1]-32)**2 > 784: oled.fill_rect(p[0],p[1],3,3,1)
		if p[0] < 0 or p[1] < 0 or p[0] > 128 or p[1] > 64 or (p[2] == 0 and p[3] == 0):
			p[0] = 64
			p[1] = 32
			p[2] = randint(-5,5)
			p[3] = randint(-5,5)
		else:
			p[0] += p[2]
			p[1] += p[3]
	if (time() >> 2) % 2:
		oled.blit(badgelogo,0,0,0)
	else:
		oled.fill_rect(32,21,64,20,0)
		oled.hctext("Push [B]",22,1)
		oled.hctext("To Start",33,1)
		sleep_ms(10)
	oled.show()
del particles,hue,badgelogo
import gc
gc.collect()

# TODO virginboot

import launcher
launcher.app_start()
