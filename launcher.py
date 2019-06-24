from badge import oled,btn,np,BAT
from time import sleep_ms,ticks_ms
from utils import hsv_to_rgb
import ujson
import gc
import sys
import os

def app_start():
	apps = []

	apps_manifest = ujson.load(open('/apps/apps.json')) # User Apps
	for app in apps_manifest['list']:
		apps.append((app['name'], '/apps/%s'%app['dir'], app['start']))

	apps.extend([ # System Apps
	('App Store','/systemapps','appstore'),
	('System Info','/systemapps','sysinfo'),
	('File Explorer','/systemapps','fileexplorer'),
	('WiFi Scan','/systemapps','wifiscan'),
	('C01N Config','/systemapps','coinconfig'),
	('Credits','/systemapps','credits')
	])

	sidx = 0
	lastbat = BAT.percentage()
	needredraw = 1
	while True:
		sleep_ms(10)
		batnow = BAT.percentage()
		if abs(lastbat-batnow) > 0.1:
			needredraw = 1
			lastbat = batnow
		if btn.L.value() == 0:
			sleep_ms(200)
			sidx=(sidx-1)%len(apps)
			needredraw = 1
		if btn.R.value() == 0:
			sleep_ms(200)
			sidx=(sidx+1)%len(apps)
			needredraw = 1
		if btn.A.value() == 0:
			sleep_ms(200)
			originalSysModules = set()
			for mod in sys.modules:
				originalSysModules.add(mod)
			# Hacky Launch Code
			exec('try:\n\tos.chdir("%s")\n\timport %s as curapp\n\tcurapp.app_start()\nexcept:\n\toled.hctext("App Launch Fail",30,1)\n\toled.show()\nfinally:\n\tos.chdir("/")'%(apps[sidx][1],apps[sidx][2]))
			# Efficient Cleanup of Userspace
			for mod in sys.modules:
				if mod not in originalSysModules:
					del sys.modules[mod]
			gc.collect()
			needredraw = 1
		if needredraw:
			needredraw = 0
			oled.fill(0)
			oled.text('Apps',0,1,1)
			oled.fill_rect(108,2,int(16*max(min(batnow,1),0)),5,1)
			oled.fill_rect(126,2,2,5,1)
			oled.rect(106,0,20,9,1)
			batstatus = 'USB' if batnow > 1 else '%d%%'%(batnow*100)
			oled.text(batstatus,104-len(batstatus)*8,1,1)
			oled.hline(0,10,128,1)
			oled.hctext(apps[sidx][0],20,1)
			oled.hctext('[A] to Launch',45,1)
			oled.hctext('<  %d/%d  >'%(sidx+1,len(apps)),56,1)
			oled.show()
			np[0] = hsv_to_rgb(sidx/len(apps),1,7)
			np.write()
			sleep_ms(20)
