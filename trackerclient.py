# Receive absolute coordinate of servo x, y, and mouth

import servo
import numpy as np
import paho.mqtt.client as mqtt


class TrackerClient:
    client = mqtt.Client()

    addr_broker = "192.168.1.15"
    xprev = 1500
    yprev = 1500

    def __init__(self):
        self.srv = servo.ServoController()

    def on_connect(self, client, userdata, flags, response):
        print("Connected with result code "+str(response))
        client.subscribe("position/x")
        client.subscribe("position/y")
        client.subscribe("position/mouth")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        if msg.topic == "position/x":
            x = int(msg.payload)
            self.srv.moveAbsoluteX(x)
        elif msg.topic == "position/y":
            y = int(msg.payload)
            self.srv.moveAbsoluteY(y)
        elif msg.topic == "position/mouth"
            m = int(msg.payload)
            self.srv.moveAbsoluteMouth(m)
        else:
            pass

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.addr_broker, 1883, 60)
        self.client.loop_forever()

    def startTracking(self):
        self.connect()

    def stopTracking(self):
        pass

if __name__ == "__main__":

    tracker = TrackerClient()
    tracker.startTracking()
    while True:
        i = raw_input()
        if i == "c":
            tracker.stopTracking()
            break
