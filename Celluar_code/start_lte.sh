#!/bin/sh
# Cron script to automatically get the wwan0 interface from the waveshare hat up and running
# Method for getting wwan interface up is described here: https://www.raspberrypi.org/forums/viewtopic.php?t=224355
sleep 40
python3 /home/pi/NGN/write_cpin.py
sleep 5
sudo ip link set wwan0 down
echo 'Y' | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set wwan0 up
sleep 10
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='web.vodafone.de',ip-type=4" --client-no-release-cid
sleep 10
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='web.vodafone.de',ip-type=4" --client-no-release-cid
sleep 5
sudo qmicli -p -d /dev/cdc-wdm0 --device-open-net='net-raw-ip|net-no-qos-header' --wds-start-network="apn='web.vodafone.de',ip-type=4" --client-no-release-cid
sleep 5
sudo udhcpc -i wwan0
sleep 5
python3 /home/pi/NGN/get_cspi.py
