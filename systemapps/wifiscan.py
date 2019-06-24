from badge import oled,wlan,btn,np
from time import sleep_ms
from ubinascii import hexlify
from utils import hsv_to_rgb

def performScan():
	oled.fill(0)
	oled.fill_rect(0,0,128,9,1)
	oled.hctext('WiFi Scan',1,0)
	oled.hctext('Scanning...',30,1)
	oled.show()

	wifis = wlan.scan()
	wifis.sort()
	return wifis

authmodes = ['OPEN','WEP','WPA_PSK','WPA2_PSK','WPA_WPA2_PSK','WPA2_ENTERPRISE','MAX']
def drawWifiScreen(wifis,sidx):
	oled.fill(0)
	if len(wifis) < 1:
		#for a in range(360):
		oled.hctext('o_O',10,1)
		oled.hctext('No WiFi Found',25,1)
		oled.hctext('[A] to Re-Scan',56,1)
		np[0] = (10,10,10)
	else:
		ssid, bssid, channel, rssi, authmode, hidden = wifis[sidx]
		oled.hctext(hexlify(bssid),0,1)
		oled.hline(0,8,128,1)
		oled.hctext(ssid,12,1)
		oled.hctext('Ch %d RSSI %d'%(channel,rssi),25,1)
		oled.hctext(authmodes[authmode],35,1)
		if hidden: oled.hctext('Hidden',45,1)
		oled.hctext('< %d/%d >'%(sidx+1,len(wifis)),56,1)
		np[0] = hsv_to_rgb(sidx/len(wifis),1,12)
	oled.show()
	np.write()

def app_start():
	sidx = 0
	needredraw = 1

	wifis = performScan()
	while True:
		sleep_ms(1)
		if btn.A.value() == 0:
			wifis = performScan()
			sidx = 0
			needredraw = 1
		if btn.L.value() == 0:
			sidx=(sidx-1)%len(wifis)
			needredraw = 1
		if btn.R.value() == 0:
			sidx=(sidx+1)%len(wifis)
			needredraw = 1
		if btn.B.value() == 0:
			return 0
		if needredraw:
			drawWifiScreen(wifis,sidx)
			needredraw = 0
			sleep_ms(200)