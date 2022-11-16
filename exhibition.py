#!/usr/bin/python
# encoding: utf-8

from pepper.unirobot import Pepper
import time
from datetime import datetime
import os
import random
random.seed(42)


def main(robot):
    while True:
        robot.stop_behaviour()
        robot.detect_touch()
        robot.start_behavior('User/toila-442fc7/behavior_1')
        time.sleep(2)
        robot.changeVoice(volume= 200, speed= 80 ,shape= 150)
        robot.show_image('/home/hieule/Downloads/IMG_0606.JPG')
        while True:
            try:
                robot.recordSound(4)
                utter = robot.speech_to_text(audio_file = 'speech.wav',lang='vi-VN').lower()
                print(utter)
                if u'tạm biệt' in utter:
                    break
                mp3_file = os.popen('python3 communication_python3.py --text u"{}"'.format(utter.encode('utf-8'))).read().split('\n')[0]
                robot.audio_service.playFile(mp3_file)
            except :
                pass

if __name__ == '__main__':
    robot = Pepper('192.168.123.250', 9559)
    robot.set_volume(100)
    main(robot)     