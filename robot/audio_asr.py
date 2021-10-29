#!/usr/bin/python3
# -*- coding: utf-8 -*-

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa

#LANG_ID = "zh-CN"
# https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn
_model_path ='/Users/liampro/Downloads/dataLake/Models/nlp/huggingface/wav/jonatasgrosman/wav2vec2-large-xlsr-53-chinese-zh-cn'
#SAMPLES = 10

class AudioASR:
    def __init__(self,model_path=_model_path ):
        self.tokenizer = Wav2Vec2Processor.from_pretrained(model_path)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_path)

    #transcription
    def transcription_text(self,audio_path,rate=16000):
        # Load the audio with the librosa library
        input_audio, _ = librosa.load(audio_path, sr=rate)

        # Tokenize the audio
        inputs = self.tokenizer(input_audio, return_tensors="pt", padding="longest")
        #print('input:',inputs)
        input_values = inputs.input_values

        # Feed it through Wav2Vec & choose the most probable tokens
        with torch.no_grad():
            logits = self.model(input_values).logits
            #print('logits:',logits)
            predicted_ids = torch.argmax(logits, dim=-1)

        # Decode & add to our caption string
        transcription = self.tokenizer.batch_decode(predicted_ids)[0]
        return transcription