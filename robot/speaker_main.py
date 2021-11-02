#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

from robot.audio_pre import AudioPre
from robot.audio_asr import AudioASR
from robot.nlp_chat import NLPChat
from robot.tts_espnet import TTSespnet

# 处理智能音箱流程
ck = AudioPre()
asr = AudioASR()
chat = NLPChat()
tts = TTSespnet()


def check_activity(audio_file):
    num = ck.get_chunks_num(audio_file)
    min_num = 100  # 参数：是否有声音的界限
    if num > min_num:
        print("检测声音是否活动:有声音")
        return True
    else:
        print("检测声音是否活动:没有声音")
    print("num:", num)
    return False


def asr_get_text(audio_file):
    audio_text = asr.transcription_text(audio_file, rate=16000)
    print("声音转文字:", audio_text)
    return audio_text


def chat_dialog(question_text="", his=[]):
    # ts1,question,answer = \
    return chat.dialog(question_text, his)


def tts_wav(text, file):
    tts.creat_wav(text, file)
