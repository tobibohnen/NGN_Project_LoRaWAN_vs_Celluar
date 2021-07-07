#!/usr/bin/python
# Filters Network information retrieved from the waveshare hat and publishes it
# to th central MQTT Broker every minute.
import RPi.GPIO as GPIO
import serial
from datetime import datetime
import time
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish


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
		return rec_buff
	if back not in rec_buff.decode():
		print(command + ' ERROR')
		print(command + ' back:\t' + rec_buff.decode())
		return 0
	else:
		print(rec_buff.decode())
		return 1

auth = {'username': CENSORED, 'password':CENSORED}


while True:
  try:
    rec_buff = send_at('AT+CPSI?', '+CPSI', 1)
    print(rec_buff.decode())
    payload = rec_buff.decode().rsplit(',', 5)
    system_mode = rec_buff.decode().split(',', 2)[0].split(':', 2)[1]
    print(payload[0])
    rec_buff = send_at('AT+CGPSINFO', '+CGPSINFO', 1)
    gps = rec_buff.decode().split(',', 4)
    gps[0] = gps[0].split(':', 2)[1]
    print("BLUB", gps[0], gps[1], gps[2], gps[3])
    longitude = f"{gps[0]}{gps[1]}"
    latitude = f"{gps[2]}{gps[3]}"
    rsrq = payload[2]
    rsrp = payload[3]
    rssi = payload[4]
    rssnr = payload[5].split("\n")[0]
    sysNow = datetime.now().strftime("%m/%d/%Y - %H:%M:%S").strip()
    send_msg = f"{sysNow}, {longitude}, {latitude}, {system_mode}, {rsrq}, {rsrp}, {rssi}, {rssnr}"
    print("MSG", send_msg)
    publish.single("ngn/lte", send_msg, hostname="CENSORED", auth=auth)
    time.sleep(60)
  except :
    pass
