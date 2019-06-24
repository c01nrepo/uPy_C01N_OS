from badge import oled
from math import floor
import os

def deleteFolder(RPATH):
	if RPATH[-1] == '/': RPATH = RPATH[:-1]
	for x in os.ilistdir(RPATH):
		if x[1] == 0x4000: #TYPE_DIR
			deleteFolder(RPATH+'/'+x[0])
		else:
			os.remove(RPATH+'/'+x[0])
	os.rmdir(RPATH)

def loadPBM(url):
	ImgW = 0
	ImgH = 0
	with open(url, 'rb') as f:
		f.readline() # Magic number
		f.readline() # Creator comment
		ImgW, ImgH = list(map(int,f.readline().decode('utf-8').split())) # Dimensions
		data = bytearray(f.read())
	import framebuf
	fbuf = framebuf.FrameBuffer(data, ImgW, ImgH, framebuf.MONO_HLSB)
	return fbuf

def hsv_to_rgb(h, s, v):
	i = floor(h*6)
	f = h*6 - i
	p = v * (1-s)
	q = v * (1-f*s)
	t = v * (1-(1-f)*s)

	r, g, b = [
		(v, t, p),
		(q, v, p),
		(p, v, t),
		(p, q, v),
		(t, p, v),
		(v, p, q),
	][int(i%6)]

	return (int(r), int(g), int(b))