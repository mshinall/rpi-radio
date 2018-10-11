#!/usr/bin/python

import sys
import I2C_LCD_driver
from pad4pi import rpi_gpio
import time
import subprocess
import signal
import os
import shlex

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
MAX_FREQ_LENGTH = 9

freq = 162.4750
inFreq = str(freq)
midx = 0
mode = MODES[midx]
mname = MNAMES[midx]
mband = MBANDS[midx]
sdrMode = SDR_MODES[midx]
edit = False
process1 = 0
process2 = 0

mylcd = I2C_LCD_driver.lcd()
factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=MATRIX, row_pins=ROWS, col_pins=COLS)

def freqString():
	return '{:.4f}'.format(freq).rjust(9)

def inFreqFloat():
	try:
		return float(inFreq)
	except:
		return float(inFreq + ".0000")

def clearLcd():
	global mylcd
	mylcd.lcd_clear()

def updateRadio():
	global process1, process2

	"""
	if process1.pid != 0:
		os.kill(process1.pid, signal.SIGINT)
	if process2.pid != 0:
		os.kill(process2.pid, signal.SIGINT)
	"""

	"""
	subprocess.Popen(shlex.split("mkfifo /tmp/pipe", shell=True))
	process1 = subprocess.Popen(shlex.split("rtl_fm -f {0}M -M {1} -s 200K -l 1 -r 48K >> /tmp/pipe"), shell=True)
	process2 = subprocess.Popen(shkex.split("aplay -t raw -r 48000 -f S16_LE /tmp/pipe"), shell=True)
	"""
	str1 = "rtl_fm -f " + freqString() + "M -M " + SDR_MODES[midx] + " -s 200K -l 1 -r 48K"
	str2 = "aplay -t raw -r 48000 -f S16_LE"
	print(str1 + " | " str2)
	process1 = subprocess.Popen(shlex.split(str1), SDR_MODES[midx])), stdout=subprocess.PIPE)
	process2 = subprocess.Popen(shkex.split(str2), stdin=process1.stdout)

def checkFreq():
	global freq
	if freq > MAX_FREQ:
		freq = MAX_FREQ
	elif freq < MIN_FREQ:
		freq = MIN_FREQ

def changeFreq():
	checkFreq()
	updateLcd()
	updateRadio()

def changeMode():
	global midx, mode, mname, mband, sdrMode

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
	global mylcd, freq, mode, edit

	clearLcd()

	if edit == True:
		mylcd.lcd_display_string(inFreq, 1, 0)
		mylcd.lcd_display_string("*", 1, 15)
	else:
		mylcd.lcd_display_string(freqString(), 1, 0)

	mylcd.lcd_display_string("MHz", 1, 10)
	mylcd.lcd_display_string(mname, 2, 0)

def numericEntry(key):
	global edit, inFreq
	if edit == False:
		inFreq = ""
	edit = True
	if len(inFreq) < 9:
		inFreq = inFreq + key
	updateLcd()

def decimalEntry(key):
	global edit, inFreq
	edit = True
	if "." not in inFreq:
		inFreq = inFreq + "."
	updateLcd()

def backspaceEntry(key):
	global edit, inFreq, freq
	edit = True
	if len(inFreq) > 0:
		inFreq = inFreq[:len(inFreq) - 1]
	freq = inFreqFloat()
	updateLcd()

def changeFreqEntry(key):
	global edit, freq
	edit = False
	freq = inFreqFloat()
	changeFreq()

def changeModeEntry(key):
	global edit
	edit = False
	changeMode()

def seekUpEntry(key):
	global edit, freq, inFreq
	edit = True
	freq = freq + SEEKW
	checkFreq()
	inFreq = freqString()
	updateLcd()

def seekDownEntry(key):
	global edit, freq, inFreq
	edit = True
	freq = freq - SEEKW
	checkFreq()
	inFreq = freqString()
	updateLcd()

keyMap = {
	"#": backspaceEntry,
	"*": decimalEntry,
	"A": changeFreqEntry,
	"B": changeModeEntry,
	"C": seekUpEntry,
	"D": seekDownEntry
}

def handleKeyPress(key):
	if key in keyMap:
		handler = keyMap[key]
	else:
		handler = numericEntry
	handler(key);

	"""
	global freq, inFreq, mode, edit

	if key == "#":
		backspaceEntry()
	elif key == "*":
		decimalEntry()
	elif key == "A":
		changeFreqEntry()
	elif key == "B":
		changeModeEntry()
	elif key == "C":
		seekUpEntry()
	elif key == "D":
		seekDownEntry()
	else:
		numericEntry(key)
	"""
try:
	changeFreq()
	keypad.registerKeyPressHandler(handleKeyPress)

	while(True):
		#print("keypad: sleeping...")
		time.sleep(0.2)
except:
	#print("keypad: cleaning up")
	keypad.cleanup()
	clearLcd()
