from badge import oled,btn
from time import sleep_ms,ticks_ms

def inputDrawing(width=8, height=8, _S=8, buffer=-1):
	import framebuf
	if buffer == -1: buffer = bytearray(width*height//8)
	fbuf = framebuf.FrameBuffer(buffer, width, height, framebuf.MONO_HLSB)
	cx,cy=0,0
	rdw=1
	while btn.B.value():
		if not btn.U.value():
			while not btn.U.value(): sleep_ms(10)
			cy=(cy-1)%height
			rdw=1
		if not btn.D.value():
			while not btn.D.value(): sleep_ms(10)
			cy=(cy+1)%height
			rdw=1
		if not btn.L.value():
			while not btn.L.value(): sleep_ms(10)
			cx=(cx-1)%width
			rdw=1
		if not btn.R.value():
			while not btn.R.value(): sleep_ms(10)
			cx=(cx+1)%width
			rdw=1
		if not btn.A.value():
			while not btn.A.value(): sleep_ms(10)
			fbuf.pixel(cx,cy,not fbuf.pixel(cx,cy))
			rdw=1
		if rdw:
			rdw=0
			oled.fill(0)
			for x in range(width):
				for y in range(width):
					if fbuf.pixel(x,y): oled.fill_rect(x*_S,y*_S,_S,_S,1)
			oled.rect(cx*_S,cy*_S,_S,_S,not fbuf.pixel(cx,cy))
			oled.text('Draw',80,0,1)
			oled.text('Cursor:',68,16,1)
			curstat='(%s,%s)'%(cx,cy)
			oled.text(curstat,96-len(curstat)*4,26,1)
			oled.text("[B] to",72,47,1)
			oled.text("Finish",72,56,1)
			oled.show()
		sleep_ms(20)
	return (width,height,buffer)

def msgBox(header, lines):
	oled.fill(0)
	oled.fill_rect(0,0,128,10,1)
	oled.text(header,0,1,0)
	if type(lines) != list: lines = [lines[i:i+16] for i in range(0, len(lines), 16)]
	for y, line in enumerate(lines):
		oled.text(line,0,11+y*8,1)
	oled.show()
	while btn.B.value():
		sleep_ms(100)
	sleep_ms(300)

def inputDPAD(Qn='Give Input!',minChar=0):
	oled.fill(0)
	oled.fill_rect(0,0,128,9,1)
	oled.hctext('DPAD INPUT',1,0)
	oled.hctext(Qn,12,1)
	oled.hctext('( need %d keys )'%minChar if minChar > 0 else '[A] to Submit',56,1)
	val = ''
	rdw=1
	while len(val) < minChar or minChar < 1:
		if not btn.A.value() and minChar < 1:
			break
			sleep_ms(200)
		if not btn.B.value():
			val = val[:-1]
			rdw=1
		if not btn.U.value():
			val += 'U'
			rdw=1
		if not btn.D.value():
			val += 'D'
			rdw=1
		if not btn.L.value():
			val += 'L'
			rdw=1
		if not btn.R.value():
			val += 'R'
			rdw=1
		if rdw:
			rdw=0
			oled.fill_rect(0,29,128,9,0)
			oled.hctext(val+('_' if (ticks_ms()>>9)%2 else ' '),30,1)
			oled.show()
			sleep_ms(200)
	oled.hctext('INPUT OK!',42,1)
	oled.show()
	return val


def selectVList(title, items, sel=0, optional=0):
	N = len(items)
	rdw=1
	while btn.A.value():
		if not btn.U.value():
			sel=(sel-1)%N
			rdw=1
		if not btn.D.value():
			sel=(sel+1)%N
			rdw=1
		if (not btn.B.value()) and optional:
			sleep_ms(300)
			return -1
		if rdw:
			oled.fill(0)
			oled.fill_rect(0,31,128,10,1)
			for dy,item in enumerate(items):
				if abs(dy-sel) > 2: continue
				if type(item) == tuple: item = item[0]
				oled.hctext(item,10*(dy-sel)+32,dy!=sel)
			oled.fill_rect(0,0,128,10,1)
			oled.hctext(title,1,0)
			oled.show()
			rdw=0
			sleep_ms(300)
	sleep_ms(300)
	if type(items[sel]) == tuple: return items[sel][1]
	return sel


keyboard = [ "0123456789abcdef",
             "ghijklmnopqrstuv",
			 "wxyzABCDEFGHIJKL",
			 "MNOPQRSTUVWXYZ \n"]
def inputAlphanumeric():
	selRow = 0
	selCol = 0
	ans = ""
	heldDown = False
	while True:
		oled.fill(0)
		oled.hctext(ans[-15:]+('_' if (ticks_ms()>>9)%2 else ' '),0,1)
		oled.hline(0,9,128,1)
		for row in range(4):
			for col in range(16):
				color = (row == selRow and col == selCol)
				oled.fill_rect(1+col*8,20+row*10-1,8,10,color)
				oled.text(keyboard[row][col],1+col*8,20+row*10,not color)
		oled.show()
		if not btn.U.value():
			selRow = (selRow + 4 - 1)%4
		if not btn.D.value():
			selRow = (selRow + 4 + 1)%4
		if not btn.L.value():
			selCol = (selCol + 16 - 1)%16
		if not btn.R.value():
			selCol = (selCol + 16 + 1)%16
		if not btn.A.value():
			if selRow == 3 and selCol == 15:
				return ans
			ans += keyboard[selRow][selCol]
		if not btn.B.value():
			ans = ans[:-1]
		holdCnt = 0
		while((not btn.U.value()) or (not btn.D.value()) or (not btn.L.value()) or (not btn.R.value()) or (not btn.A.value()) or (not btn.B.value())):
			sleep_ms(10)
			holdCnt += 1
			if heldDown:
				if holdCnt >= 5:
					break
			else:
				if holdCnt >= 50:
					heldDown = True
		if holdCnt < 5:
			heldDown = False

def drawDualButton(lefttext, righttext, leftsel, rightsel):
	btnWidth = 54
	btnHeight = 14
	topTextOffset = int((btnHeight-8)/2)
	leftTextOffset = int((btnWidth - len(lefttext)*8)/2)
	rightTextOffset = int((btnWidth - len(righttext)*8)/2)
	if leftsel:
		oled.fill_rect(5, int(64/2-btnHeight/2), btnWidth, btnHeight, 1)
	else:
		oled.rect(5, int(64/2-btnHeight/2), btnWidth, btnHeight, 1)
	oled.text(lefttext, 5+leftTextOffset, int(64/2-btnHeight/2) + topTextOffset, 1-leftsel)

	if rightsel:
		oled.fill_rect(128-5-btnWidth, int(64/2-btnHeight/2), btnWidth, btnHeight, 1)
	else:
		oled.rect(128-5-btnWidth, int(64/2-btnHeight/2), btnWidth, btnHeight, 1)
	oled.text(righttext, 128-5-btnWidth+rightTextOffset, int(64/2-btnHeight/2) + topTextOffset, 1-rightsel)


def getDualButton(title, lefttext, righttext, default):
	sel = default
	hasUpdates = 1
	while(btn.A.value()):
		if hasUpdates:
			oled.fill(0)
			oled.hctext(title, 0,1)
			drawDualButton(lefttext, righttext, 1-sel, sel)
			oled.hctext("A: Select", 64	- 20,1)
			oled.show()
			hasUpdates = 0
		if(btn.L.value() == 0):
			sel = 0
			hasUpdates = 1
		if(btn.R.value() == 0):
			sel = 1
			hasUpdates = 1
	return sel
