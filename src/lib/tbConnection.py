#!/bin/python3

import paho.mqtt.client as mqtt
import json
import threading
import time


class TBConnection:
    def on_connect(self, client, userdata, flags, rc):
        '''
        we add a callback function in order to capture a bad connection due to e.g. non-functional DNS servers
        '''
        if rc == 0:
            self.client.connected_flag = True  # set flag
            print("connected OK")
        else:
            print("Bad connection Returned code=", rc)

    def __init__(self, interval, host, port, secret):
        self.client = mqtt.Client()
        self.client.connected_flag = False  # create flag in class
        self.client.username_pw_set(secret)
        self.client.on_connect = self.on_connect
        self.client.connect(host, port)
        self.client.loop_start()
        while not self.client.connected_flag:  # wait in loop
            print("No connection established yet")
            time.sleep(1)
        self.interval = interval
        self.telemetry = dict()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.sendThread)
        self.end = False

    def addTelemetry(self, name, value, telSet="default"):
        self.lock.acquire()
        if not telSet in self.telemetry.keys():
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
