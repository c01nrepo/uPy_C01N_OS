from badge import oled,btn,battery,wlan,readConfig
from uikit import selectVList
from time import sleep_ms,localtime
import os
import machine
from ubinascii import hexlify
import gc

def app_start():
	BAT = battery()
	config = readConfig()
	vfs = os.statvfs('/')
	timenow = str(localtime()).replace(' ','')

	items = [
	'Name:%s'%config['name'],
	'Machine Unique:',
	hexlify(machine.unique_id()).decode('utf-8').upper(),
	'',
	'C01N_OS %s'%config['version'],
	'uPy %s'%os.uname().release,
	'',
	'Localtime:',
	timenow[:12],
	timenow[12:],
	'',
	'VBAT: %.2fV'%BAT.voltage(),
	'Battery: %d%%'%(100*BAT.percentage()),
	'',
	'RAM Heap Free:',
	'%d B'%gc.mem_free(),
	'',
	'Flash VFS Size:',
	'%d B'%(vfs[0]*vfs[2]),
	'Flash VFS Free:',
	'%d B'%(vfs[0]*vfs[3]),
	'',
	'WiFi %s'%('Connected!' if wlan.isconnected() else 'Unavaliable'),
	wlan.config('essid'),
	'WiFi MAC:',
	hexlify(wlan.config('mac')).decode('utf-8').upper(),
	]

	selected = 0
	while selected != -1:
		selected = selectVList('Sys Info', items, selected, 1)
		sleep_ms(300)