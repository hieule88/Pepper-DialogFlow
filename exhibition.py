#!/usr/bin/python
# encoding: utf-8

from pepper.unirobot import Pepper
import time
import os
import random
random.seed(42)


def main(robot):
    while True:
        robot.show_web('https://d5a7dc652b0958.lhr.life')
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
                mp3_file, abspath, title, size, quantity, floor = mp3_file_abspath_params.split('@')  
                
                robot.show_web('https://d5a7dc652b0958.lhr.life/?title={}&size={}&quantity={}&floor={}'.format(title, size, quantity, floor))
                robot.upload_file(mp3_file)
                time.sleep(2)
                robot.audio_service.playFile('/home/nao/' + abspath)
            except :
                pass

if __name__ == '__main__':
    robot = Pepper('10.51.5.141', 9559)
    robot.set_volume(60)
    robot.reset_tablet()
    # robot.show_web('https://stackoverflow.com/questions/1622793/django-cookies-how-can-i-set-them')
    main(robot)     