# 备注

## TTS备选

import pythoncom
from win32com import client
 
pythoncom.CoInitialize()
engine=client.Dispatch("SAPI.SpVoice")
engine.Speak('hello，你好呀')

