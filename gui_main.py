import sys,os

sys.path.append('./data/speaker/external-libraries')

import tkinter as tk
from PIL import Image, ImageTk
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from speechbrain.dataio.dataio import read_audio
import threading

#self
from robot.recode import Recoder # self
#from robot.audio_tts import AudioTTS

audio_file = "data/speaker/temp/recoder1.wav"

#tts = AudioTTS()

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
        
        #self.show_plt()
        pygame.mixer.init()# initialise the pygame
        #self.tts = AudioTTS()

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

    def play(self,file):
        # self.show_plt()
        # def __play():
        #     pygame.mixer.music.load(file)
        #     pygame.mixer.music.play(loops=0)
        # T = threading.Thread(target=__play)
        # T.start()
        self.tts_say("主人，今天天气很好，适合和朋友出去玩！")

    def tts_say(self,text):
        def __say():
            try:
                from robot.audio_tts import AudioTTS
                tts = AudioTTS()
                tts.say(text)
            except:
                pass
        try:
            T = threading.Thread(target=__say,daemon=True)
            T.start()
        except:
                pass   

    def __recode_start(self):
        self.recoder.recode(100)# 声音长度

    def recode_start(self):
        print("Start recode")
        self.var.set('Start recode')
        T = threading.Thread(target=self.__recode_start)
        T.start()
        # 录音：今天天气怎么样？
        #self.recoder.recode(60)# 声音长度

    def recode_play(self):
        print("Play")
        self.play(audio_file)

    def recode_stop(self):
        print("Stop recode")
        self.recoder.stop()
        self.var.set('Stop recode')
        self.recoder.save(audio_file)

    def show_plt(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(5, 5),
                    dpi=100)
        # list of squares
        #y = [i ** 2 for i in range(101)]
        # adding the subplot
        plot1 = fig.add_subplot(211) # 111
        # 原始音频
        clean = read_audio(audio_file).squeeze()
        # plotting the graph :
        plot1.plot(clean) #数值 #plot1.plot(y)

        plot2 = fig.add_subplot(212)
        plot2.specgram(clean,Fs=16000)# specgram()函数用于绘制频谱图。
        #plot2.xlabel('Time')
        #plot2.ylabel('Frequency')

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()


app = Application()
# 设置窗口
app.master.title('虚拟人1号（Virtual Human No. 1）')
app.master.geometry('800x800')

# 主消息循环:
app.mainloop()
