#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import pygame
import threading

from robot.audio_pre import AudioPre
from robot.audio_asr import AudioASR
from robot.nlp_chat import NLPChat
from robot.audio_tts_espnet import TTSespnet
from robot.audio_person_id import AudioPersonID
from robot.recode import Recoder  # self

pygame.mixer.init()  # initialise the pygame
# 处理智能音箱流程
ck = AudioPre()
asr = AudioASR()
chat = NLPChat()
tts = TTSespnet()
person = AudioPersonID()
recoder = Recoder()


def check_people_by_audio(audio_check="test.wav", audio_origin="origin.wav"):
    # 比较2个声音（同人）
    score, prediction = person.predict(audio_check, audio_origin)
    return score, prediction


def play(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(loops=0)


def play_by_thread(file):
    threading.Thread(target=play, args=(file,)).start()


def check_activity(audio_file, min_num=100):
    num = ck.get_chunks_num(audio_file)
    # min_num = 100  # 参数：是否有声音的界限
    print("check_activity-num:", num)
    if num > min_num:
        print("检测声音是否活动:有声音")
        return True
    else:
        print("检测声音是否活动:没有声音")
    return False


def asr_get_text(audio_file):
    audio_text = asr.transcription_text(audio_file, rate=16000)
    print("声音转文字:", audio_text)
    return audio_text


def chat_dialog(question_text="", his=[]):
    # ts1,question,answer = \
    return chat.dialog(question_text, his)


def tts_wav(text, file):
    print(f"[TTS]{text}")
    tts.creat_wav(text, file)


def tts_say(text, file):
    tts_wav(text, file)
    play(file)


def recode(time_count=60):
    recoder.recode(time_count)


def recode_and_save(time_count=60, file="temp.wav"):
    recoder.recode(time_count)
    print("save recoder file")
    recoder.save(file)
    print("save recoder file finish")


def recode_stop():
    recoder.stop()


def recode_save(file):
    recoder.save(file)
