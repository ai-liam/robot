
import soundfile
from espnet2.bin.tts_inference import Text2Speech

# https://zenodo.org/record/4036268/files/tts_train_conformer_fastspeech2_raw_phn_tacotron_g2p_en_no_space_train.loss.ave.zip?download=1:
_model_path = "/Users/liampro/Downloads/dataLake/Models/audio/espnet/tts/tts_train_conformer_fastspeech2_raw_phn_tacotron_g2p_en_no_space_train.loss.ave.zip"

class TTSespnet:
    def __init__(self ,model_path=_model_path ):
        self.text2speech = Text2Speech.from_pretrained(model_path)

    def creat_wav(self ,text="我喜欢踢足球,foobar.我也喜欢玩游戏." ,audio_file="ts.wav"):
        speech = self.text2speech(text)["wav"]
        # audio_file = "data/speaker/temp/tts_out.wav"
        soundfile.write(audio_file, speech.numpy(), self.text2speech.fs, "PCM_16")
