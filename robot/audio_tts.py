#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 语音播报模块
import pyttsx3 
import time 

class AudioTTS:
    def __init__(self ):
        # 模块初始化
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting.premium")
        #self.engine.setProperty('rate', 105)

    def say(self,text="你好"):
        print('准备开始语音播报...')
        self.engine.say(text)
        # 等待语音播报完毕 
        self.engine.runAndWait()
        #self.engine.stop()
        time.sleep(1)
        
    def speak(self,text="你好"):
        print('准备开始语音播报...2')
        self.engine.speak(text)
        time.sleep(1)

    def save(self,text="你好",file_dir="temp.mp3"):
        print('准备开始语音保存...')
        #engine.say(text)
        # 等待语音播报完毕 
        self.engine.save_to_file(text, file_dir)
        self.engine.runAndWait()

    def say_and_save(self,text="你好",file_dir="temp.mp3"):
        print('准备开始语音播报...')
        self.engine.say(text)
        self.engine.runAndWait()
        print('准备开始语音保存...')
        # 等待语音播报完毕 
        self.engine.save_to_file(text, file_dir)
        self.engine.runAndWait()
        #self.engine.stop()