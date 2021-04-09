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

    def addTelemetry(self, name, value):
        self.lock.acquire()
        self.telemetry[name] = value
        self.lock.release()

    def sendTelemetry(self):
        self.lock.acquire()
        sendJson = json.dumps(self.telemetry)
        self.lock.release()
        self.client.publish("v1/devices/me/telemetry", sendJson)
        
        
    
    def sendThread(self):
        lastTime = time.time()
        while True:
            time.sleep(1)
            if self.end:
                break
            if lastTime + self.interval < time.time():
                self.sendTelemetry()
    
    def startTelemetry(self):
        self.thread.start()
    def stopTelemetry(self):
        self.end = True
        self.thread.join()

    
    
    