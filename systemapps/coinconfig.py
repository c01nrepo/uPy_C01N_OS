from badge import oled, btn, readConfig, writeConfig, wlan
from urandom import getrandbits
from ubinascii import a2b_base64, b2a_base64, hexlify
import socket
import ujson
import gc
import network
import machine

def app_start():
	oled.fill(0)
	oled.hctext('C01N Config',0,1)
	oled.fill_rect(0,55,128,9,1)
	oled.hctext('Restart to Exit',56,0)
	oled.show()
	webhtml = open('/systemapps/coinconfig.html').read()
	config = readConfig()
	outpacket = [['c01n_name','Device Name',config['name']],['c01n_ssid','WiFi SSID',config['wifi'][0]],['c01n_pass','WiFi Password',config['wifi'][1]],['c01n_repo','App Repo URL',config['apprepourl']]]

	ap_if = network.WLAN(network.AP_IF)
	AP_SSID = 'C01N-%s'%hexlify(ap_if.config('mac')).decode('utf-8')[-6:]
	AP_PASS = bytearray(5)
	for p in range(5): AP_PASS[p] = getrandbits(8)
	AP_PASS = hexlify(AP_PASS)
	ap_if.active(1)
	ap_if.config(essid=AP_SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=AP_PASS)
	oled.hctext('SSID:%s'%AP_SSID,11,1)
	oled.hctext('PASS:%s'%AP_PASS.decode('utf-8'),20,1)
	oled.show()

	port = 8000 + getrandbits(10)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', port))
	s.listen(5)
	oled.hctext('Web Page @',32,1)
	oled.hctext('%s:%d'%(ap_if.ifconfig()[0],port),41,1)
	oled.show()

	try:
		while True:
			conn, addr = s.accept()
			print('Connection from %s' % str(addr))
			request = conn.recv(1024)
			request = request.decode('utf-8')
			if 'GET / ' in request:
				conn.send('HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n')
				conn.sendall(webhtml%b2a_base64(ujson.dumps(outpacket)).decode('utf-8')[:-1])
			elif 'UPDATE /?c=' in request:
				lines = request.split('\r\n')
				for line in lines:
					if 'UPDATE /?c=' in line:
						b64 = line.split('UPDATE /?c=')[1].split(' ')[0]
						packet = ujson.loads(a2b_base64(b64))
						if 'c01n_name' in packet: config.update({'name':packet['c01n_name']})
						if 'c01n_ssid' in packet and 'c01n_pass' in packet: config.update({'wifi':[packet['c01n_ssid'],packet['c01n_pass']]})
						if 'c01n_repo' in packet: config.update({'apprepourl':packet['c01n_repo']})
						#config.update({'virginboot':0})
						writeConfig(config)
						oled.fill(0)
						oled.hctext('REBOOTING',30,1)
						oled.show()
						machine.reset()
						break
				conn.send('HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n')
				conn.sendall('{"Status":"OK"}')
			conn.close()
	except KeyboardInterrupt:
		pass
	finally:
		s.close()
		gc.collect()
		machine.reset()