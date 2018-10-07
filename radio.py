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
MODES = ["NFM", "WFM", "AM ", "LSB", "USB"]

freq = "120.0000"
midx = 0
mode = MODES[midx]
edit = False

mylcd = I2C_LCD_driver.lcd()
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=MATRIX, row_pins=ROWS, col_pins=COLS)

def updateRadio():
	adjustFreq()
	updateLcd()
	print("updateRadio: freq=" + freq + " mode=" + mode)

def adjustFreq():
	global freq
	iFreq = int(float(freq))
	if iFreq > 1700:
		freq = "1700.0000"
	elif iFreq < 25:
		freq = "25.0000"

	freq = freq[:10]

def changeMode():
	global midx
	midx += 1
	if midx >= len(MODES):
		midx = 0
	elif midx < 0:
		midx = len[MODES]

	mode = MODES[midx]
	updateLcd()

def updateLcd():
	global mylcd
	global freq
	global mode

	mylcd.lcd_clear()
	mylcd.lcd_display_string(freq, 1, 0)
	mylcd.lcd_display_string("Mhz", 1, 13)
	if edit == True:
		mylcd.lcd_display_string("edit", 2, 12)
	mylcd.lcd_display_string(mode, 2, 0)


def handleKeyPress(key):
	global freq
	global mode

	if key == "#":
		edit = True
		freq = freq[:len(freq) - 1]
	elif key == "*":
		edit = True
		freq = freq + "."
	elif key == "A":
		edit = False
		updateRadio()
	elif key == "B":
		edit = True
		changeMode()
	else:
		edit = True
		freq = freq + key

	updateLcd()

updateLcd()
keypad.registerKeyPressHandler(handleKeyPress)

try:
	while(True):
		#print("keypad: sleeping...")
		time.sleep(0.2)
except:
	#print("keypad: cleaning up")
	keypad.cleanup()
