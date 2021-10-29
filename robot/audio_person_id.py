#!/usr/bin/python3
# -*- coding: utf-8 -*-

from speechbrain.pretrained import SpeakerRecognition
 
# https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb
_model_dir='/Users/liampro/Downloads/dataLake/Models/audio/speechbrain/spkrec-ecapa-voxceleb'

class AudioPersonID:
    def __init__(self,source=_model_dir, savedir=_model_dir ):
        self.verification = SpeakerRecognition.from_hparams(source=source, savedir=savedir)

    def predict(self,audio_check="test.wav",audio_origin="origin.wav"):
        score, prediction = self.verification.verify_files(audio_check,audio_origin)
        return float(score[0]), bool(prediction[0])