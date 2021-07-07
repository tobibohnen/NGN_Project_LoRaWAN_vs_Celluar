# Subscribes to the central MQTT broker on all ngn/# topics and writes received
# messages into a log file.
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish


broker = "192.168.178.X"
brokerauth = {'username': CENSORED, 'password': CENSORED}
topic = "ngn/#"

while True:
  msg = subscribe.simple(topic, hostname=broker, auth=brokerauth)
  output = f"{msg.topic}: {str(msg.payload.decode('utf-8'))}"
  print(output)
  with open("all_payload.txt", "a") as myfile:
    myfile.write(f"\n{output}\n")
