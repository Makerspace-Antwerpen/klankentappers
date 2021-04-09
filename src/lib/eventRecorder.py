#!/bin/python3

import rx
import time
import threading


class EventRecorder(rx.core.typing.Observer):
    def __init__(self, detectFunction, cooldownTime, createFileWriter):
        self.eventDetector = detectFunction
        self.eventBusy = False
        self.createFileWriter = createFileWriter
        self.lastTrigger = 0
        self.cooldownTime = cooldownTime
        self.fileWriter = None
        self.lock = threading.Lock()
    
    def on_next(self, val: tuple):
        self.lock.acquire()
        eventTrigger = self.eventDetector(val, self.eventBusy)

        if eventTrigger:
            self.lastTrigger = time.time()

        if not self.eventBusy and eventTrigger:
            self.eventBusy = True
            self.fileWriter = self.createFileWriter()

        if self.eventBusy and (self.lastTrigger + self.cooldownTime) < time.time():
            self.eventBusy = False
            print("dispose")
            self.fileWriter.setEnd(val[2])
            self.fileWriter = None
        self.lock.release() 

    def on_completed(self):
        print("audioSubject completed")

    def on_error(self, error):
        print(error)
