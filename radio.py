#!/usr/bin/python

import sys
import I2C_LCD_driver
from pad4pi import rpi_gpio
import time

MATRIX = [['1','2','3','A'],
		  ['4','5','6','B'],
		  ['7','8','9','C'],
		  ['*','0','#','D']]

#BCM numbering
COLS = [4,17,27,22]
ROWS = [6,13,19,26]
MODES = ["NFM", "WFM", "AM", "LSB", "USB"]
MNAMES = ["Narrow FM", "Wide FM", "AM", "Lower SSB", "Upper SSB"]

freq = "120.0000"
midx = 0
mode = MODES[midx]
mname = MNAMES[midx]
edit = False

mylcd = I2C_LCD_driver.lcd()
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=MATRIX, row_pins=ROWS, col_pins=COLS)

def clearLcd():
	global mylcd
	mylcd.lcd_clear()

def updateRadio():
	print("updateRadio: freq=" + freq + " mode=" + mode)

def changeFreq():
	global freq
	iFreq = int(float(freq))
	if iFreq > 1700:
		freq = "1700.0000"
	elif iFreq < 25:
		freq = "25.0000"

	freq = freq[:10]

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
	mylcd.lcd_display_string('{:.4f}'.format(float(freq[:10])).rjust(9), 1, 0)
	mylcd.lcd_display_string("Mhz", 1, 13)
	if edit == True:
		mylcd.lcd_display_string("*", 2, 15)
	mylcd.lcd_display_string(mname, 2, 0)


def handleKeyPress(key):
	global freq
	global mode
	global edit

	if key == "#":
		edit = True
		freq = freq[:len(freq) - 1]
		updateLcd()
	elif key == "*":
		edit = True
		freq = freq + "."
		updateLcd()
	elif key == "A":
		edit = False
		changeFreq()
	elif key == "B":
		edit = False
		changeMode()
	else:
		if edit == False:
			freq = ""
		edit = True
		freq = freq + key
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
