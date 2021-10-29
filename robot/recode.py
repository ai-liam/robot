#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pyaudio import PyAudio, paInt16 
import numpy as np 
from datetime import datetime 
import wave

#from IPython.display import Audio, Javascript

class Recoder:
    def __init__(self, rate=16000):
        self.NUM_SAMPLES = 2000      #pyaudio内置缓冲大小
        self.SAMPLING_RATE = rate # 8000    #取样频率
        self.LEVEL = 500         #声音保存的阈值
        self.COUNT_NUM = 20      #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
        self.SAVE_LENGTH = 8         #声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
        self.TIME_COUNT = 60 #60     #录音时间，单位s ?
        self.save_buffer = []
        self.is_recode = False
        
    def pause(self):
        self.is_recode = False
    
    def restart(self):
        self.is_recode = True
    
    def stop(self):
        self.is_recode = False
        
    def save(self,file_name):
        wf = wave.open(file_name, 'wb') 
        wf.setnchannels(1) 
        wf.setsampwidth(2) 
        wf.setframerate(self.SAMPLING_RATE) 
        wf.writeframes(np.array(self.save_buffer).tostring()) 
        # wf.writeframes(self.save_buffer.decode())
        wf.close() 

    def loops(self):
        # print time_count
        # 读入NUM_SAMPLES个取样
        string_audio_data = self.stream.read(self.NUM_SAMPLES) 
        # 将读入的数据转换为数组
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        # 计算大于LEVEL的取样的个数
        large_sample_count = np.sum( audio_data > self.LEVEL )
        #print(np.max(audio_data))
        # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
        if large_sample_count > self.COUNT_NUM:
            self.save_count = self.SAVE_LENGTH 
        else: 
            self.save_count -= 1
        if self.save_count < 0:
            self.save_count = 0 

        if self.save_count > 0 : 
        # 将要保存的数据存放到save_buffer中
            #print  save_count > 0 and time_count >0
            self.save_buffer.append( string_audio_data ) 
        else: 
        #print save_buffer
        # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
            print("没有获得数据")
            #print "debug"
            # if len(self.save_buffer) > 0 : 
            #     print("Recode a piece of  voice successfully!")
            #     return True

    def recode(self,time_count=60):
        print("开始录音")
        self.is_recode = True
        pa = PyAudio() 
        self.stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True, 
            frames_per_buffer=self.NUM_SAMPLES) 
        self.save_count = 0 
        self.save_buffer = [] 
        while (self.is_recode):
            time_count -= 1
            self.loops()
            if time_count==0:
                print("录音结束") 
                if len(self.save_buffer)>0:
                    print("Recode a piece of  voice successfully!!")
                    return True
                else:
                    return False
        

if __name__ == "__main__":
    r= Recoder()
    r.recode(60)
    r.save("temp.wav")