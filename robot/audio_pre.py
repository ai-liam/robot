#!/usr/bin/python3
# -*- coding: utf-8 -*-
from speechbrain.pretrained import VAD

# https://huggingface.co/speechbrain/vad-crdnn-libriparty
_model_dir = '/Users/liampro/Downloads/dataLake/Models/audio/speechbrain/vad-crdnn-libriparty'

class AudioPre:
    def __init__(self,model_dir=_model_dir,save_dir= _model_dir):
        self.VAD = VAD.from_hparams(source=model_dir, savedir=save_dir)
    
    # 获取有效声音块
    def get_chunks_num(self,audio_file="test.wav"):
        boundaries = self.VAD.get_speech_segments(audio_file)
        v= self.VAD.save_boundaries(boundaries)
        prob_chunks = self.VAD.get_speech_prob_file(audio_file)
        prob_th = self.VAD.apply_threshold(prob_chunks, activation_th=0.5, deactivation_th=0.25).float()
        #check
        db = list(prob_th.squeeze())
        num =0
        for i in db:
            j = int(i)
            if j > 0:
                num+=1
        return num

if __name__ == "__main__":
    r= AudioPre()
    num= r.get_chunks_num("test.wav")
    if num > 100:
        print("有声音")
    else:
        print("没有声音")