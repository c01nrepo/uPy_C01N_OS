from badge import oled,btn
from os import ilistdir,stat
from uikit import selectVList,msgBox
from time import sleep_ms

TYPE_DIR = 0x4000
TYPE_FILE = 0x8000

def app_start():
	cedir = '/'
	while True:
		dirlist = []
		for item in ilistdir(cedir): dirlist.append(item[0] + ('/' if item[1] == TYPE_DIR else ''))
		sindex = selectVList(cedir[-16:], dirlist,0,1)
		if sindex == -1:
			sleep_ms(300)
			if cedir == '/': return 0
			cedir = '/'.join(cedir.split('/')[:-1]) # go back
			if cedir == '': cedir = '/'
			continue
		selected = dirlist[sindex]
		if selected[-1] == '/': selected = selected[:-1]
		newpath = cedir + ('' if cedir == '/' else '/') + selected
		filestats = stat(newpath)
		if filestats[0] == TYPE_FILE:
			print("FILE %s"%newpath)
			msgBox(selected,['TYPE_FILE','Size:%dB'%filestats[6],'Path:',newpath[-16:]])
		else:
			cedir = newpath