import sys, os

sys.path.append('./data/speaker/external-libraries')

import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from speechbrain.dataio.dataio import read_audio
import threading
import time

# self
import robot.speaker_main as sp

audio_file = "data/speaker/temp/recoder1.wav"
audio_file_ck = "data/speaker/temp/ck_master.wav"
audio_file_ck_temp = "data/speaker/temp/ck_temp.wav"
audio_file_tts = "data/speaker/temp/tts_master.wav"
audio_file_temp = "data/speaker/temp/1_temp.wav"
audio_file_auto = "data/speaker/temp/auto_temp.wav"
audio_file_auto_chat = "data/speaker/temp/auto_chat_temp.wav"


class Application(tk.Frame):
    def __init__(self, master=tk.Tk(), width=800, height=800):
        tk.Frame.__init__(self, master)
        self.width = width
        self.height = height
        self.pack()
        self.create_widgets()
        self.widgets_pack()
        self.flag_auto_check = True
        self.flag_auto_chat = True
        # other
        # self.show_plt(audio_file)

    def create_widgets(self):
        self.canvas_img = tk.Canvas(self.master, height=180, width=self.width)
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
        self.input_name = tk.Entry(self.master, text="爸爸", font=('Arial', 14), width=10)
        self.button_input = tk.Button(self.master, text='录入新声纹', command=self.click_recode_new)
        self.button_people_check = tk.Button(self.master, text='录入并检测声纹', command=self.click_people_check)
        self.button_auto_check_activity = tk.Button(self.master, text='自动测声音', command=self.click_check_activity)
        self.button_auto_chat = tk.Button(self.master, text='自动聊天', command=self.click_auto_chat)
        self.button_test = tk.Button(self.master, text='测试', command=self.click_test)
        # self.button_people_temp = tk.Button(self.master, text='录入并检测声纹', command=self.click_people_temp)
        # Message ,Text
        self.msg_log = tk.Message(self.master, bg='white', textvariable=self.var_log, font=('Arial', 12),
                                  width=self.width)
        self.var_in.set("输入信息：今天天气怎么样？")
        self.var_out.set("输出信息：天气很好，很适合和朋友一起出去玩，🍎！")
        self.var_log.set("日志：\n 输入信息：今天天气怎么样？ \n 输出信息：天气很好，很适合和朋友一起出去玩，🍎！")
        self.input_name.insert(0, "苹果爸爸")

    def widgets_pack(self):
        self.canvas_img.place(x=0, y=0)  # pack(side='top')  #

        self.label_name.place(x=int(self.width * 0.5 - 100), y=200)  # pack(side='top') #
        self.button_recode.place(x=200, y=230)
        self.button_recode_stop.place(x=300, y=230)  # pack()
        self.button_recode_play.place(x=400, y=230)
        self.button_recode_do.place(x=500, y=230)
        self.label_info_in.place(x=0, y=280)
        self.label_info_out.place(x=0, y=310)

        self.label_us_name.place(x=10, y=342)
        self.input_name.place(x=150, y=340)
        self.button_input.place(x=250, y=340)
        self.button_people_check.place(x=360, y=340)
        self.button_auto_check_activity.place(x=500, y=340)
        self.button_auto_chat.place(x=600, y=340)
        self.button_test.place(x=720, y=340)

        self.msg_log.place(x=0, y=380)

    def log(self, text):
        t = time.strftime("[%H:%M:%S] ", time.localtime())
        self.var_log.set(t + text + '\n' + self.var_log.get())
        print(text)

    def chat(self, file=audio_file, file_tts=audio_file_tts, min_num=150):
        self.log("[AI]启动AI大脑，分析录音")
        ck = sp.check_activity(file, min_num=min_num)
        if not ck:
            self.log("[声音状态]: 无效")
            return
        self.log(f'[声音状态]{ck}')
        txt = sp.asr_get_text(file)
        self.log(f'[ASR]转换文字为 {txt}')
        if txt == "":
            return
        self.var_in.set(f"[输入信息]：{txt}")
        ts1, question, answer = sp.chat_dialog(txt)
        self.var_out.set(f"[输出信息]：{answer}")
        self.log(f'[Chat] {answer}')
        self.log(f"[TTS保存]：{answer}")
        sp.tts_wav(answer, file_tts)
        time.sleep(0.01)
        self.log(f"[TTS播放]：{answer}")
        sp.play(file_tts)
        time.sleep(3)

    def check_activity(self, time_count=60, file=audio_file_auto):
        self.log('[声音状态]录入和保存声音')
        sp.recode_and_save(time_count, file)
        self.log('[声音状态]开始检测数据')
        ck = sp.check_activity(file, 150)
        if not ck:
            self.log("[结果]：无效")
            return
        self.log(f'[结果]有声音')

    def auto_chat(self, time_count=60, file=audio_file_auto_chat):
        self.log('[CHAT]新一轮聊天')
        self.log('[声音]录入和保存声音')
        sp.recode_and_save(time_count, file)
        self.log('[声音]开始检测数据')
        self.chat(file, audio_file_tts)

    def click_test(self):
        self.flag_auto_check = False
        self.flag_auto_chat = False
        self.log("[X]关掉自动检测声音")

    def click_auto_chat(self):
        self.log('[CHAT]开始自动聊天模式')
        self.flag_auto_chat = True

        def __thread():
            while self.flag_auto_chat:
                time.sleep(0.1)
                self.auto_chat(80, audio_file_auto_chat)
                time.sleep(0.1)

        threading.Thread(target=__thread).start()

    # 自动检测声音是否有人说话
    def click_check_activity(self):
        self.log('[声音状态]开始自动检测有没人说话')
        self.flag_auto_check = True

        def __thread():
            while self.flag_auto_check:
                time.sleep(0.1)
                self.check_activity(50, audio_file_auto)
                time.sleep(1)

        threading.Thread(target=__thread).start()

    def click_people_check(self):
        self.log("[声纹验证]录入声纹并验证；")

        def __recode():
            self.log("[声纹]录入和保存声纹；")
            sp.recode_and_save(60, audio_file_ck_temp)  # 声音长度
            time.sleep(0.01)
            self.log("[声纹]保存完毕；")
            score, prediction = sp.check_people_by_audio(audio_file_ck_temp, audio_file_ck)
            if prediction:
                self.log(f"[声纹验证]同1个人；score:{score}")
                sp.tts_say(f"您好，{self.input_name.get()}，您来了！", audio_file_temp)
            else:
                self.log(f"[声纹验证]匹配不成功；score:{score}")
                sp.tts_say("你是谁？", audio_file_temp)

        threading.Thread(target=__recode).start()

    def click_recode_new(self):
        self.log("[声纹]新录入声纹；")

        def __thread():
            sp.recode_and_save(60, audio_file_ck)
            self.log("[声纹]保存声纹完毕；")

        threading.Thread(target=__thread).start()

    def click_recode_start(self):
        self.log("[录音]新录入声音；")
        threading.Thread(target=sp.recode, args=(200,)).start()

    def click_recode_do(self):
        threading.Thread(target=self.chat, args=(audio_file, audio_file_tts)).start()

    def click_recode_play(self):
        self.log("Play")
        sp.play(audio_file)

    def click_recode_stop(self):
        self.log("[录音]停止录入声音；")
        sp.recode_stop()
        self.log("[录音]保存声音；")
        sp.recode_save(audio_file)
        # do
        threading.Thread(target=self.chat, args=(audio_file, audio_file_tts)).start()

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
