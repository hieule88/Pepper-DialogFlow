#!/usr/bin/python
# encoding: utf-8

from pepper.unirobot import Pepper
import time
import os
import random
random.seed(42)

def main(robot):
    robot.changeVoice(volume= 70, speed= 80 ,shape= 150)
    robot.set_volume(50)
    # robot.sound_detect_service.setParameter("Sensitivity", 0.7)
    streaming = True

    utter = robot.listen_to("pepper")
    print(utter)

    while streaming:
        try:
            robot.recordSound(4)
            utter = robot.speech_to_text(audio_file = 'speech.wav',lang='vi-VN').lower()
            # utter = robot.listen_to("pepper")
            print(utter)
            if u"pepper" in utter:
                robot.sound_detect_service.setParameter("Sensitivity", 0.9)
                mymy_active = True
                robot.start_behavior('System/boot-config/animations/hello')
                time.sleep(1)
                robot.audio_service.playFile('/home/nao/xinchao.mp3')
                while mymy_active:
                    try:
                        robot.recordSound(4)
                        utter = robot.speech_to_text(audio_file = 'speech.wav',lang='vi-VN')
                        streaming, mymy_active = robot.react_command(utter)
                    except:
                        continue
            # robot.sound_detect_service.setParameter("Sensitivity", 0.7)
        except:
            continue

if __name__ == '__main__':
    robot = Pepper('10.51.5.181', 9559)
    main(robot)