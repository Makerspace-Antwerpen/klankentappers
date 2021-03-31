#!/bin/python3

import paho.mqtt.client as mqtt
import json


class TBConnection:
    def __init__(self, host, port, secret):
        self.client = mqtt.Client()
        self.client.username_pw_set(secret)
        self.client.connect(host, port)
        self.client.loop_start()
        self.telemetry = dict()

    def addTelemetry(self, name, value):
        self.telemetry[name] = value

    def sendTelemetry(self):
        print(self.telemetry)
        sendJson = json.dumps(self.telemetry)
        self.client.publish("v1/devices/me/telemetry", sendJson)
        self.telemetry.clear()
    
    
    