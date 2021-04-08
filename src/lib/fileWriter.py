#!/bin/python3

import rx
import soundfile as sf

class FileWriter(rx.core.typing.Observer):
    def __init__(self, outputDir, date, samplerate, audioDataSubject):
        fileName = outputDir + "/" + date.datetime.now().astimezone().replace(microsecond=0).isoformat() + ".wav"
        self.audioFile = sf.SoundFile(fileName, mode='w', samplerate=48000, format="WAV", channels=1, subtype="PCM_16")
        self.metaFile = open(outputDir + "/" + date.datetime.now().astimezone().replace(microsecond=0).isoformat() + ".meta", "wt")
        self.subscription = audioDataSubject.subscribe(self)
        self.end = None
        print(fileName)


    def on_next(self, val: tuple):
        if self.end != None:
            if self.end < val[2]:
                print("self destruct")
                self.subscription.dispose()
                del(self.subscription)
                self.on_completed()
                return
        self.audioFile.write(val[1])
        self.metaFile.write(str(val[0]) + "\n")

    def on_error(self, error):
        print(error)

    def on_completed(self):
        print("file closed")
        self.audioFile.close()
        self.metaFile.close()

    def setEnd(self, end):
        self.end = end

    def __del__(self):
        print("destructor used")
        self.audioFile.close()
        self.metaFile.close()