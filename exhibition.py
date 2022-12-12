#!/usr/bin/python
# encoding: utf-8

from pepper.unirobot import Pepper
import time
import os
import random
random.seed(42)


def main(robot):
    while True:
        robot.show_web('http://10.50.10.194:8000/')
        robot.stop_behaviour()
        robot.detect_touch()
        robot.start_behavior('User/toila-442fc7/behavior_1')
        time.sleep(2)
        while True:
            try:
                robot.recordSound(4)
                utter = robot.speech_to_text(audio_file = 'speech.wav',lang='vi-VN').lower()
                
                print(utter)
                if u'tạm biệt' in utter:
                    break
                mp3_file_abspath_params = os.popen('python3 communication_python3.py --text u"{}"'.format(utter.encode('utf-8'))).read().split('\n')[0]
                mp3_file, abspath, title, size, quantity, floor, intent = mp3_file_abspath_params.split('@')  
                
                if title != '':
                    robot.show_web('http://10.50.10.194:8000/?title={}&size={}&quantity={}&floor={}'.format(title, size, quantity, floor))
                
                robot.upload_file(mp3_file)
                robot.audio_service.playFile('/home/nao/' + abspath)
                time.sleep(1)
                
                if intent == 'item.confirm.yes':
                    break 
            except :
                pass

if __name__ == '__main__':
    robot = Pepper('10.51.5.248', 9559)
    robot.set_volume(80)
    robot.reset_tablet()
    # robot.show_web('http://10.50.10.194:8000/')
    main(robot)     