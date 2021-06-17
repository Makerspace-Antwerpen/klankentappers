#!/bin/python3

import paho.mqtt.client as mqtt
import json
import threading
import time


class TBConnection:
    def __init__(self, interval, host, port, secret):
        self.client = mqtt.Client()
        self.client.username_pw_set(secret)
        self.client.connect(host, port)
        self.client.loop_start()
        self.interval = interval
        self.telemetry = dict()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.sendThread)
        self.end = False

    def addTelemetry(self, name, value, telSet="default"):
        self.lock.acquire()
        if (self.telemetry[telSet] == None):
            self.telemetry[telSet] = dict()
        self.telemetry[telSet][name] = value
        self.lock.release()

    def sendTelemetry(self, telSet="default"):
        self.lock.acquire()
        sendJson = json.dumps(self.telemetry[telSet])
        self.lock.release()
        self.client.publish("v1/devices/me/telemetry", sendJson)

        
        
    
    def sendThread(self):
        while True:
            time.sleep(self.interval)
            self.sendTelemetry()
    
    def startTelemetry(self):
        self.thread.start()
    def stopTelemetry(self):
        self.end = True
        self.thread.join()

    
    
    