#!/usr/bin/python3
# -*- coding: utf-8 -*-

''' 国家语言：
Arabic, Basque, Breton, Catalan, Chinese_China, Chinese_Hongkong, Chinese_Taiwan, Chuvash, Czech, Dhivehi, Dutch, English,
Esperanto, Estonian, French, Frisian, Georgian, German, Greek, Hakha_Chin, Indonesian, Interlingua, Italian, Japanese,
Kabyle, Kinyarwanda, Kyrgyz, Latvian, Maltese, Mangolian, Persian, Polish, Portuguese, Romanian, Romansh_Sursilvan, 
Russian, Sakha, Slovenian, Spanish, Swedish, Tamil, Tatar, Turkish, Ukranian, Welsh
'''

import torchaudio
from speechbrain.pretrained import EncoderClassifier
 
# https://huggingface.co/speechbrain/lang-id-commonlanguage_ecapa
_model_dir='/Users/liampro/Downloads/dataLake/Models/audio/speechbrain/lang-id-commonlanguage_ecapa'

class AudioLangID:
    def __init__(self,source=_model_dir, savedir=_model_dir ):
        self.classifier = EncoderClassifier.from_hparams(source=source, savedir=savedir)

    def predict(self,audio_file="test.wav"):
        out_prob, score, index, text_lab = self.classifier.classify_file(audio_file)
        #print(text_lab)
        # ['Italian']
        return text_lab[0],int(index)