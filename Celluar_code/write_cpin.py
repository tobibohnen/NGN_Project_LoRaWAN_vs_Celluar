#!/usr/bin/python
# Script for activating the SIM card and GPS functionality of the Waveshare hat
import RPi.GPIO as GPIO
import serial
import time

ser = serial.Serial("/dev/ttyUSB2",115200)
ser.flushInput()

power_key = 6
rec_buff = ''

def send_at(command,back,timeout):
	rec_buff = ''
	ser.write((command+'\r\n').encode())
	time.sleep(timeout)
	if ser.inWaiting():
		time.sleep(0.01 )
		rec_buff = ser.read(ser.inWaiting())
	if back not in rec_buff.decode():
		print(command + ' ERROR')
		print(command + ' back:\t' + rec_buff.decode())
		return 0
	else:
		print(rec_buff.decode())
		return 1


try:
	send_at('AT+CPIN=CENSORED', 'OK', 1)
	send_at('AT+CGPS=1,1', 'OK', 1)
except :
	if ser != None:
		ser.close()
	GPIO.cleanup()
