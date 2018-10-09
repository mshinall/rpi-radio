#!/usr/bin/python

import sys
import I2C_LCD_driver
from pad4pi import rpi_gpio
import time
from subprocess import call

MATRIX = [['1','2','3','A'],
		  ['4','5','6','B'],
		  ['7','8','9','C'],
		  ['*','0','#','D']]

#BCM numbering
COLS = [4,17,27,22]
ROWS = [6,13,19,26]
MODES = ["NFM", "WFM", "AM", "LSB", "USB"]
MNAMES = ["Narrow FM", "Wide FM", "AM", "Lower SSB", "Upper SSB"]
SDR_MODES = ["fm", "wbfm", "am", "lsb", "usb"]
MBANDS = [12.5, 200, 200, 100, 100]
SEEKW = 0.0125
MAX_FREQ = 1700.0000
MIN_FREQ = 25.0000
SDR_CMD = "rtl_fm -M {0} -f {1}M -s 200K -r 48K - | aplay -t raw -r 48000 -c 1 -f S16_LE"

freq = 162.4750
inFreq = str(freq)
midx = 0
mode = MODES[midx]
mname = MNAMES[midx]
mband = MBANDS[midx]
sdrMode = SDR_MODES[midx]
edit = False

mylcd = I2C_LCD_driver.lcd()
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=MATRIX, row_pins=ROWS, col_pins=COLS)

def freqString():
	return '{:.4f}'.format(freq).rjust(9)

def freqFloat():
	return float(inFreq)

def clearLcd():
	global mylcd
	mylcd.lcd_clear()

def updateRadio():
	print("updateRadio: freq=" + freqString() + " mode=" + mode)
	print(SDR_CMD.format(sdrMode, freqString())
	call(SDR_CMD.format(sdrMode, freqString())
	#print("updated")

def changeFreq():
	global freq
	if freq > MAX_FREQ:
		freq = MAX_FREQ
	elif freq < MIN_FREQ:
		freq = MIN_FREQ

	updateLcd()
	updateRadio()

def changeMode():
	global midx
	global mode
	global mname
	global mband

	midx += 1
	if midx >= len(MODES):
		midx = 0
	mode = MODES[midx]
	mname = MNAMES[midx]
	mband = MBANDS[midx]
	sdrMode = SDR_MODES[midx]
	updateLcd()
	updateRadio()

def updateLcd():
	global mylcd
	global freq
	global mode
	global edit

	clearLcd()
	mylcd.lcd_display_string(freqString(), 1, 0)
	mylcd.lcd_display_string("Mhz", 1, 13)
	if edit == True:
		mylcd.lcd_display_string("*", 2, 15)
	mylcd.lcd_display_string(mname, 2, 0)


def handleKeyPress(key):
	global freq
	global inFreq
	global mode
	global edit

	if key == "#":
		edit = True
		inFreq = inFreq[:len(inFreq) - 1]
		freq = freqFloat
		updateLcd()
	elif key == "*":
		edit = True
		inFreq = inFreq + "."
		updateLcd()
	elif key == "A":
		edit = False
		freq = freqFloat()
		changeFreq()
	elif key == "B":
		edit = False
		changeMode()
	elif key == "C":
		edit = True
		freq = freq + SEEKW
		inFreq = freqString()
		updateLcd()
	elif key == "D":
		edit = True
		freq = freq - SEEKW
		inFreq = freqString()
		updateLcd()
	else:
		if edit == False:
			inFreq = ""
		edit = True
		inFreq = inFreq + key
		updateLcd()


try:
	changeFreq()
	keypad.registerKeyPressHandler(handleKeyPress)

	while(True):
		print("keypad: sleeping...")
		time.sleep(0.2)
except:
	print("keypad: cleaning up")
	keypad.cleanup()
	clearLcd()
