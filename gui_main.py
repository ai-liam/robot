import sys,os

sys.path.append('./data/speaker/external-libraries')

import tkinter as tk
#from tkinter import *
from PIL import Image, ImageTk
#import pygame

from robot.recode import Recoder # self

audio_file = "data/speaker/temp/recoder1.wav"

class Application(tk.Frame):
    def __init__(self, master=None,width=800,height=600):
        tk.Frame.__init__(self, master)
        self.width = width
        self.height= height
        self.create_widgets()
        # other
        self.pack()
        self.widgets_pack()
        # ai
        self.recoder = Recoder()
        #pygame.mixer.init()# initialise the pygame

    def create_widgets(self):
        self.canvas = tk.Canvas(self, height=200, width=500)
        self.img = ImageTk.PhotoImage(Image.open("data/speaker/ui/vno1.jpeg"))
        self.canvas.create_image(250, 100, anchor='center', image=self.img)  # n center,nw,ne
        self.canvas.image = self.img  # 绑定图片

        self.label_name = tk.Label(self, text='您好，我是虚拟人1号。很高兴为您服务！', bg='green', font=('Arial', 12), width=100, height=2)
        self.button_recode = tk.Button(self, text='录音', command=self.recode_start)
        self.button_recode_stop = tk.Button(self, text='停止', command=self.recode_stop)
        self.button_recode_play = tk.Button(self, text='播放', command=self.recode_play)
        self.input_name = tk.Entry(self)
        self.var = tk.StringVar()
        self.label_info = tk.Label(self, textvariable=self.var, bg='gray', font=('Arial', 12), width=100, height=2)

    def widgets_pack(self):
        self.canvas.pack()
        self.label_name.pack()
        self.input_name.pack()
        self.button_recode.pack()
        self.button_recode_stop.pack()
        self.button_recode_play.pack()
        self.label_info.pack()

    def recode_start(self):
        print("Start recode")
        self.var.set('Start recode')
        # 录音：今天天气怎么样？
        self.recoder.recode(60)# 声音长度

    def recode_play(self):
        print("Play")
        # pygame.mixer.music.load("audio_file")
        # pygame.mixer.music.play(loops=0)

    def recode_stop(self):
        print("Stop recode")
        self.var.set('Stop recode')
        self.recoder.save(audio_file)


app = Application()
# 设置窗口
app.master.title('虚拟人1号（Virtual Human No. 1）')
app.master.geometry('800x600')

# 主消息循环:
app.mainloop()
