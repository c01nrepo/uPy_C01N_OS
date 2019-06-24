from badge import oled,btn,wlan,connectWifi,readConfig
import urequests
from uikit import selectVList
from time import sleep_ms,ticks_ms
from utils import deleteFolder
import os

def rebuildAppsIndex(APP_ROOT='/apps',INDEX_NAME='apps.json'):
	if INDEX_NAME in os.listdir(APP_ROOT):
		apps = {'list': []}
		import json
		for x in os.ilistdir(APP_ROOT):
			if x[1] == 0x4000 and 'manifest.json' in os.listdir(APP_ROOT+'/'+x[0]):
					curapp = json.load(open(APP_ROOT+'/'+x[0]+'/manifest.json','r'))
					apps['list'].append({"name":curapp['name'],"dir":x[0],"start":curapp['start']})
		f1 = open(APP_ROOT+'/'+INDEX_NAME,'w')
		f1.write(json.dumps(apps))
		f1.close()
		print(apps)

def installApp(REPO_URL,manifest,APP_ROOT='/apps'):
	import upip_utarfile as tarfile
	import uzlib,os,gc
	from upip import url_open
	gc.collect()
	oled.fill(0)
	oled.text('Installing...',0,0,1)
	oled.text(manifest['name'],0,8,1)
	oled.text(manifest['version'],0,16,1)
	oled.show()
	count = 0
	try:
		s1 = url_open(REPO_URL+manifest['url'])
		f2 = uzlib.DecompIO(s1,30)
		t3 = tarfile.TarFile(fileobj=f2)
		for x in t3:
			print(x)
			count += 1
			oled.fill_rect(0,32,128,16,0)
			oled.hctext('File #%d'%count,32,1)
			oled.hctext(x.name[-16:],40,1)
			oled.show()
			if x.type == tarfile.DIRTYPE: # a dir
				FOLDER_PATH = APP_ROOT+'/'+x.name[:-1]
				print(FOLDER_PATH)
				if x.name[:-1] in os.listdir(APP_ROOT): deleteFolder(FOLDER_PATH) # delete if exists
				os.mkdir(FOLDER_PATH)
			else: # a file
				f4 = open(APP_ROOT+'/'+x.name,'wb')
				f4.write(t3.extractfile(x).read())
				f4.close()
	finally:
		s1.close()
	rebuildAppsIndex(APP_ROOT)
	oled.text('Done :)  Reboot!',0,56,1)
	oled.show()
	sleep_ms(500)
	import machine
	machine.reset()

def viewAppDetail(manifest):
	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.text(manifest['name'],0,1,0)
	oled.hctext('V:%s'%manifest['version'],21,1)
	oled.hctext(manifest['author'],31,1)
	oled.text('[R] to Install',0,48,1)
	oled.text('[B] to Cancel',0,56,1)
	desc = manifest['desc']+'   '
	while True:
		ticknow = ticks_ms()
		oled.fill_rect(0,11,128,9,0)
		for i in range(16): oled.text(desc[(i+ticknow//150)%len(desc)],8*i,11,1)
		oled.show()
		if not btn.R.value():
			sleep_ms(300)
			return True
		if not btn.B.value():
			sleep_ms(300)
			return False
		sleep_ms(20)

def app_start():
	connectWifi()
	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.hctext('App Store',1,0)

	if not wlan.isconnected():
		oled.hctext('No WiFi :(',24,1)
		oled.hctext('Connection',32,1)
		oled.hctext('[B] to Quit',56,1)
		oled.show()
		while(btn.B.value()):
			sleep_ms(100)
		return 1

	REPO_URL = readConfig()['apprepourl']

	oled.hctext('Connecting to',24,1)
	oled.hctext('Repository',34,1)
	oled.show()

	listing = (urequests.get("%slisting.json"%REPO_URL)).json()

	s0id = 0
	while True:
		s0id = selectVList('Apps Available',list(map(lambda a: a['name'],listing['apps'])),s0id,1)
		if s0id == -1: return 0
		if viewAppDetail(listing['apps'][s0id]): installApp(REPO_URL, listing['apps'][s0id])

	return 0