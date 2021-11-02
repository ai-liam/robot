import sys, os

sys.path.append('./data/speaker/external-libraries')

import tkinter as tk
from PIL import Image, ImageTk
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from speechbrain.dataio.dataio import read_audio
import threading

# self
from robot.recode import Recoder  # self

# from robot.audio_tts import AudioTTS

audio_file = "data/speaker/temp/recoder1.wav"


# tts = AudioTTS()

def tts_say(text):
    def __say():
        try:
            from robot.audio_tts import AudioTTS
            tts = AudioTTS()
            tts.say(text)
        finally:
            pass

    try:
        T = threading.Thread(target=__say, daemon=True)
        T.start()
    finally:
        pass


class Application(tk.Frame):
    def __init__(self, master=tk.Tk(), width=800, height=800):
        tk.Frame.__init__(self, master)
        self.width = width
        self.height = height
        self.create_widgets()
        # other
        self.pack()
        self.widgets_pack()
        # ai
        self.recoder = Recoder()

        self.show_plt()

        pygame.mixer.init()  # initialise the pygame
        # self.tts = AudioTTS()

    def create_widgets(self):
        self.canvas_img = tk.Canvas(self, height=180, width=self.width, bg="white")
        self.img = ImageTk.PhotoImage(Image.open("data/speaker/ui/vno1.jpeg"))
        self.canvas_img.create_image(int(self.width * 0.5), 100, anchor='center', image=self.img)  # n center,nw,ne
        self.canvas_img.image = self.img  # 绑定图片

        self.var_in = tk.StringVar()
        self.var_out = tk.StringVar()
        self.label_name = tk.Label(self.master, text='您好，我是虚拟人1号。很高兴为您服务！', bg='green', font=('Arial', 12))
        self.button_recode = tk.Button(self.master, text='录音', command=self.recode_start)
        self.button_recode_stop = tk.Button(self.master, text='停止', command=self.recode_stop)
        self.button_recode_play = tk.Button(self.master, text='播放', command=self.recode_play)
        self.label_info_in = tk.Label(self.master, text='输入信息:', textvariable=self.var_in, bg='yellow',
                                      font=('Arial', 12))  # textvariable=self.var , width=self.width
        self.label_info_out = tk.Label(self.master, text='输出信息:', textvariable=self.var_out, bg='white',
                                       font=('Arial', 12))

        self.label_us_name = tk.Label(self.master, text='声纹主人的昵称:', font=('Arial', 14))
        self.input_name = tk.Entry(self.master, text="爸爸", font=('Arial', 14), width=20)
        self.input_name.insert(0, "爸爸")
        self.button_input = tk.Button(self.master, text='录入新声纹', command=self.recode_play)
        self.button_test = tk.Button(self.master, text='测试', command=self.event_test)

    def widgets_pack(self):
        self.canvas_img.pack(side='top')  # place(x=0, y=0)

        self.label_name.place(x=int(self.width * 0.5 - 100), y=200)  # pack(side='top') #
        self.button_recode.place(x=300, y=230)
        self.button_recode_stop.place(x=400, y=230)  # pack()
        self.button_recode_play.place(x=500, y=230)
        self.label_info_in.place(x=0, y=280)
        self.label_info_out.place(x=0, y=320)

        self.label_us_name.place(x=100, y=382)
        self.input_name.place(x=250, y=380)
        self.button_input.place(x=450, y=380)
        self.button_test.place(x=580, y=380)

    def event_test(self):
        tts_say("主人，今天天气很好，适合和朋友出去玩！")

    def play(self, file):
        self.show_plt()

        def __play():
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(loops=0)

        T = threading.Thread(target=__play)
        T.start()

    def __recode_start(self):
        self.recoder.recode(100)  # 声音长度

    def recode_start(self):
        print("Start recode")
        self.var_in.set('Start recode')
        T = threading.Thread(target=self.__recode_start)
        T.start()
        # 录音：今天天气怎么样？
        # self.recoder.recode(60)# 声音长度

    def recode_play(self):
        print("Play")
        self.play(audio_file)

    def recode_stop(self):
        print("Stop recode")
        self.recoder.stop()
        self.var_out.set('Stop recode')
        self.recoder.save(audio_file)

    def show_plt(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(7, 3),
                     dpi=100)
        # list of squares
        # y = [i ** 2 for i in range(101)]
        # adding the subplot
        plot1 = fig.add_subplot(211)  # 111
        # 原始音频
        clean = read_audio(audio_file).squeeze()
        # plotting the graph :
        plot1.plot(clean)  # 数值 #plot1.plot(y)

        plot2 = fig.add_subplot(212)
        plot2.specgram(clean, Fs=16000)  # specgram()函数用于绘制频谱图。
        # plot2.xlabel('Time')
        # plot2.ylabel('Frequency')

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas_plt = FigureCanvasTkAgg(fig, master=self.master)
        canvas_plt.draw()
        # placing the canvas on the Tkinter window
        canvas_plt.get_tk_widget().place(x=int(self.width * 0.5 - 350), y=500)
        # creating the Matplotlib toolbar
        # toolbar = NavigationToolbar2Tk(canvas,self)
        # toolbar.update()
        # # placing the toolbar on the Tkinter window
        # self.canvas_plt.get_tk_widget().pack()


app = Application()
# 设置窗口
app.master.title('虚拟人1号（Virtual Human No. 1）')
app.master.geometry('800x800')

# 主消息循环:
app.mainloop()
