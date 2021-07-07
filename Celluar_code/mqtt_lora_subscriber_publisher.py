# Subscribes to the MQTT Broker of The Things Network to retrieve and filter
# the mDot data and publishes those into the central MQTT Broker.

from datetime import datetime
import time
import json
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish


broker = "192.168.178.38"
brokerauth = {'username': CENSORED, 'password': CENSORED}
port = 1883
topic = "ngn/lora"
loratopic = 'v3/hello-mdot@ttn/device s/dev4/up'
lorabroker = "eu1.cloud.thethings.network"
loraauth = {'username': CENSORED, 'password': CENSORED}

print(f"Messages are published on topic -> CTRL + C to shutdown")


while True:
  msg = subscribe.simple(loratopic, hostname=lorabroker, auth=loraauth)
  print(f"{msg.topic}: {msg.payload}")
  json_msg = json.loads(msg.payload)
  try:
    uplink = json_msg['uplink_message']
    metadata = uplink['rx_metadata'][0]
    snr = metadata['snr']
    rssi = metadata['rssi']
    channel_rssi = metadata['channel_rssi']
    air_time = uplink['consumed_airtime']
    send_value = uplink['decoded_payload']['var']
    received_at = datetime.now()
    received_at = received_at.strftime("%m/%d/%Y - %H:%M:%S")
    with open("lora_payload.txt", "a") as myfile:
        myfile.write(f"\n{received_at}: \n{msg.payload}\n")
    payload = f"{snr}, {rssi}, {channel_rssi}, {air_time}, {send_value}, {received_at}"
    publish.single(topic, payload, hostname=broker, auth=brokerauth)
  except KeyError:
    pass
