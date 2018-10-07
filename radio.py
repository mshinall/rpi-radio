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
SEEKW = 0.0125
MAX_FREQ = 1700.0000
MIN_FREQ = 25.0000

freq = 120.0000
inFreq = "120.0000"
midx = 0
mode = MODES[midx]
mname = MNAMES[midx]
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

def changeFreq():
	global freq
	freq = freqFloat()
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

	midx += 1
	if midx >= len(MODES):
		midx = 0
	mode = MODES[midx]
	mname = MNAMES[midx]
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
		changeFreq()
	elif key == "B":
		edit = False
		changeMode()
	elif key == "C":
		edit = True
		freq = freq + SEEKW
		updateLcd()
	elif key == "D":
		edit = True
		freq = freq - SEEKW
		updateLcd()
	else:
		if edit == False:
			inFreq = ""
		edit = True
		inFreq = inFreq + key
		updateLcd()



changeFreq()
keypad.registerKeyPressHandler(handleKeyPress)

try:
	while(True):
		#print("keypad: sleeping...")
		time.sleep(0.2)
except:
	#print("keypad: cleaning up")
	keypad.cleanup()
	clearLcd()
