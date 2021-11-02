import sys, os

sys.path.append('./data/speaker/external-libraries')

import tkinter as tk
from PIL import Image, ImageTk
import pygame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from speechbrain.dataio.dataio import read_audio
import threading
import time

# self
from robot.recode import Recoder  # self
import robot.speaker_main as sp

# from robot.audio_tts import AudioTTS

audio_file = "data/speaker/temp/recoder1.wav"
audio_file_ck = "data/speaker/temp/ck_master.wav"
audio_file_tts = "data/speaker/temp/tts_master.wav"

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
        T = threading.Thread(target=__say, daemon=False)
        T.start()
    finally:
        pass


class Application(tk.Frame):
    def __init__(self, master=tk.Tk(), width=800, height=800):
        tk.Frame.__init__(self, master)
        self.width = width
        self.height = height
        self.pack()
        self.create_widgets()
        self.widgets_pack()
        # other
        self.recoder = Recoder()
        # self.show_plt(audio_file)
        # init
        pygame.mixer.init()  # initialise the pygame

    def create_widgets(self):
        self.canvas_img = tk.Canvas(self, height=180, width=self.width, bg="white")
        self.img = ImageTk.PhotoImage(Image.open("data/speaker/ui/vno1.jpeg"))
        self.canvas_img.create_image(int(self.width * 0.5), 100, anchor='center', image=self.img)  # n center,nw,ne
        self.canvas_img.image = self.img  # 绑定图片

        self.var_in = tk.StringVar()
        self.var_out = tk.StringVar()
        self.var_log = tk.StringVar()
        self.label_name = tk.Label(self.master, text='您好，我是虚拟人1号。很高兴为您服务！', bg='green', font=('Arial', 12))
        self.button_recode = tk.Button(self.master, text='录音', command=self.click_recode_start)
        self.button_recode_stop = tk.Button(self.master, text='停止', command=self.click_recode_stop)
        self.button_recode_play = tk.Button(self.master, text='播放', command=self.click_recode_play)
        self.button_recode_do = tk.Button(self.master, text='检测', command=self.click_recode_do)
        self.label_info_in = tk.Label(self.master, text='输入信息:', textvariable=self.var_in, bg='yellow',
                                      font=('Arial', 12))  # textvariable=self.var , width=self.width
        self.label_info_out = tk.Label(self.master, text='输出信息:', textvariable=self.var_out, bg='lightgreen',
                                       font=('Arial', 12))

        self.label_us_name = tk.Label(self.master, text='声纹主人的昵称:', font=('Arial', 14))
        self.input_name = tk.Entry(self.master, text="爸爸", font=('Arial', 14), width=20)
        self.button_input = tk.Button(self.master, text='录入新声纹', command=self.click_recode_new)
        self.button_test = tk.Button(self.master, text='测试', command=self.click_test)
        # Message ,Text
        self.msg_log = tk.Message(self.master, bg='white', textvariable=self.var_log, font=('Arial', 12),
                                  width=self.width)
        self.var_in.set("输入信息：今天天气怎么样？")
        self.var_out.set("输出信息：天气很好，很适合和朋友一起出去玩，🍎！")
        self.var_log.set("日志：\n 输入信息：今天天气怎么样？ \n 输出信息：天气很好，很适合和朋友一起出去玩，🍎！")
        self.input_name.insert(0, "苹果爸爸")

    def widgets_pack(self):
        self.canvas_img.pack(side='top')  # place(x=0, y=0)

        self.label_name.place(x=int(self.width * 0.5 - 100), y=200)  # pack(side='top') #
        self.button_recode.place(x=200, y=230)
        self.button_recode_stop.place(x=300, y=230)  # pack()
        self.button_recode_play.place(x=400, y=230)
        self.button_recode_do.place(x=500, y=230)
        self.label_info_in.place(x=0, y=280)
        self.label_info_out.place(x=0, y=310)

        self.label_us_name.place(x=100, y=342)
        self.input_name.place(x=250, y=340)
        self.button_input.place(x=450, y=340)
        self.button_test.place(x=580, y=340)

        self.msg_log.place(x=0, y=380)
        # self.msg_log.insert("记录")

    def log(self, text):
        t = time.strftime("[%H:%M:%S] ", time.localtime())
        self.var_log.set(t + text + '\n' + self.var_log.get())
        print(text)

    def play(self, file):
        # self.show_plt(file)
        def __play():
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(loops=0)

        threading.Thread(target=__play).start()

    def chat(self):
        self.log("[AI]启动AI大脑，分析录音")
        ck = sp.check_activity(audio_file)
        if not ck:
            self.var_in.set("[输入信息]：无效！")
            return
        self.log(f'[声音状态]{ck}')
        txt = sp.asr_get_text(audio_file)
        self.log(f'[ASR]转换文字为 {txt}')
        self.var_in.set(f"[输入信息]：{txt}")
        ts1, question, answer = sp.chat_dialog(txt)
        self.var_out.set(f"[输出信息]：{answer}")
        self.log(f'[Chat] {answer}')
        self.log(f"[TTS保存]：{answer}")
        sp.tts_wav(answer,audio_file_tts)
        time.sleep(0.01)
        self.log(f"[TTS播放]：{answer}")
        pygame.mixer.music.load(audio_file_tts)
        pygame.mixer.music.play(loops=0)

    def click_test(self):
        # tts_say("主人，今天天气很好，适合和朋友出去玩！")
        self.play(audio_file_tts)

    def click_recode_new(self):
        self.log("[声纹]新录入声纹；")

        def __recode():
            self.recoder.recode(60)  # 声音长度
            time.sleep(0.1)
            self.log("[声纹]保存声纹；")
            self.recoder.save(audio_file_ck)
            time.sleep(0.1)
            self.log("[声纹]保存完毕；")

        threading.Thread(target=__recode).start()

    def click_recode_start(self):
        self.log("[录音]新录入声音；")

        def __recode_start():
            self.recoder.recode(200)

        threading.Thread(target=__recode_start).start()

    def click_recode_do(self):
        threading.Thread(target=self.chat).start()

    def click_recode_play(self):
        self.log("Play")
        self.play(audio_file)

    def click_recode_stop(self):
        self.log("[录音]停止录入声音；")
        self.recoder.stop()
        self.log("[录音]保存声音；")
        self.recoder.save(audio_file)
        # do
        threading.Thread(target=self.chat).start()

    def show_plt(self, file):
        # the figure that will contain the plot
        fig = Figure(figsize=(7, 3),
                     dpi=100)
        # adding the subplot
        plot1 = fig.add_subplot(211)  # 111
        # 原始音频
        clean = read_audio(file).squeeze()
        # plotting the graph :
        plot1.plot(clean)  # 数值 #plot1.plot(y)

        plot2 = fig.add_subplot(212)
        plot2.specgram(clean, Fs=16000)  # specgram()函数用于绘制频谱图。
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas_plt = FigureCanvasTkAgg(fig, master=self.master)
        canvas_plt.draw()
        # placing the canvas on the Tkinter window
        canvas_plt.get_tk_widget().place(x=int(self.width * 0.5 - 350), y=500)


app = Application()
# 设置窗口
app.master.title('虚拟人1号（Virtual Human No. 1）')
app.master.geometry('800x800')

# 主消息循环:
app.mainloop()
